# Removed from the baseline, 2026-10-21

An Ingestion run on 2026-10-20 at 13:29 UTC wrote the old Sales 0.1.0 assets (vocabulary, taxonomy, ontology and shapes), its change record and its ingestion report into `KE Baseline/Baseline Core v1.0/`. They are not core content: the Sales domain lives in `KE Domains/Commercial Operations/sales/` (now 0.4.0). They were moved here, at Jeffrey Wallk's request, so that the baseline holds only core files again. Nothing was deleted.

If that run also loaded them into GraphDB, they occupy the Sales graphs (…/vocabulary|taxonomy|ontology|shapes/domain-sales/). `KE Domains/graphdb-load.command` replaces those graphs with Sales 0.4.0. The change record stays in the audit log graph, which is append-only.
