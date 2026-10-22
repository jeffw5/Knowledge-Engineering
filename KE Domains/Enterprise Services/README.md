# Enterprise Services

`catalog/`: the enterprise service catalog 0.1.0, built by `../_build/build_catalog.py` (D25). Every operational area publishes its services here. A domain consumes another area's service only through its catalog entry, never by referring to that area's processes or resources (D27).

| Graph | Contents |
|---|---|
| `…/resource/enterprise-services/internal-portfolio/` | Internal domain services (department services, on the APQC PCF). Published so far: total cost of employment analysis and benefits comparison (Domain Sales, Sales assembly 0.4.0). |
| `…/resource/enterprise-services/external-portfolio/` | External services, following the HR Services & PEO Enterprise Business Model. Empty until the model is ingested into HR Service Operations. |
| `…/resource/enterprise-services/manifest/0.1.0/` | The catalog release. |

A portfolio lists its services with `dcterms:hasPart`; each service is defined by its domain's assembly. Enterprise services are composed from core terms and domain terms; the catalog has no vocabulary of its own.
