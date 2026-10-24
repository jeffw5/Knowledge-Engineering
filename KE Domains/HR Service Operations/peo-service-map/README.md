# PEO Service Map

The external services of HR Service Operations, organized so every question a client persona asks can be traced to the service that answers it. Built by `../../_build/build_service_map.py`; shown in KE Workbench > Products & Services > PEO Service Map.

**Supply side: the service breakdown.** Human Resources Service Operations > L1 domain (the eight concepts of the area taxonomy) > L2 bounded context > L3 domain service. Each L3 service is also filed under the service line a client buys it in. L2 and L3 come from the business model extract in `Reference/hr-services-business-model/`; their IRIs follow D26 (`.../taxonomy/domain-<L1>.<L2>.<L3>/`) and are marked *planned* until the model is ingested (open question 27).

**Demand side: the questions.** Customer 360 persona > job to be done > job map stage > desired outcome. Each desired outcome becomes the question the persona asks ("Minimize the time required to X" becomes "How quickly can you help me X?") and is answered by the services that address it (`jtbd:isAddressedByService`). Each job also gives a headline question ("Can you help me ...?").

| File | What |
|---|---|
| `peo-service-map.json` | The map (also written to `KE Workbench/data/peo-service-map/peo-service-map.js`) |
| `coverage-report.md` | Questions with no service, services no question reaches, questions per persona |

Rebuild after changing the business model extract, the area taxonomy or the Customer 360 data: `python3 _build/build_service_map.py` from `KE Domains`. Status: Draft 0.1.0; nothing is loaded into GraphDB.
