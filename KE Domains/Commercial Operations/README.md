# Commercial Operations

The operational area that sells, markets, prices and cares for the organization's offerings and clients (D26). Built on Baseline Core v1.0; see `../README.md` for the hierarchy, naming and insulation rules.

| Folder | Asset names | IRIs |
|---|---|---|
| `commercial-operations/` | Commercial Operations Vocabulary, Taxonomy, Ontology, Shapes (0.4.0): what two or more of the area's domains share, and a taxonomy of its domains | `…/<kind>/commercial-operations/` |
| `sales/` | Domain Sales (0.4.0) | `…/<kind>/domain-sales/` |
| `sales/partner-and-channel/` | Domain Sales.Partner & Channel (0.2.0), an L2 domain of Sales | `…/<kind>/domain-sales.partner-and-channel/` |
| `marketing/` | Domain Marketing (0.2.0), including competitive intelligence | `…/<kind>/domain-marketing/` |
| `pricing/` | Domain Pricing (0.3.0), formerly Pricing and contracts | `…/<kind>/domain-pricing/` |
| `customer-care/` | Domain Customer Care (0.2.0), formerly Customer success | `…/<kind>/domain-customer-care/` |
| `sales/assembly/` | Sales assembly 0.5.0 and Sales value map 0.3.0 | `…/resource/domain-sales/…` |
| `sales/partner-and-channel/assembly/` | Domain Sales.Partner & Channel assembly 0.1.0 | `…/resource/domain-sales.partner-and-channel/…` |
| `marketing/assembly/`, `pricing/assembly/`, `customer-care/assembly/` | Domain Marketing, Pricing and Customer Care assemblies 0.1.0 | `…/resource/domain-<domain>/…` |
| `commercial-operations/assembly/` | The records and outside parties the domains share, and the PEO buyer persona graph 0.2.0 (part of the value map) | `…/resource/commercial-operations/…` |

Changes in 0.4.0 (2026-10-21):
- Legal moved to Business Operations. With it went the client service agreement, commercial agreement and clause, and the contract management steps, agreement terms and statuses that were in Pricing and contracts.
- Partner and channel became an L2 domain of Sales.
- The previous versions are in `../archive/superseded-0.4.0/`.

Some primitives shared well beyond this area, such as benefit, payroll, insurance, workers' compensation and claim, still live in the Commercial Operations vocabulary. Every area may cite them (D27). They will move to the HR Service Operations domain that owns each subject once those domains are built.

## Processes and services on APQC PCF 7.4 (D28)

Every domain's processes follow APQC: process group (L2) › process (L3) › activity (L4), with the activity's tasks (L5) as its steps. Each step carries a drafted SIPOCM, and each domain has its services. The content is authored in `../_build/apqc_commercial.py` and built by `../_build/build_assembly.py`; the report is `commercial-operations/assembly/assembly-report.md`.

| Domain | APQC elements it owns | Activities | Steps | Services |
|---|---|---:|---:|---:|
| Sales | 3.4 (but 3.4.2 and Finance's 3.4.3.2–5), 3.5 (but 3.5.2.4–5, 3.5.3.10, 3.5.5) | 41 | 56 + 7 earlier | 14 + 2 earlier |
| Sales.Partner & Channel | 3.2.3, 3.2.4, 3.4.2, 3.5.5 | 26 | 30 | 5 |
| Marketing | 3.1, 3.2 (but 3.2.2–4), 3.3 (but 3.3.3) | 54 | 56 | 11 |
| Pricing | 3.2.2, 3.3.3, 3.5.3.10 | 15 | 17 | 4 |
| Customer Care | 3.5.2.4, 3.5.2.5, 6.0 | 39 | 49 | 9 |

The workbook `sales/Sales Services and Processes.xlsx` (APQC 7.2.1) is superseded by the assemblies.
