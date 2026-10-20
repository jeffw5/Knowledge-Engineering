#!/bin/bash
# Load the Commercial Operations domains into a GraphDB repository that already holds Baseline Core v1.0.
#
#   graphdb-load.command                          all domains, repository value-kb
#   graphdb-load.command value-kb sales legal     only these domains (the Commercial Operations container is added if missing)
#   GRAPHDB_URL=http://host:7200 graphdb-load.command my-repo
#
# Insulation: the script replaces only the named graphs of the domains it loads
# (https://www.insperity.com/{vocabulary,taxonomy,ontology,shapes}/domain-<name>/) and of their assembly components
# (https://www.insperity.com/resource/domain-<name>/{persona-graph,party-graph,step-graph,process-graph,service-graph,value-map,manifest}/…/).
# Assembly graphs of a loaded domain that are no longer in its assembly folder (superseded by a release) are backed
# up and removed, so GraphDB holds exactly the current release.
# Only the latest version of each asset in a domain's trig/ folder is loaded. It never clears the repository and
# never writes a core or baseline graph; it counts the baseline statements before and after and stops if they differ.
# Each replaced graph is first saved to archive/graphdb-backup-<time>/. Change records are appended to the audit log
# (graph …/graph/change-log), which is append-only.

REPO="${1:-value-kb}"; shift 2>/dev/null
GDB="${GRAPHDB_URL:-http://localhost:7200}"
cd "$(dirname "$0")" || exit 1
BASE="$(pwd)"
STAMP="$(date -u +%Y-%m-%dT%H%M%SZ)"
OUT="$BASE/archive/graphdb-backup-$STAMP"
EP="$GDB/repositories/$REPO"
NS="https://www.insperity.com/"
fail() { echo; echo "STOPPED: $*"; echo; read -n1 -r -p "Press any key to close." _; exit 1; }
enc() { python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$1"; }
P='PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX skos: <http://www.w3.org/2004/02/skos/core#> PREFIX dct: <http://purl.org/dc/terms/> PREFIX core: <https://www.insperity.com/ontology/core/> '
ask() { curl -sf -G "$EP" --data-urlencode "query=$P SELECT (COUNT(*) AS ?n) WHERE { $1 }" -H 'Accept: text/csv' | tail -1 | tr -d '\r'; }
count() { local n; n=$(curl -sf -G "$EP" --data-urlencode "query=$P SELECT (COUNT(DISTINCT ?x) AS ?n) WHERE { $2 }" -H 'Accept: text/csv' | tail -1 | tr -d '\r'); printf '     %-66s %s\n' "$1" "${n:-?}"; }
# the trig files of a domain, latest version of each asset, in load order (assets, then assembly components)
files_of() {
  local d="$1" kind f
  for kind in vocabulary taxonomy ontology shapes; do
    ls "$BASE/$d"/trig/$kind-domain-*.trig 2>/dev/null | sort -V | tail -1
  done
  for kind in persona-graph party-graph step-graph process-graph service-graph value-map manifest; do
    for f in "$BASE/$d"/assembly/trig/$kind-*.trig; do [ -e "$f" ] && echo "$f"; done
  done
}
GRAPH_RX='^https://www\.insperity\.com/((vocabulary|taxonomy|ontology|shapes)/domain-[a-z0-9-]+/|resource/domain-[a-z0-9-]+/(persona-graph|party-graph|step-graph|process-graph|service-graph|value-map|manifest)/[a-z0-9.-]+/)$'
BASELINE='GRAPH ?g { ?s ?p ?o } FILTER(REGEX(STR(?g), "^https://www.insperity.com/((vocabulary|taxonomy|ontology|shapes)/core|reference/)") || STRSTARTS(STR(?g), "http://purl.obolibrary.org/obo/"))'

echo "Commercial Operations domains  ·  repository $REPO at $GDB"
echo
curl -sf "$GDB/rest/repositories" >/dev/null || fail "GraphDB is not answering at $GDB. Start GraphDB and try again."
curl -sf -o /dev/null "$EP/size" || fail "There is no repository called \"$REPO\". Give its ID: graphdb-load.command <repository>"
[ "$(ask 'GRAPH <https://www.insperity.com/ontology/core/> { ?s ?p ?o }')" -gt 0 ] 2>/dev/null \
  || fail "the core domain ontology is not in \"$REPO\". Load Baseline Core v1.0 first (KE Baseline/Baseline Core v1.0/graphdb-rebuild.command)."

# ── which domains ───────────────────────────────────────────────────────────
ALL="commercial-operations sales marketing legal customer-success pricing-and-contracts partner-and-channel"
WANT="${*:-$ALL}"
case " $WANT " in *" commercial-operations "*) ;; *)
  if [ "$(ask 'GRAPH <https://www.insperity.com/ontology/domain-commercial-operations/> { ?s ?p ?o }')" = "0" ]; then
    echo "     The Commercial Operations container is not loaded yet; adding it (every domain imports it)."; WANT="commercial-operations $WANT"; fi ;;
