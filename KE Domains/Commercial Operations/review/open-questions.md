# Open questions (Commercial Operations 0.1.0)

These need a decision before the domains move from Draft to Candidate. None of them blocks loading the Draft.

## Core release decisions (the baseline was not changed)

1. **Promote 18 general primitives to the core?** They are listed in `promotion-candidates.csv`: analysis, industry, stage, cycle, demand, generation, research, email, profile, strength, weakness, threat, share, interview, certification, milestone, percentage, program. Each is general rather than commercial; it lives in a domain only because the core lacks it. Promoting them is a core release; the domains would then be rebuilt to point at the core terms.
2. **Promote the deontic norm classes?** `legal:norm`, `legal:obligation`, `legal:permission`, `legal:prohibition`, `legal:right`, plus `legal:statute`, `legal:regulation` and `legal:provision`. They formalize concepts that the core taxonomy already holds (core-policy "Norm", "Statute"…), and organizational policies need them as much as law does. They probably belong in the core ontology.
3. **Sense collisions with core terms.**
   - *conversion*: the container's commercial sense (lead → opportunity → client) against core-logic "conversion" (unit or format). Declared a homonym. You could rename the core term "unit conversion".
   - *plan*: core-product "plan" covers only the benefit, retirement or insurance plan. Sales and account plans are therefore built on core-process "planning". Does the core need a general plan (a directive)?
   - *term*: the pricing and contracts sense, an agreement's period, against core-rules "terms", the concepts of a fact type.
4. **Core polymorphic leftovers.** core-services "sales account" duplicates the container primitive *account*, and "campaign management", "competitive analysis" and "customer segmentation" are polymorphic terms built on primitives that now exist (campaign, analysis, segment). Relink them in the next core clean-up.
5. **core-domain vocabulary.** "Commercial" has customer support, marketing and sales as narrower terms, and "Legal" sits under Corporate. Customer success maps to customer support, and pricing and contracts and partner and channel map to Commercial. Should the core-domain vocabulary gain customer success, pricing and contracts, and partner and channel, and should Legal be shared with a future Corporate area?

## Modeling decisions

6. **D5: core concepts formalized from domain graphs.** Is storing `core:formalizedBy` triples for core concepts in domain graphs acceptable, or should those links wait for a core release? The baseline lineage check is unaffected either way.
7. **Legal hosted in Commercial Operations.** Legal here is scoped to commercial and regulatory law as it bears on selling and contracting. If a Corporate operational area is built, does Legal move there, with Commercial Operations keeping only contract provisions?
8. **State law.** Professional employer organization registration, workers' compensation and unemployment insurance law vary by state. They are modeled as bodies of law with `legal:hasJurisdiction`; no per-state statutes are instantiated yet.
9. **Selling stages.** The six stages follow Baseline decision 18 (Discover, Qualify, Evaluate, Propose, Decide, Onboard). The Onboard stage ends at the client handoff, and customer success onboarding takes over. Confirm this split.

## Content review

10. **Counsel review.** The definitions of the federal statutes, certified professional employer organization status, multiple employer welfare arrangements and multiple employer plans were drafted from general knowledge. They need review by counsel before they are used to derive rules.
11. **The organization's own names.** Offerings, team roles and key measures use generic industry terms (for example "Client success manager" and "Paid worksite employees"). Add the organization's own names as alternative labels.
12. **Label words not covered by a primitive.** `concept-links.csv` lists 66 such concepts in the `unmatched_words` column. Most are inflections or modifiers (qualified, won, sourced, regulatory). A few may hide a missing primitive (credential, duty, arrangement, listing, insight, attainment).
13. **Shapes not yet run.** The 20 shapes parse and load, but they have not been executed against instance data, and the load script has not yet been run against your GraphDB.

## Assembly (Sales 0.2.0)

14. **Names for the component tiers.** You've ruled out "module", so the instance graphs are called persona graph, process graph, step graph, service graph and manifest for now. Keep these names or choose your own?
15. **Standard steps or occurrences (D18).** Model execution as occurrences that realize the standard steps, which strict BFO calls for, or keep standard instances only until execution data is captured?
16. **Two core shape findings** (warnings only; the baseline was not changed):
    - Core `process-shape` targets `core:process`, so it also fires on every process step. It probably wants to exclude steps.
    - Core `asset-shape` expects a lifecycle on every asset, which here includes graph headers and records. Should standard instances carry lifecycles, or should the shape exempt them?
17. **Direction of an outcome.** Minimize and maximize are recorded as notes on desired outcomes. Should they be core primitives (core-measure has "reduction" but not these)?
18. **Buyer persona in the container.** The "Buyer persona" concept is in the marketing taxonomy, but the persona graph (container) and sales both need it, so under D2 it belongs in the container.
19. **Job study data.** The job study records job kinds as "Related financial job", "Related social job" and "Related emotional/risk job". These are mapped to functional or emotional with a finance subject where relevant (Baseline 20). Also, outcome CA-J2.2.3 says "Maximize the accuracy" but its direction is minimize (of % variance). Please confirm both.
20. **Next services.** 24 more services in *Sales Services and Processes.xlsx* are ready to be assembled the same way. Census collection is already shared; the quote and signature steps will need the container moves listed in item 3.

## Service › Process › Process step (Sales 0.3.0)

21. **Supplier and customer relations.** `has supplier` and `has customer` sit in the Commercial Operations container under RO *has participant*, as candidates for the core. Promote them, keep them in the container, or prefer another parent?
22. **New steps and measures.** Census collection is now two steps (census request, census validation), and benefits plan analysis adds current benefits collection. Each step has one provider measure (for example census turnaround time, plan document completeness). Please confirm the steps, the measures and their units; none has a measured value yet.
23. **Step measures and metric cards.** The value map compares delivered outcomes with desired outcomes on the persona metric cards. Should it also state which step measure feeds each metric card (for example census validation failure rate → census-pass v1.0)?
24. **Sales 0.1.0 in the baseline folder again.** An Ingestion run at 13:29 UTC today (change record 2026-10-20T132911Z) wrote `vocabulary-, taxonomy-, ontology- and shapes-domain-sales-0.1.0.ttl` and a change record into `KE Baseline/Baseline Core v1.0/ttl/`. The builds now ignore anything in that folder that is not a core file, but the files and any GraphDB graphs that run loaded should probably be removed.

