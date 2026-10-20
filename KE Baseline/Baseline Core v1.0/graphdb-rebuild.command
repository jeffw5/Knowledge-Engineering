#!/bin/bash
# Rebuild a GraphDB repository from Baseline Core v1.0: back up, clear, load in dependency order, check lineage.
#
#   graphdb-rebuild.command [repository]          (default: value-kb)
#   GRAPHDB_URL=http://host:7200 graphdb-rebuild.command my-repo
#
# Order: BFO 2020 → RO Core → RO extract → core vocabularies → core taxonomies → core domain ontology → core shapes.
# The whole repository is saved to KE Baseline/Archive Baseline Core v0.1/graphdb-backup-<time>/repository.trig
# before anything is cleared,
# and you are asked to type the repository name before it is cleared. The audit log (graph …/graph/change-log) is
# append-only: it is saved separately, put back after the clear, and the change records in trig/ are added to it.

REPO="${1:-value-kb}"
GDB="${GRAPHDB_URL:-http://localhost:7200}"
cd "$(dirname "$0")" || exit 1
BASE="$(pwd)"
STAMP="$(date -u +%Y-%m-%dT%H%M%SZ)"
OUT="$(cd "$BASE/.." && pwd)/Archive Baseline Core v0.1/graphdb-backup-$STAMP"
EP="$GDB/repositories/$REPO"
fail() { echo; echo "STOPPED: $*"; echo; read -n1 -r -p "Press any key to close." _; exit 1; }

echo "Baseline Core v1.0 rebuild  ·  repository $REPO at $GDB"
echo
curl -sf "$GDB/rest/repositories" >/dev/null || fail "GraphDB is not answering at $GDB. Start GraphDB and try again."
curl -sf -o /dev/null "$EP/size" || fail "There is no repository called \"$REPO\". Give its ID: graphdb-rebuild.command <repository>"

# ── 0. find the reference files first, so a missing download never leaves an empty repository ──
BFO_SRC="$BASE/reference/bfo-core.ttl"; BFO_TYPE=text/turtle
mkdir -p "$OUT"
if [ ! -f "$BFO_SRC" ]; then
  BFO_SRC="$OUT/bfo.owl"; BFO_TYPE=application/rdf+xml
  curl -sfL -H 'Accept: application/rdf+xml' "http://purl.obolibrary.org/obo/bfo.owl" -o "$BFO_SRC" || fail "could not download BFO; nothing was changed."
fi
RO_SRC="${RO_CORE:-$(ls "$BASE"/reference/ro-core.owl 2>/dev/null | head -1)}"
if [ -z "$RO_SRC" ]; then
  RO_SRC="$OUT/ro-core.owl"
  curl -sfL -H 'Accept: application/rdf+xml' "http://purl.obolibrary.org/obo/ro/core.owl" -o "$RO_SRC" \
    || fail "could not download RO Core; nothing was changed. Put a copy at reference/ro-core.owl and run again."
fi
[ -f "$BASE/reference/ro-extract.ttl" ] || fail "reference/ro-extract.ttl is missing; nothing was changed."

# ── 1. back up ─────────────────────────────────────────────────────────────
echo "1/5  Backing up $REPO (explicit statements, all graphs)…"
curl -sf -G "$EP/statements" --data-urlencode 'infer=false' -H 'Accept: application/x-trig' -o "$OUT/repository.trig" \
  || fail "the backup failed; nothing was cleared."
SIZE=$(wc -c < "$OUT/repository.trig" | tr -d ' ')
echo "     saved $OUT/repository.trig ($SIZE bytes)"
curl -sf "$EP/namespaces" -H 'Accept: text/csv' -o "$OUT/namespaces.csv"
LOG="https://www.insperity.com/graph/change-log"
curl -sf -G "$EP/statements" --data-urlencode "context=<$LOG>" --data-urlencode 'infer=false' -H 'Accept: application/x-trig' -o "$OUT/change-log.trig" \
  || fail "the audit log could not be saved; nothing was cleared."
echo "     saved the audit log to $OUT/change-log.trig ($(grep -c 'ChangeRecord' "$OUT/change-log.trig" | tr -d ' ') record lines)"

# ── 2. confirm and clear ──────────────────────────────────────────────────
echo
echo "2/5  This deletes every statement in \"$REPO\" (the backup above can restore it)."
read -r -p "     Type the repository name to clear it: " ANSWER
[ "$ANSWER" = "$REPO" ] || fail "not confirmed; nothing was cleared."
curl -sf -X DELETE "$EP/statements" || fail "GraphDB refused to clear the repository."
echo "     cleared ($(curl -sf "$EP/size") statements left)"

load() {   # load <file> <content-type> [graph]  — a TriG file carries its own graph
  local f="$1" ct="$2" g="$3" url="$EP/statements"
  [ -n "$g" ] && url="$url?context=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote("<"+sys.argv[1]+">"))' "$g")"
  if curl -sf -X POST "$url" -H "Content-Type: $ct; charset=utf-8" --data-binary @"$f" -o /dev/null; then
    echo "     ✓ $(basename "$f")"
  else
    echo "     ✗ $(basename "$f")  (GraphDB refused it)"; ERRORS=$((ERRORS+1))
  fi
}
ERRORS=0