esac
for d in $WANT; do [ -d "$BASE/$d/trig" ] || fail "no domain folder \"$d\" (known: $ALL)"; done

BEFORE=$(ask "$BASELINE")
echo "1/4  Baseline statements before: $BEFORE"

# ── back up the graphs about to be replaced ─────────────────────────────────
echo
echo "2/4  Backing up the domain graphs that will be replaced"
mkdir -p "$OUT"
for d in $WANT; do
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    G=$(grep -m1 '^# Named graph: ' "$f" | sed 's/^# Named graph: //')
    [[ "$G" =~ $GRAPH_RX ]] || fail "$(basename "$f") names graph \"$G\", which is not a domain graph; nothing was changed."
    curl -sf -G "$EP/statements" --data-urlencode "context=<$G>" --data-urlencode 'infer=false' -H 'Accept: application/x-trig' -o "$OUT/$(basename "$f")" \
      || fail "the backup of $G failed; nothing was changed."
  done < <(files_of "$d")
done
# assembly graphs in GraphDB that the current release no longer has (for example a step graph a release replaced)
STALE=()
for d in $WANT; do
  CUR=" "; while IFS= read -r f; do [ -n "$f" ] && CUR="$CUR$(grep -m1 '^# Named graph: ' "$f" | sed 's/^# Named graph: //') "; done < <(files_of "$d")
  while IFS= read -r G; do
    G=$(echo "$G" | tr -d '\r'); [ -n "$G" ] || continue
    case "$CUR" in *" $G "*) ;; *)
      curl -sf -G "$EP/statements" --data-urlencode "context=<$G>" --data-urlencode 'infer=false' -H 'Accept: application/x-trig' -o "$OUT/stale-$(echo "$G" | sed 's#^https://www.insperity.com/resource/##; s#/$##; s#/#-#g').trig" \
        || fail "the backup of $G failed; nothing was changed."
      STALE+=("$G") ;;
    esac
  done < <(curl -sf -G "$EP" --data-urlencode "query=SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } FILTER(REGEX(STR(?g), \"^${NS}resource/domain-$d/(persona-graph|party-graph|step-graph|process-graph|service-graph|value-map|manifest)/\")) }" -H 'Accept: text/csv' | tail -n +2)
done
echo "     saved to $OUT"

# ── replace each domain graph ───────────────────────────────────────────────
echo
echo "3/4  Loading (each graph is cleared and reloaded; nothing else is touched)"
ERRORS=0
for d in $WANT; do
  echo "   $d"
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    G=$(grep -m1 '^# Named graph: ' "$f" | sed 's/^# Named graph: //')
    curl -sf -X DELETE "$EP/statements?context=$(enc "<$G>")" || { echo "     ✗ could not clear $G"; ERRORS=$((ERRORS+1)); continue; }
    if curl -sf -X POST "$EP/statements" -H 'Content-Type: application/x-trig; charset=utf-8' --data-binary @"$f" -o /dev/null; then
      echo "     ✓ $(basename "$f")"
    else
      echo "     ✗ $(basename "$f")  (GraphDB refused it; restore from $OUT)"; ERRORS=$((ERRORS+1))
    fi
  done < <(files_of "$d")
done
for G in "${STALE[@]}"; do
  curl -sf -X DELETE "$EP/statements?context=$(enc "<$G>")" && echo "     − removed superseded ${G#${NS}resource/}" || { echo "     ✗ could not remove $G"; ERRORS=$((ERRORS+1)); }
