#!/usr/bin/env python3
"""Export each vocabulary and taxonomy named graph from a GraphDB repository
to its own file, named {type}-{tier}-{name}-{version}.{trig|ttl}.

Only explicit (authored) statements are exported (infer=false), per
Semantic Governance v1.9, Section 3.3: inferred statements are never promoted.

Usage:
  python3 graphdb_export.py [--repo REPO_ID] [--server http://localhost:7200]
                            [--out ./export] [--types vocabulary taxonomy]
                            [--format trig|ttl] [--user U --password P]
Standard library only.
"""
import argparse
import base64
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

FORMATS = {"trig": "application/x-trig", "ttl": "text/turtle"}


def request(url, accept, auth=None, data=None, content_type=None):
    req = urllib.request.Request(url, data=data)
    req.add_header("Accept", accept)
    if content_type:
        req.add_header("Content-Type", content_type)
    if auth:
        req.add_header("Authorization", "Basic " + auth)
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def sparql(base, repo, query, auth):
    body = urllib.parse.urlencode({"query": query}).encode()
    raw = request(f"{base}/repositories/{repo}", "application/sparql-results+json",
                  auth, body, "application/x-www-form-urlencoded")
    return json.loads(raw)["results"]["bindings"]


def size(base, repo, context, auth):
    ctx = urllib.parse.quote(context, safe="")
    return int(request(f"{base}/repositories/{repo}/size?context={ctx}", "text/plain", auth))


def asset_name(iri):
    """https://www.insperity.com/taxonomy/core-process/ -> taxonomy-core-process"""
    path = urllib.parse.urlparse(iri).path.strip("/")
    parts = [p for p in path.split("/") if p and p != "graph"]
    # drop a trailing version segment such as 0.1.0
    if parts and re.fullmatch(r"\d+\.\d+\.\d+", parts[-1]):
        parts = parts[:-1]
    return re.sub(r"[^A-Za-z0-9._-]+", "-", "-".join(parts)).strip("-") or "unnamed"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="GraphDB repository id (optional if the server has only one)")
    ap.add_argument("--server", default="http://localhost:7200")
    ap.add_argument("--out", default="./export")
    ap.add_argument("--types", nargs="+", default=["vocabulary", "taxonomy"],
                    help="first IRI path segments to export: vocabulary taxonomy ontology shapes")
    ap.add_argument("--format", choices=FORMATS, default="trig")
    ap.add_argument("--user")
    ap.add_argument("--password")
    a = ap.parse_args()

    base = a.server.rstrip("/")
    auth = base64.b64encode(f"{a.user}:{a.password}".encode()).decode() if a.user else None
    out = pathlib.Path(a.out)

    # Pick the repository automatically when none is given
    if not a.repo:
        repos = [r["id"] for r in json.loads(request(f"{base}/rest/repositories", "application/json", auth))]
        if len(repos) == 1:
            a.repo = repos[0]
            print(f"Using repository: {a.repo}")
        else:
            sys.exit("Repositories on this server: " + ", ".join(repos or ["(none)"])
                     + "\nRun again with --repo NAME, using one of the names above.")
    out.mkdir(parents=True, exist_ok=True)

    # 1. List named graphs
    raw = request(f"{base}/repositories/{a.repo}/contexts", "application/sparql-results+json", auth)
    graphs = [b["contextID"]["value"] for b in json.loads(raw)["results"]["bindings"]
              if b["contextID"]["type"] == "uri"]

    def wanted(g):
        segs = [s for s in urllib.parse.urlparse(g).path.strip("/").split("/") if s]
        if segs and segs[0] == "graph":          # guide pattern /graph/{artifact-type}/...
            segs = segs[1:]
        return bool(segs) and segs[0] in a.types

    selected = sorted(g for g in graphs if wanted(g))
    print(f"{len(graphs)} named graphs; exporting {len(selected)} ({', '.join(a.types)})\n")

    # Default-graph check: these statements belong to no asset and are not exported
    default_count = size(base, a.repo, "null", auth)
    if default_count:
        print(f"WARNING: {default_count} statements are in the default graph and will not be exported.\n")

    used = set()
    for g in selected:
        # 2. Header: the scheme or ontology in this graph, its version and identifier
        rows = sparql(base, a.repo, f"""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX owl:  <http://www.w3.org/2002/07/owl#>
            PREFIX dct:  <http://purl.org/dc/terms/>
            SELECT ?s ?v ?id WHERE {{ GRAPH <{g}> {{
              VALUES ?t {{ skos:ConceptScheme owl:Ontology }}
              ?s a ?t .
              OPTIONAL {{ ?s owl:versionInfo ?v }}
              OPTIONAL {{ ?s dct:identifier ?id }}
            }} }}""", auth)
        heads = {r["s"]["value"] for r in rows}
        if len(heads) > 1:
            print(f"WARNING: {g} holds {len(heads)} schemes/ontologies (guide: one per file): "
                  + ", ".join(sorted(heads)))
        head = rows[0] if rows else {}
        version = head.get("v", {}).get("value", "unversioned")
        name = head.get("id", {}).get("value") or asset_name(head.get("s", {}).get("value", g))
        if version == "unversioned":
            print(f"WARNING: {g} has no owl:versionInfo")

        # 3. Export explicit statements only
        ctx = urllib.parse.quote(f"<{g}>", safe="")
        data = request(f"{base}/repositories/{a.repo}/statements?context={ctx}&infer=false",
                       FORMATS[a.format], auth)

        fname = f"{name}-{version}.{a.format}"
        n = 2
        while fname in used:                     # never overwrite within one run
            fname = f"{name}-{version}-{n}.{a.format}"
            n += 1
        used.add(fname)
        (out / fname).write_bytes(data)
        print(f"{fname:60s} {size(base, a.repo, f'<{g}>', auth):>7} statements  <- {g}")

    print(f"\nDone: {len(selected)} files in {out.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        sys.exit(f"GraphDB returned {e.code}: {e.read().decode(errors='replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach GraphDB: {e.reason}")
