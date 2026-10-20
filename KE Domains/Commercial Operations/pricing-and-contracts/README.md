# Pricing and contracts

A domain of the Commercial Operations operational area. It refers only to the core (Baseline Core v1.0) and to the Commercial Operations container, never to a sibling domain, so it can change without affecting them.

The pricing and contracts ontology. It extends the core domain ontology and the Commercial Operations ontology with quotes for opportunities, and underwriting and its decisions, which consume the Commercial Operations census. Agreements are the Commercial Operations client service agreement and its clauses.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-pricing-and-contracts-0.2.0.ttl` · `trig/vocabulary-domain-pricing-and-contracts-0.2.0.trig` | `https://www.insperity.com/vocabulary/domain-pricing-and-contracts/` | 174 |
| `ttl/taxonomy-domain-pricing-and-contracts-0.2.0.ttl` · `trig/taxonomy-domain-pricing-and-contracts-0.2.0.trig` | `https://www.insperity.com/taxonomy/domain-pricing-and-contracts/` | 791 |
| `ttl/ontology-domain-pricing-and-contracts-0.2.0.ttl` · `trig/ontology-domain-pricing-and-contracts-0.2.0.trig` | `https://www.insperity.com/ontology/domain-pricing-and-contracts/` | 91 |
| `ttl/shapes-domain-pricing-and-contracts-0.2.0.ttl` · `trig/shapes-domain-pricing-and-contracts-0.2.0.trig` | `https://www.insperity.com/shapes/domain-pricing-and-contracts/` | 68 |

Built from `../_build/spec_pricing_and_contracts.py` by `../_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (12 primitives)

quote, price, fee, discount, underwriting, class code, experience modification factor, loss run, burden, term ⁼, signature, percentage ⁺

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (48 concepts, 8 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Pricing component | `core:measure` | 8 |  |
| Pricing model | `core:directive` | 4 | `core-product/pricing-models-and-structures` |
| Quote | `pricingcontracts:quote` | 3 | `domain-commercial-operations/proposal` |
| Underwriting input | `core:information-asset` | 4 |  |
| Underwriting outcome | `pricingcontracts:underwriting-decision` | 4 | `core-decision/eligibility-determination` |
| Contract management step | `core:process-step` | 9 | `core-services/contract-management` |
| Agreement term | `commercialops:clause` | 4 | `domain-commercial-operations/clause` |
| Agreement status | `core:lifecycle-status` | 4 |  |

## Ontology (3 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `pricingcontracts:quote` | `core:information-asset` | core:concerns some commercialops:opportunity; core:hasComponent only core:measure |
| `pricingcontracts:underwriting` | `core:process` | core:hasStep some core:process-step; core:governedBy only core:directive |
| `pricingcontracts:underwriting-decision` | `core:decision` | core:consumes some core:information-asset; core:governedBy only core:directive |

## Shapes (2)

- `quote-shape` on `pricingcontracts:quote`: A shape that checks a quote names the opportunity it prices and is built from pricing components.
- `underwriting-decision-shape` on `pricingcontracts:underwriting-decision`: A shape that checks an underwriting decision names its inputs and the guideline that governs it.