# ── 3. reference ontologies ───────────────────────────────────────────────
echo
echo "3/5  Reference ontologies"
if [ "$BFO_TYPE" = text/turtle ]; then load "$BFO_SRC" text/turtle "http://purl.obolibrary.org/obo/bfo.owl"; else load "$BFO_SRC" application/rdf+xml "http://purl.obolibrary.org/obo/bfo.owl"; fi
load "$RO_SRC" application/rdf+xml "http://purl.obolibrary.org/obo/ro/core.owl"
load "$BASE/reference/ro-extract.ttl" text/turtle "https://www.insperity.com/reference/ro-extract/"

# ── 4. KE Baseline, in dependency order ───────────────────────────────────
echo
echo "4/5  Baseline Core v1.0"
if [ -s "$OUT/change-log.trig" ]; then load "$OUT/change-log.trig" application/x-trig; fi   # the audit log, put back as it was
for group in vocabulary-core taxonomy-core ontology-core shapes-core change-record; do
  for f in "$BASE"/trig/$group-*.trig; do
    [ -e "$f" ] || continue
    load "$f" application/x-trig
  done
done
[ "$ERRORS" -eq 0 ] || echo "     $ERRORS file(s) were not loaded; see above."

# ── 5. lineage checks ─────────────────────────────────────────────────────
echo
echo "5/5  Lineage checks (0 is clean; the taxonomy figures count what is still open for review)"
P='PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX skos: <http://www.w3.org/2004/02/skos/core#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX core: <https://www.insperity.com/ontology/core/> '
count() {   # count <label> <where>
  local n
  n=$(curl -sf -G "$EP" --data-urlencode "query=$P SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE { $2 }" -H 'Accept: text/csv' | tail -1 | tr -d '\r')
  printf '     %-62s %s\n' "$1" "${n:-?}"
}
count "core classes with no BFO ancestor" \
  'GRAPH <https://www.insperity.com/ontology/core/> { ?x a owl:Class } FILTER NOT EXISTS { ?x rdfs:subClassOf+ ?b FILTER(STRSTARTS(STR(?b), "http://purl.obolibrary.org/obo/BFO_")) }'
count "core relations with no BFO/RO/IAO ancestor (or inverse)" \
  'GRAPH <https://www.insperity.com/ontology/core/> { ?x a owl:ObjectProperty } FILTER NOT EXISTS { ?x rdfs:subPropertyOf+ ?r FILTER(STRSTARTS(STR(?r), "http://purl.obolibrary.org/obo/")) } FILTER NOT EXISTS { { ?x owl:inverseOf ?y } UNION { ?y owl:inverseOf ?x } ?y rdfs:subPropertyOf+ ?r2 FILTER(STRSTARTS(STR(?r2), "http://purl.obolibrary.org/obo/")) }'
count "taxonomy top concepts with no core:formalizedBy" \
  '?s skos:hasTopConcept ?x FILTER(STRSTARTS(STR(?s), "https://www.insperity.com/taxonomy/core-")) FILTER NOT EXISTS { ?x core:formalizedBy ?c }'
count "core:formalizedBy targets that are not core classes" \
  '?t core:formalizedBy ?x FILTER NOT EXISTS { GRAPH <https://www.insperity.com/ontology/core/> { ?x a owl:Class } }'
count "taxonomy concepts with no vocabulary primitive" \
  '?x a skos:Concept ; skos:inScheme ?s FILTER(STRSTARTS(STR(?s), "https://www.insperity.com/taxonomy/core-")) FILTER NOT EXISTS { ?x dct:subject ?v . ?v a skos:Concept ; skos:inScheme ?vs FILTER(STRSTARTS(STR(?vs), "https://www.insperity.com/vocabulary/")) }'
count "links to vocabulary terms that are not loaded" \
  '?t core:hasPrimaryTerm|dct:subject ?x FILTER(STRSTARTS(STR(?x), "https://www.insperity.com/vocabulary/")) FILTER(STRSTARTS(STR(?t), "https://www.insperity.com/")) FILTER NOT EXISTS { ?x a skos:Concept } FILTER(!STRENDS(STR(?x), "/"))'
EXPECT=$(( $(ls "$BASE"/trig/*.trig | grep -vc change-record) + 4 ))
echo; count "graphs in the repository (expected: $EXPECT)" '{ GRAPH ?x { ?s ?p ?o } }'
count "change records in the audit log" 'GRAPH <https://www.insperity.com/graph/change-log> { ?x a <http://www.w3.org/ns/prov#Activity> }'
echo
echo "Done. Backup: $OUT"
echo "In the KE Workbench: Model Editor (Ontology) › ⚙ › Reload."
read -n1 -r -p "Press any key to close." _
