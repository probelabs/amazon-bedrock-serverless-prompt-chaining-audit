# P12 dogfood — session mistakes as named checks

Binary: `/home/dev/src/proof-bin/proof` built from `/home/dev/src/reqproof` (`ddef8cf`+dirty).
Date: 2026-08-14. Loop: `proof audit --check` only (no `proof workflow`, no mute).

## Product correction

IAM `Action=* Resource=*` and untrusted template/HTML-to-PDF are **not**
obligatory project-specific audit checks. They are **reusable code-signal
rules** in Proof's Python signal pack (`builtin:python/default` /
`py.privilege.unconstrained_grant`, `py.template.untrusted_string_render`),
auto-selected when a repo has `.py` and `signals.defaults: auto`. The
reusable *gate* is `code_signal_obligations_reviewed` / `proof signals`,
not a default-on check named after AWS or WeasyPrint.

Do **not** judge this fixture via `proof audit --check iam_wildcard_policy_clean`
or `untrusted_renderer_clean`. Those ids are gone. Judge via the pack.

OpenGrep 1.22.0 + `builtin:python/default` on this tree:

- `pipeline/pipeline_stack.py:168` and `:287` → `py.privilege.unconstrained_grant`
- `functions/trip_planner/pdf_creator/index.py` → `py.template.untrusted_string_render`
- `stacks/util.py` and `stacks/trip_planner_stack.py` stay clean (WeasyPrint layer / `rm -rf weasyprint` are not sinks)

Catalog closure: unconstrained grant → `constrained_principal_scope_preserved`;
untrusted string render → `source_fragment_validated_before_composition`.

`hazard.required_checks` is only `spec_lint_hazard_consequence`.

Do not claim 0/0. Do not file KIs for this correction.

## What stays as named checks (general)

| Check | Session mistake | This fixture |
|---|---|---|
| `role_prompt_hygiene` | “EMPTY LIST IS A SUCCESS” / Max 3 / Prefer 0 | **pass** — 41 roles, no empty-is-win or finding-quota language |
| `code_predicates_modeled` (help + polarity) | missing help topic; CDK kwargs counted as decisions | **pass** — 17 implemented FRETish reqs; `indent=2` / `memory_size=256` ignored |
| `acceptance_witness_quality` | `:acceptance` on SYS/SW/INT tests | already implemented (prior turn) |
| history-mine on `onboard_v1` | history sweep was a chat step | bound: `problem_reports_reviewed`, `change_evidence_complete` |
| `required_checks` rewind | `verify: proof audit --check` does not rewind | process gate; see below |

## Checklist bind

Project `proof/checklists/definitions/onboard_v1.yaml` now uses `required_checks`
(not `verify: proof audit --check`). Soft `verify:` is only `test -f` / `test -d`.

`proof audit --check process_checklist` **rewound `variables`** and invalidated
dependents because:

- `variable_drift`: 20 `stale_in_list` (domain vars listed on reqs, not in FRETish)
- `variables_declared`: SYS-REQ-006 guarantee conjunct
  `not (deploy_actions_are_star and deploy_resources_are_star)` is input-only
  (environment fact, not a component-chosen output)

That rewind is still general. It is the intended fail-closed stamp. Do not
confirm `variables` until those two checks are honestly green. Do not file a
KI for the rewind.

## What the signal pack would have caught earlier

A fresh clone of this sample with `.py` and `signals.defaults: auto` would
surface unconstrained IAM grants and untrusted HTML-to-PDF via
`builtin:python/default` (`py.privilege.unconstrained_grant`,
`py.template.untrusted_string_render`) and the
`code_signal_obligations_reviewed` gate after the engine lands — no Codex
scan, no hazard-sweep, and no AWS/WeasyPrint-named obligatory check.
