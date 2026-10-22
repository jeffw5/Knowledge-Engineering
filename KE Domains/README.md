# KE Domains

The domain-specific vocabularies, taxonomies, ontologies and shapes of the enterprise, organized by operational area. They are built on **Baseline Core v1.0** (`../KE Baseline/Baseline Core v1.0`), which they read and never change. Design decisions D1–D29 are in `review/design-decisions.md`.

Draft · author Jeffrey Wallk · Semantic Governance: Services, Architecture & Integration v1.9 (Draft), Part III

## Structure

```
KE Domains/
  Commercial Operations/          Sales (with its L2 Partner & Channel), Marketing, Pricing, Customer Care
    commercial-operations/        the area's shared assets
    sales/  sales/partner-and-channel/  marketing/  pricing/  customer-care/
    <domain>/assembly/            each domain's assembly on APQC PCF 7.4; sales/assembly also holds the Sales value map
  Business Operations/            Finance, Accounting, HR, Billing & AR, Compliance, Legal, Security
    business-operations/  legal/
  HR Service Operations/          the eight L1 domains of the HR Services & PEO Enterprise Business Model
    hr-service-operations/
  Technical Operations/           Business Systems, AI Strategy & Enterprise Analytics, Platform, Data Engineering,
    technical-operations/         Knowledge Engineering and Cybersecurity Services
  Reference/apqc-pcf/             APQC Process Classification Framework reference registry (read only)
  Enterprise Services/catalog/    the enterprise service catalog: internal and external portfolios
  _build/                         specs and builders
  review/                         design decisions, open questions, build reports
  change-log/                     change records for the audit log
  archive/                        superseded versions and GraphDB backups
  graphdb-load.command            loads everything above into GraphDB
```

Each folder that holds assets has `ttl/` and `trig/` subfolders and a `README.md`.

## Hierarchy and naming (D25–D27)

- **Levels.** Enterprise › Operational area › Domain (L1, with L2 and L3 below it) › services and processes.
- **Names.** An asset's name is a first qualifier followed by a second one:
  - first qualifier: *Core*, *Domain L1.L2.L3* or the operational area's name;
  - second qualifier: Vocabulary, Taxonomy or Ontology (or Shapes).
  - For example: "Commercial Operations Ontology", "Domain Sales Taxonomy", "Domain Sales.Partner & Channel Vocabulary".
- **IRIs.**
  - Area assets live at `…/<kind>/<area>/`, for example `…/ontology/commercial-operations/`.
  - Domain assets live at `…/<kind>/domain-<L1>[.<L2>[.<L3>]]/`, with the levels joined by dots, for example `…/taxonomy/domain-sales.partner-and-channel/`.
- **Insulation (D27).**
  - A domain's classes, relations, concepts and imports refer only to:
    - the core;
    - its operational area's shared assets;
    - its parent domains;
    - itself;
    - the APQC reference registry.
  - Vocabulary primitives may be cited from any domain in any area (`dcterms:subject`, `core:hasPrimaryTerm`), never copied.
  - Classes and instances from different areas are combined only in enterprise services.
- **Two service portfolios (D25).**
  - **Internal domain services** are department services. They are built on the APQC PCF, which is loaded once as a reference registry with one owner domain per process.
  - **External services** are the services clients and worksite employees receive. They follow the HR Services & PEO Enterprise Business Model.
  - Both portfolios are published in the enterprise service catalog. A domain consumes another area's service only through the catalog.

## Contents

| Operational area | Area or domain | Version | Primitives | Concepts | Classes | Relations | Shapes |
|---|---|---|---:|---:|---:|---:|---:|
| Commercial Operations | Commercial Operations | 0.4.0 | 38 | 58 | 8 | 3 | 4 |
| | Domain Sales | 0.4.0 | 13 | 59 | 4 | 0 | 3 |
| | Domain Sales.Partner & Channel | 0.2.0 | 9 | 36 | 2 | 0 | 2 |
| | Domain Marketing | 0.2.0 | 34 | 66 | 3 | 0 | 3 |
| | Domain Pricing | 0.3.0 | 10 | 29 | 3 | 0 | 2 |
| | Domain Customer Care | 0.2.0 | 13 | 50 | 4 | 0 | 3 |
| Business Operations | Business Operations | 0.1.0 | 3 | 8 | 0 | 0 | 0 |
| | Domain Legal | 0.2.0 | 42 | 90 | 11 | 2 | 5 |
| Human Resources Service Operations | Human Resources Service Operations | 0.1.0 | 10 | 9 | 0 | 0 | 0 |
| Technical Operations | Technical Operations | 0.1.0 | 3 | 7 | 0 | 0 | 0 |

Also included:
- the APQC PCF reference registry 0.2.0 (PCF 7.4, categories 3.0 and 6.0, 309 elements);
- the enterprise service catalog 0.1.0, with 2 internal services published;
- the Commercial Operations domain assemblies on APQC PCF 7.4: Sales 0.5.0 (with the Sales value map 0.3.0), Marketing, Pricing, Customer Care and Sales.Partner & Channel 0.1.0 (`Commercial Operations/README.md`, D28).

The areas other than Commercial Operations have their shared assets and a taxonomy of their domains so far. Domain Legal has moved into Business Operations. The other domains are built as each area is modeled; HR Service Operations starts from the business model.

## Build

From this folder:

```
python3 _build/build_domains.py        # areas and domains (add --only <key> to rewrite one)
python3 _build/build_reference.py      # APQC PCF reference registry
python3 _build/build_assembly.py       # Commercial Operations assemblies and the Sales value map: build, validate, measure
python3 _build/build_catalog.py        # enterprise service catalog
./graphdb-load.command [repository]    # load everything into GraphDB (default value-kb)
```

The builds read the core from `../KE Baseline/Baseline Core v1.0/ttl`, taking only its core files. They take the Part III checks and the Turtle writer from `../KE Workbench/ingest/ke_ingest.py`, and exit with an error if any rule fails. A rebuild overwrites hand edits to generated files, so make lasting changes in the specs, or in GraphDB once editing moves there (D23).

`graphdb-load.command` works in five steps:
1. Backs up every managed graph it will replace or remove.
2. Loads the latest version of each asset, then the assemblies, the registry and the catalog.
3. Removes managed graphs the release no longer has, such as the retired `…/domain-customer-success/`.
4. Appends the change records.
5. Runs the checks, and stops if the baseline statement count changes.
