# Commercial Operations

The domain-specific vocabularies, taxonomies, ontologies and shapes of the Commercial Operations operational area of a professional employer organization, built on **Baseline Core v1.0** (`../../KE Baseline/Baseline Core v1.0`), which they read and never change.

Commercial Operations container and Sales 0.3.0, Pricing and contracts 0.2.0, other domains 0.1.1 · Draft · author Jeffrey Wallk · Semantic Governance: Services, Architecture & Integration v1.9 (Draft), Part III

## Structure

```
KE Domains/
  Commercial Operations/                 one folder per operational area
    commercial-operations/  ttl/ trig/   the container: what two or more domains share
                            assembly/    the PEO buyer persona graph, shared by every domain
    sales/                  ttl/ trig/
                            assembly/    process, step and service graphs, the manifest, and the assembly report
    marketing/              ttl/ trig/   includes competitive intelligence
    legal/                  ttl/ trig/   commercial and regulatory
    customer-success/       ttl/ trig/
    pricing-and-contracts/  ttl/ trig/
    partner-and-channel/    ttl/ trig/
    review/        design decisions, open questions, build report, concept links, promotion candidates, homonyms
    change-log/    PROV-O change records for the audit log (append-only)
    _build/        the domain specs and build_domains.py; the assembly spec and build_assembly.py
    archive/       superseded releases and GraphDB backups of replaced graphs
    graphdb-load.command
```

Each domain folder holds four assets, each in its own named graph:

| Asset | IRI pattern | Prefixes |
|---|---|---|
| `vocabulary-domain-<name>` | `https://www.insperity.com/vocabulary/domain-<name>/` | `salesvoc:` |
| `taxonomy-domain-<name>` | `https://www.insperity.com/taxonomy/domain-<name>/` | `salestax:` |
| `ontology-domain-<name>` | `https://www.insperity.com/ontology/domain-<name>/` | `sales:` |
| `shapes-domain-<name>` | `https://www.insperity.com/shapes/domain-<name>/` | `salesshp:` |

The ontology prefixes are `commercialops:`, `sales:`, `marketing:`, `legal:`, `customersuccess:`, `pricingcontracts:` and `partnerchannel:`.

## Contents

| Domain | Version | Primitives | Concepts | Classes | Relations | Shapes |
|---|---|---:|---:|---:|---:|---:|
| Commercial operations (container) | 0.3.0 | 38 | 55 | 10 | 3 | 5 |
| Sales | 0.3.0 | 13 | 59 | 4 | 0 | 3 |
| Marketing (incl. competitive intelligence) | 0.1.1 | 34 | 66 | 3 | 0 | 3 |
| Legal (commercial and regulatory) | 0.1.1 | 39 | 68 | 9 | 2 | 4 |
| Customer success | 0.1.1 | 13 | 50 | 4 | 0 | 3 |
| Pricing and contracts | 0.2.0 | 12 | 48 | 3 | 0 | 2 |
| Partner and channel | 0.1.1 | 9 | 36 | 2 | 0 | 2 |
| **Total** | | **158** | **382** | **35** | **5** | **22** |

9,827 triples in the domain assets, plus the assembly graphs (`sales/assembly/README.md`). Each domain's `README.md` lists its top concepts, classes, axioms and shapes.

## How the domains are insulated

1. **One folder and four named graphs per domain.** A domain is loaded, reloaded or rolled back on its own.
2. **Siblings never refer to each other.** A domain refers only to the core, the Commercial Operations container and itself. Anything two domains share (account, lead, opportunity, proposal, client service agreement, clause, competitor, worksite employee, sale, benefit, payroll, insurance, workers' compensation…) lives in the container. The build refuses a sibling reference, and the load script checks for one again in GraphDB.
3. **Pinned to a core version.** Each domain ontology imports the core and container ontologies by their ontology IRIs, so the KE Workbench resolves them, and records the versions it was built against with `dcterms:requires` (`…/ontology/core/0.1.0/`). A change to the core reaches a domain only when that domain is rebuilt against the new core and re-released.
4. **The baseline stays untouched.** Nothing here writes a core file or a core graph. Where a core taxonomy concept is formalized by a domain class (for example core "Statute" → `legal:statute`), the `core:formalizedBy` triple is stored in the domain's own ontology graph. The load script counts the baseline statements before and after the load and stops if they differ.

## Assembly

A domain is assembled from components (design decisions D17–D24). The vocabulary, taxonomy and ontology are the parts catalog and the joining rules. The components are instance graphs. The **service assembly** is Service › Process › Process step:
- a party graph of who takes part (the organization, its agents, and the roles of outside parties);
- step graphs, one per reusable step, each with its SIPOCM (supplier, input, process step, output, customer, measure);
- process graphs, one per process, which build it from steps with `core:hasStep` and `core:precedes`;
- service graphs, one per service, which join the processes that enable it (`core:supports`) and its delivery step (`core:deliveryOf`);
- a manifest listing the component versions that make a release.

The **value map** is a separate assembly: the buyer persona graph (jobs, job steps and desired outcomes, in the container) and a value-map graph that says which job steps each step addresses and what each service delivers today, with its own manifest.

The build validates both against the shapes and measures the service assembly (assembly index, copy number) and the value map (value gaps between desired and delivered outcomes). Sales is the first domain assembled, with two services; see `sales/assembly/README.md`.

## Load into GraphDB

Load Baseline Core v1.0 first, then double-click `graphdb-load.command`. You can also run it with a repository and domains: `./graphdb-load.command value-kb sales legal`. For each domain it loads, it:

1. backs up that domain's graphs to `archive/graphdb-backup-<time>/`;
2. clears and reloads only those graphs, and removes the domain's assembly graphs that the current release no longer has;
3. appends the change records to the audit log;
4. runs the checks: BFO lineage, `core:formalizedBy`, primitives, broad matches, assembly typing, sibling references and the baseline statement count.

Only the latest version of each asset is loaded, followed by the domain's assembly graphs.

The repository is never cleared. Then, in the KE Workbench, go to Model Editor (Ontology) › ⚙ › Reload.

## Rebuild

From this folder: `python3 _build/build_domains.py` (or `--only sales` to rewrite one domain), then `python3 _build/build_assembly.py` to rebuild, validate and measure the assembly. The build reads the core from `../../KE Baseline/Baseline Core v1.0/ttl` and the Part III checks and Turtle writer from `../../KE Workbench/ingest/ke_ingest.py`. It writes `ttl/` and `trig/` and refreshes `review/`, and it exits with an error if any rule fails. A rebuild overwrites hand edits to the generated files, so make lasting changes in the spec.

## Review before Candidate

See `review/open-questions.md`. In short: 20 general primitives are proposed for promotion to the core; the legal deontic classes are probably core material too; there are three sense collisions with core terms; and the definitions of law and regulation need review by counsel.
