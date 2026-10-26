# Persona, job, job step and desired outcome instances — Draft 0.4.0 (2026-10-26)

Instance set for the Customer 360 / PEO Outcome Benchmark, conforming to the
jobs-to-be-done ontology (`../00-jobs-to-be-done-ontology.ttl`) and Baseline Core v1.0
(`core:persona`, `core:job`, `core:job-step`, `core:desired-outcome` and the core shapes).

| File | Graph | Contents |
|---|---|---|
| 20-client-personas.ttl | …/outcome-benchmark/client-personas | 7 personas (P1–P7) |
| 21-jobs.ttl | …/outcome-benchmark/jobs | 26 functional jobs (22 core functional, 4 consumption chain) + 16 emotional jobs (E01–E16) |
| 22-job-map-steps.ttl | …/outcome-benchmark/job-map-steps (new) | 189 job map steps (e.g. J01-S01) |
| 23-desired-outcomes.ttl | …/outcome-benchmark/desired-outcomes | 224 desired outcomes (O001–O224) |

## What changed from 02 / 03 / 04
Every triple in the earlier files is kept; these files load into the same named graphs and replace them.

- **Job steps added.** Each functional job is broken into its own steps, worded in the executor's
  language, placed on one universal stage (`jtbd:isPlacedAtJobStep`), ordered (`jtbd:hasStepOrder`,
  `core:precedes`) and linked both ways to the job (`core:isStepOf` / `core:hasStep`).
  Steps and outcomes are intentionally not one-to-one: a step carries one or more outcomes, a stage can
  hold more than one step, and a stage with no outcomes has no step.
- **Outcomes mapped to job steps.** Each outcome now has `core:outcomeOf` and `jtbd:relatesToJobMapStep`
  to exactly one step, in the same stage as its existing `jtbd:occursAtJobStep`. This satisfies the
  core desired-outcome shape (min 1 `core:outcomeOf` to a job step), which the 0.3.0 set failed.
- **Emotional jobs as instances.** The 16 `jtbd:hasEmotionalJob` strings are now `jtbd:emotional-job`
  individuals executed by their persona. "Be seen as …" statements are typed emotional, not social,
  because job kinds are functional and emotional only. The strings stay on the personas for existing tools.
- **Personas** gain `core:performsJob` for every job they execute (explicit, so queries work without inference).
- New steps and emotional jobs carry `jtbd:hasEvidenceStatus evid:candidate` and `core:hasLifecycleStatus core:Draft`.

## Validation (2026-10-26)
Parsed and checked against the core shape rules: 0 errors. Every functional job has steps; every step belongs
to a job and has at least one desired outcome; every outcome is mapped to exactly one step of its own job and stage;
all inverses (executor/participant, step/job, outcome/step) agree; no dangling references.

Expected warnings:
- 16 × job shape: emotional jobs have no job steps yet. Elicit them in the Appreciative Inquiry interviews.
- 224 × desired-outcome shape: no `core:measuredBy` metric card yet. Targets need SME input.

## Load order
BFO, RO → Baseline Core v1.0 → 00 ontology → 05, 06, 11 vocabularies → 01 job map stages →
20 personas → 21 jobs → 22 job map steps → 23 desired outcomes.
