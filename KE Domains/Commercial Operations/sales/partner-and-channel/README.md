# Domain Sales.Partner & Channel

A domain of the Commercial Operations operational area, an L2 domain of Domain Sales. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the Commercial Operations ontology and its parent domains, never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).

The partner and channel ontology, an L2 domain of Domain Sales. It extends the core domain ontology, the Commercial Operations ontology and the Domain Sales ontology with the channel partner role borne by organizations and the partner programs that govern how partners refer, sell and are rewarded.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-sales.partner-and-channel-0.2.0.ttl` · `trig/vocabulary-domain-sales.partner-and-channel-0.2.0.trig` | `https://www.insperity.com/vocabulary/domain-sales.partner-and-channel/` | 134 |
| `ttl/taxonomy-domain-sales.partner-and-channel-0.2.0.ttl` · `trig/taxonomy-domain-sales.partner-and-channel-0.2.0.trig` | `https://www.insperity.com/taxonomy/domain-sales.partner-and-channel/` | 595 |
| `ttl/ontology-domain-sales.partner-and-channel-0.2.0.ttl` · `trig/ontology-domain-sales.partner-and-channel-0.2.0.trig` | `https://www.insperity.com/ontology/domain-sales.partner-and-channel/` | 64 |
| `ttl/shapes-domain-sales.partner-and-channel-0.2.0.ttl` · `trig/shapes-domain-sales.partner-and-channel-0.2.0.trig` | `https://www.insperity.com/shapes/domain-sales.partner-and-channel/` | 57 |

Built from `KE Domains/_build/spec_sales_partner_and_channel.py` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (9 primitives)

alliance, program ⁺, reseller, accountant, bank, franchise, association, marketplace, co-marketing

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (36 concepts, 7 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Channel partner type | `partnerchannel:channel-partner` | 9 | `core-role/partner` |
| Sales channel | `core:asset` | 4 |  |
| Partner program | `partnerchannel:partner-program` | 7 |  |
| Partner agreement | `core:directive` | 3 | `core-policy/contractual-instrument` |
| Partner attribution | `core:information-asset` | 2 | `commercial-operations/attribution` |
| Partner measure | `core:measure` | 3 | `core-measure/key-performance-indicator` |
| Technology integration | `core:capability` | 1 |  |

## Ontology (2 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `partnerchannel:channel-partner` | `core:role` | core:roleOf some core:organization |
| `partnerchannel:partner-program` | `core:directive` | core:governs some partnerchannel:channel-partner |

## Shapes (2)

- `channel-partner-shape` on `partnerchannel:channel-partner`: A shape that checks the channel partner role is borne by an organization.
- `partner-program-shape` on `partnerchannel:partner-program`: A shape that checks a partner program governs channel partners.