done
for f in "$BASE"/change-log/*.trig; do
  [ -e "$f" ] || continue
  ID=$(grep -m1 -o 'ChangeRecord/[^>]*' "$f")
  if [ "$(ask "GRAPH <${NS}graph/change-log> { <${NS}resource/change-log/$ID> ?p ?o }")" = "0" ]; then
    curl -sf -X POST "$EP/statements" -H 'Content-Type: application/x-trig; charset=utf-8' --data-binary @"$f" -o /dev/null \
      && echo "     ✓ audit log + $(basename "$f")" || { echo "     ✗ $(basename "$f")"; ERRORS=$((ERRORS+1)); }
  fi
done
[ "$ERRORS" -eq 0 ] || echo "     $ERRORS file(s) were not loaded; see above."

AFTER=$(ask "$BASELINE")
[ "$BEFORE" = "$AFTER" ] || fail "the baseline graphs changed ($BEFORE → $AFTER statements). Restore them with KE Baseline/Baseline Core v1.0/graphdb-rebuild.command."

# ── checks ──────────────────────────────────────────────────────────────────
echo
echo "4/4  Checks (0 is clean)"
D='FILTER(REGEX(STR(?g), "^https://www.insperity.com/[a-z]+/domain-"))'
count "domain classes with no BFO ancestor" \
  "GRAPH ?g { ?x a owl:Class } $D FILTER(isIRI(?x)) FILTER NOT EXISTS { ?x rdfs:subClassOf+ ?b FILTER(STRSTARTS(STR(?b), \"http://purl.obolibrary.org/obo/BFO_\")) }"
count "domain relations with no BFO/RO/IAO ancestor" \
  "GRAPH ?g { ?x a owl:ObjectProperty } $D FILTER NOT EXISTS { ?x rdfs:subPropertyOf+ ?r FILTER(STRSTARTS(STR(?r), \"http://purl.obolibrary.org/obo/\")) }"
count "domain taxonomy top concepts with no core:formalizedBy" \
  '?s skos:hasTopConcept ?x FILTER(STRSTARTS(STR(?s), "https://www.insperity.com/taxonomy/domain-")) FILTER NOT EXISTS { ?x core:formalizedBy ?c }'
count "core:formalizedBy targets that are not classes" \
  '?t core:formalizedBy ?x FILTER NOT EXISTS { ?x a owl:Class }'
count "domain taxonomy concepts with no vocabulary primitive" \
  '?x a skos:Concept ; skos:inScheme ?s FILTER(STRSTARTS(STR(?s), "https://www.insperity.com/taxonomy/domain-")) FILTER NOT EXISTS { ?x core:hasPrimaryTerm ?v . ?v a skos:Concept }'
count "links to vocabulary terms that are not loaded" \
  '?t core:hasPrimaryTerm|dct:subject ?x FILTER(STRSTARTS(STR(?t), "https://www.insperity.com/taxonomy/domain-") || STRSTARTS(STR(?t), "https://www.insperity.com/ontology/domain-")) FILTER(STRSTARTS(STR(?x), "https://www.insperity.com/vocabulary/")) FILTER NOT EXISTS { ?x a skos:Concept } FILTER(!STRENDS(STR(?x), "/"))'
count "broad matches to concepts that are not loaded" \
  '?t skos:broadMatch ?x FILTER(STRSTARTS(STR(?t), "https://www.insperity.com/taxonomy/domain-")) FILTER NOT EXISTS { ?x a skos:Concept }'
count "assembly resources with no core or domain class" \
  'GRAPH ?g { ?x ?p ?o } FILTER(STRSTARTS(STR(?g), "https://www.insperity.com/resource/domain-")) FILTER(STRSTARTS(STR(?x), "https://www.insperity.com/resource/domain-")) FILTER NOT EXISTS { ?x a ?c . ?c a owl:Class }'
count "assembly resources classified by a concept that is not loaded" \
  'GRAPH ?g { ?x dct:type ?t } FILTER(STRSTARTS(STR(?g), "https://www.insperity.com/resource/domain-")) FILTER NOT EXISTS { ?t a skos:Concept }'
count "references from one domain to a sibling domain (insulation)" \
  'GRAPH ?g { ?s ?p ?x } FILTER(REGEX(STR(?g), "^https://www.insperity.com/[a-z]+/domain-")) FILTER(isIRI(?x) && REGEX(STR(?x), "^https://www.insperity.com/[a-z]+/domain-"))
   BIND(REPLACE(STR(?g), "^https://www.insperity.com/[a-z]+/domain-([a-z0-9-]+)/.*$", "$1") AS ?gd)
   BIND(REPLACE(STR(?x), "^https://www.insperity.com/[a-z]+/domain-([a-z0-9-]+)/.*$", "$1") AS ?xd)
   FILTER(?xd != ?gd && ?xd != "commercial-operations")'
echo
echo "     baseline statements before and after: $BEFORE / $AFTER (unchanged)"
echo
echo "Done. Backup of the replaced domain graphs: $OUT"
echo "In the KE Workbench: Model Editor (Ontology) › ⚙ › Reload."
read -n1 -r -p "Press any key to close." _
