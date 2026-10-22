# Partner and channel

A domain of the Commercial Operations operational area. It refers only to the core (Baseline Core v1.0) and to the Commercial Operations container, never to a sibling domain, so it can change without affecting them.

The partner and channel ontology. It extends the core domain ontology and the Commercial Operations ontology with the channel partner role borne by organizations and the partner programs that govern how partners refer, sell and are rewarded.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-partner-and-channel-0.1.1.ttl` · `trig/vocabulary-domain-partner-and-channel-0.1.1.trig` | `https://www.insperity.com/vocabulary/domain-partner-and-channel/` | 132 |
| `ttl/taxonomy-domain-partner-and-channel-0.1.1.ttl` · `trig/taxonomy-domain-partner-and-channel-0.1.1.trig` | `https://www.insperity.com/taxonomy/domain-partner-and-channel/` | 593 |
| `ttl/ontology-domain-partner-and-channel-0.1.1.ttl` · `trig/ontology-domain-partner-and-channel-0.1.1.trig` | `https://www.insperity.com/ontology/domain-partner-and-channel/` | 60 |
| `ttl/shapes-domain-partner-and-channel-0.1.1.ttl` · `trig/shapes-domain-partner-and-channel-0.1.1.trig` | `https://www.insperity.com/shapes/domain-partner-and-channel/` | 55 |

Built from `../_build/spec_partner_and_channel.py` by `../_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (9 primitives)

alliance, program ⁺, reseller, accountant, bank, franchise, association, marketplace, co-marketing

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (36 concepts, 7 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Channel partner type | `partnerchannel:channel-partner` | 9 | `core-role/partner` |
| Sales channel | `core:asset` | 4 |  |
| Partner program | `partnerchannel:partner-program` | 7 |  |
| Partner agreement | `core:directive` | 3 | `domain-commercial-operations/commercial-agreement` |
| Partner attribution | `core:information-asset` | 2 | `domain-commercial-operations/attribution` |
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
