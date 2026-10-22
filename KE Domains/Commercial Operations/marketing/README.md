# Domain Marketing

A domain of the Commercial Operations operational area. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the Commercial Operations ontology, never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).

The marketing ontology. It extends the core domain ontology and the Commercial Operations ontology with marketing campaigns and with competitive intelligence and battlecards as sourced information assets about competitors and markets.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-marketing-0.2.0.ttl` · `trig/vocabulary-domain-marketing-0.2.0.trig` | `https://www.insperity.com/vocabulary/domain-marketing/` | 452 |
| `ttl/taxonomy-domain-marketing-0.2.0.ttl` · `trig/taxonomy-domain-marketing-0.2.0.trig` | `https://www.insperity.com/taxonomy/domain-marketing/` | 1052 |
| `ttl/ontology-domain-marketing-0.2.0.ttl` · `trig/ontology-domain-marketing-0.2.0.trig` | `https://www.insperity.com/ontology/domain-marketing/` | 88 |
| `ttl/shapes-domain-marketing-0.2.0.ttl` · `trig/shapes-domain-marketing-0.2.0.trig` | `https://www.insperity.com/shapes/domain-marketing/` | 83 |

Built from `KE Domains/_build/spec_marketing.py` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (34 primitives)

campaign, audience, funnel, awareness, positioning, demand ⁺, generation ⁺, touchpoint, impression, nurturing, intent, firmographics, research ⁺, case study, public relations, social media, search engine optimization, webinar, trade show, email ⁺, profile ⁺, intelligence, battlecard, landscape, differentiator, strength ⁺, weakness ⁺, threat ⁺, alternative, status quo, displacement, share ⁺, interview ⁺, strengths, weaknesses, opportunities and threats analysis

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (66 concepts, 13 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Marketing campaign | `marketing:campaign` | 5 | `core-services/campaign-management` |
| Marketing channel | `core:asset` | 8 |  |
| Marketing content | `core:information-asset` | 3 |  |
| Audience definition | `core:information-asset` | 2 |  |
| Marketing signal | `core:information-asset` | 2 | `commercial-operations/commercial-signal` |
| Buyer persona | `core:persona` | 0 | `core-persona/persona` |
| Funnel stage | `core:lifecycle-status` | 5 |  |
| Marketing measure | `core:measure` | 6 | `core-measure/key-performance-indicator` |
| Competitive intelligence | `marketing:intelligence` | 5 | `core-services/competitive-analysis` |
| Competitive intelligence activity | `core:process-step` | 5 | `core-services/competitive-analysis` |
| Competitive alternative | `commercialops:competitor` | 6 | `commercial-operations/competitor` |
| Competitive insight | `marketing:intelligence` | 4 |  |
| Competitive outcome | `core:event` | 2 |  |

## Ontology (3 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `marketing:campaign` | `core:process` | core:hasStep some core:process-step; core:measuredBy only core:measure; core:governedBy only core:directive |
| `marketing:intelligence` | `core:information-asset` | core:concerns some core:party |
| `marketing:battlecard` | `marketing:intelligence` | core:concerns some core:organization |

## Shapes (3)

- `campaign-shape` on `marketing:campaign`: A shape that checks a campaign is broken into steps and is measured.
- `intelligence-shape` on `marketing:intelligence`: A shape that checks competitive intelligence names what it is about and cites its source.
- `battlecard-shape` on `marketing:battlecard`: A shape that checks a battlecard names the competitor organization it positions against.
