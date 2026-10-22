# Domain Pricing

A domain of the Commercial Operations operational area. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the Commercial Operations ontology, never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).

The pricing ontology. It extends the core domain ontology and the Commercial Operations ontology with quotes for opportunities, and underwriting and its decisions, which consume the Commercial Operations census. Agreements and their clauses are in Domain Legal (Business Operations).

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-pricing-0.3.0.ttl` · `trig/vocabulary-domain-pricing-0.3.0.trig` | `https://www.insperity.com/vocabulary/domain-pricing/` | 150 |
| `ttl/taxonomy-domain-pricing-0.3.0.ttl` · `trig/taxonomy-domain-pricing-0.3.0.trig` | `https://www.insperity.com/taxonomy/domain-pricing/` | 495 |
| `ttl/ontology-domain-pricing-0.3.0.ttl` · `trig/ontology-domain-pricing-0.3.0.trig` | `https://www.insperity.com/ontology/domain-pricing/` | 93 |
| `ttl/shapes-domain-pricing-0.3.0.ttl` · `trig/shapes-domain-pricing-0.3.0.trig` | `https://www.insperity.com/shapes/domain-pricing/` | 70 |

Built from `KE Domains/_build/spec_pricing.py` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (10 primitives)

quote, price, fee, discount, underwriting, class code, experience modification factor, loss run, burden, percentage ⁺

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (29 concepts, 6 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Pricing component | `core:measure` | 8 |  |
| Pricing model | `core:directive` | 4 | `core-product/pricing-models-and-structures` |
| Quote | `pricing:quote` | 3 | `commercial-operations/proposal` |
| Underwriting input | `core:information-asset` | 4 |  |
| Underwriting outcome | `pricing:underwriting-decision` | 4 | `core-decision/eligibility-determination` |
| Pricing review | `core:process-step` | 0 | `core-services/contract-management` |

## Ontology (3 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `pricing:quote` | `core:information-asset` | core:concerns some commercialops:opportunity; core:hasComponent only core:measure |
| `pricing:underwriting` | `core:process` | core:hasStep some core:process-step; core:governedBy only core:directive |
| `pricing:underwriting-decision` | `core:decision` | core:consumes some core:information-asset; core:governedBy only core:directive |

## Shapes (2)

- `quote-shape` on `pricing:quote`: A shape that checks a quote names the opportunity it prices and is built from pricing components.
- `underwriting-decision-shape` on `pricing:underwriting-decision`: A shape that checks an underwriting decision names its inputs and the guideline that governs it.
