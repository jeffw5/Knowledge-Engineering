# Review decisions (training data for the ingestion agents)

`dispositions.jsonl` holds one JSON object per line, appended by Conformance Review whenever a reviewer disposes of a finding. The file is append-only. If a term has several records, the latest one wins.

| Field | Meaning |
|---|---|
| `schema` | `ke-disposition/1` |
| `id`, `at`, `by` | record id, UTC time, reviewer (the configured author) |
| `disposition` | `fix` · `accept` (an exception: the term is meant to be this way) · `not-an-issue` (the rule fired wrongly) · `defer` · `escalate` (needs a modeling decision) |
| `rationale` | why: what the agents should learn |
| `term` | `iri`, `label`, `kind`, `definition`, `primaryTerm`, and `context` (broader term and its definition, narrower terms, siblings, alternative labels, scheme): what the agent saw |
| `findings` | the findings on the term: `rule` (Conformance Review rule id), `severity`, `title`, `detail` |
| `suggested` | what the tool proposed, if anything (`kind`, `target`, `text`), so acceptance and rejection of suggestions can be measured |
| `actions` | for `fix`: the changes saved (`type` label/definition/description/link/addVocab/formalize/rename/remove/removeAlt/unlink, with `old`/`new`/`target`…). For a definition written by Claude and then edited, `generatedDraft` and `generatedBy` keep the draft. |
| `source` | `mode` (files or graphdb), `model`, `modelTitle`, `file`, `repository` |

How ingestion uses it (`ke_ingest.py`; to switch it off, set `"learnFromReview": false` in the configuration):

- **Fixes are replayed.** When the same term is ingested again with the value the reviewer replaced, the correction is applied again: label, definition, description, vocabulary link, formalized by. For a vocabulary link or formalized-by decision, a concept with the same label in another taxonomy also counts as the same term. The ingestion report lists these under *Applied from review decisions*.
- **Accepted findings stay accepted.** Findings marked accept or not-an-issue are reported as information, with the rationale.
- **The definition writer learns.** Claude is shown up to `definitionExamples` (default 12) recent definitions reviewers approved, corrected drafts first, with the rejected draft and the reviewer's note.
- **Records for review.** Deferred and escalated items are not acted on automatically. They are the open modeling questions, and they are part of the training set.
