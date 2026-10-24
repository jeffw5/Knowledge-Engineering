# HR Services & PEO Enterprise Business Model (extract)

`business-model-structure.json` holds the structure of Jeffrey Wallk's HR Services & PEO Enterprise Business Model as it was extracted for the PEO Outcome Benchmark on 2026-10-22: 11 service lines (9 from the model, 2 added for the benchmark), 8 L1 domains, 17 L2 bounded contexts and 74 L3 domain services, with their business-model identifiers (`http://example.org/hrservices/ddd#`).

It is read by `_build/build_service_map.py` to build the PEO Service Map. It is an extract, not the model: the 148 business processes and the supporting operations are not in it. When the model is ingested into HR Service Operations (open question 27), the builder should read the ingested L2 and L3 domains instead.
