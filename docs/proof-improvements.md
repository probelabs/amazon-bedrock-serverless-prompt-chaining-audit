# ReqProof improvement plan

This is a product plan for **ReqProof** (`proof`), not a rewrite of the Bedrock
prompt-chaining sample. The sample at `/workspace` is the **dogfood fixture**:
every change below must be shown red or green by `proof audit` (or a named
`proof audit --check …`) on this tree.

**Do not dogfood with `proof workflow`.** That command is a second spine
(spec → implement → verify → document). It is too coarse, it can
`advance --force`, and it is not the loop we want agents to learn. The
deterministic loop is:

```bash
proof audit
proof audit --check <check-id>
proof checklist show onboard_v1
proof checklist confirm --id <step> --note "…"
proof checklist reset --id <step> --invalidate-dependents
```

Role prompts may still say “run the onboard role,” but the **machine gate**
is always `proof audit`.

## KnownIssue usage (product only)

A **KnownIssue** records a **product** defect or a confirmed failure mode in
the shipped sample (handler, stack, client). It is **not** a bucket for
ReqProof process debt.

Do **not** file a KI for:

- missing `// MCDC` / `# MCDC` row comments (`mcdc_coverage`)
- missing obligation triples or integration/acceptance witnesses
- checklist stamps, `process_checklist`, onboard incomplete
- untraced pytest helpers that are not product code
- “audit is not green” as such

Those stay as **audit warnings**, `witness_deferred` / obligation deferrals
(when the CLI requires a tracker id, that tracker must still describe the
*product* hole, not the check), or engine work in this document.

This repo already has several KIs that violate that rule
(`KI-accept-*`, `KI-obligation-evidence-gaps`, `KI-spec-mcdc-row-witnesses`,
`KI-untraced-test-harness`). They were filed to make leftover audit IDs
look “mapped.” That was incorrect. They are process/evidence gaps, not
product bugs. Treat them as to-withdraw when a human wants the ledger
cleaned; do not add more of that shape.

A KI that *can* be product-shaped: a real branch in shipped code that
tests do not drive (for example incomplete polarities in `stacks/util.py`)
— only if the code’s behavior is wrong or untested on a user path, not
because an audit row is red.

## Status ledger (dogfood on this repo)

Statuses: **done** = engine change landed in rebuilt `/home/dev/src/proof-bin/proof` from `/home/dev/src/reqproof` (`ddef8cf`+dirty).

| Item | Status | Judge command | Observation |
|---|---|---|---|
| P0 checklist↔audit bind | **done** | `proof audit --check process_checklist`; `proof checklist check onboard_v1` | **pass**. `process_checklist: OK — onboard_v1 complete (11 confirmed, 0 skipped, 3 not-applicable)`; `checklist onboard_v1: OK` exit 0. Dual `proof audit` `{SCRATCH}/audit-1.txt` / `{SCRATCH}/audit-2.txt`. |
| P1 under_modeled | **done** | `proof audit --check under_modeled_requirements_clean` | **pass**. “no requirements look under-modeled relative to current tests or implementation.” |
| P2 solver_modeling_opportunity | **done** | `proof audit --check solver_modeling_opportunity` | **pass**. “27 formalized requirements evaluated, 8 carried enumerable-domain signals, all with modeled or waived domains (0 waived, 0 suppressed by bool-only gate).” |
| P3 nonbool_inputs_constrained | **done** | `proof audit --check nonbool_inputs_constrained` | **pass**. “all 11 non-bool input/mode variables across 23 formalized components carry a domain model.” Engine 0-int polarity still present; this fixture now declares ints so the check is exercising ranges, not the empty-int pass. |
| P4 spec_lint_formalization_quality | **done** | `proof audit --check spec_lint_formalization_quality` | **pass**. “lint-formalization-quality: no issues found.” |
| P5 spec_lint_decomposition_adds_refinement | **done** | `proof audit --check spec_lint_decomposition_adds_refinement` | **pass**. “lint-decomposition-adds-refinement: no issues found.” SYS-REQ-003 `temperature_settings_count` now covered by SW-REQ-003. |
| P6 software_formalization_complete | **done** | `proof audit --check software_formalization_complete --check interface_formalization_complete` | **pass**. “all 10 review or approved guarantee requirement(s) in 1 configured lower formal-layer spec(s) have a non-envelope FRETish formalization”; “all 7 … cross-component spec(s)” likewise. |
| P7 spec_conformance predicates | **done** | `proof audit --check spec_lint_spec_conformance_review_grounded` | **pass**. “lint-spec-conformance-review-grounded: no issues found.” |
| P8 code_predicates_modeled | **done** | `proof audit --check code_predicates_modeled` | **pass**. “all load-bearing code predicates on 17 implemented FRETish requirement(s) are modeled or explicitly not_modeled (15 empty-decision mutex leaf/leaves).” |
| P9 onboard/spec-review prompts | **done** | `proof role show onboard --format agent`; grep builtin `{onboard,spec-review,formal-proof}.md` | **pass**. Role text: machine gate is `proof audit`; do not run `proof workflow`. onboard/spec-review forbid workflow; formal-proof.md lists `proof audit --check`. |
| P10 formal-proof bool Kind2 | **done** | `proof verify`; `proof audit --check system_formalization_complete --check variables_declared` | **pass**. Dual audit: `verify_passes` “verify pipeline passed”; `system_formalization_complete` 10/10 FRETish; `variables_declared` 27 components preflight. |
| P11 measure Implements paths | **done** | `proof audit --check code_mcdc_coverage` | **pass**. Aggregate decisions 100.0%, conditions 100.0%, 0 incomplete functions. `stacks/util.py` is 9/9 decisions (10/10 conditions). |
| P12 session mistakes → named checks | **done (honest amber)** | `proof signals` / pack presence / `code_signal_obligations_reviewed` (after engine lands); `role_prompt_hygiene`; `process_checklist` | IAM `Action=* Resource=*` and untrusted HTML-to-PDF are reusable Python signal-pack rules (`builtin:python/default` / `py.privilege.unconstrained_grant`, `py.template.untrusted_string_render`), **not** obligatory named checks. Do not judge via `proof audit --check iam_wildcard_policy_clean`. General gates stay: `role_prompt_hygiene`, `acceptance_witness_quality`, `code_predicates_modeled`, `required_checks` rewind, history-mine bind. `process_checklist` **rewound `variables`** (`variable_drift` 20 stale_in_list; `variables_declared` SYS-006 input-only IAM conjunct). Checklist incomplete on purpose. Do not claim 0/0. |

---

## 1. What went wrong (witness, not theory)

An onboard of this AWS CDK / Lambda / Streamlit sample produced a
**structurally complete** four-layer tree that did **not** describe the
shipped logic.

| Machine said | Reality |
|---|---|
| 26 reqs, 4 layers linked, 23 FRETish formulas | Almost every formula is `the X shall always satisfy !A \| B` |
| `l0/l1/l2_*_complete`, `levels_connected` pass | Children rename the same two bools |
| `system_formalization_complete` pass | Non-empty FRETish counts as formalized |
| `nonbool_inputs_constrained` pass | Zero ints declared, so the error check has nothing to fail |
| `solver_modeling_opportunity` pass | Bool-only gate = “no opportunity” |
| `spec_lint_formalization_quality` pass | Well-formed implication is enough |
| `spec_lint_decomposition_adds_refinement` pass | Renamed identifiers, or canned `gap_reviews` |
| `software_formalization_complete` pass | Only looks at **approved** guarantees; all L2 is `review` |
| `under_modeled_requirements_clean` pass | See §4 — scope, engine, family, try/except |
| `process_checklist` / `onboard_v1` complete | Stamps + notes; verify is `test -f proof.yaml` |
| Native Python MC/DC 17/17 on `functions/` | Spec-level `mcdc_coverage` still 53–67 uncovered FRETish rows |

This is a **Proof product gap**. The onboard / spec-review prompts and the
checks they treat as “done” reward a tree of two-bool envelopes.

---

## 2. Design rules

1. **Deterministic first.** If a fact is in AST, MC/DC JSON, description
   numerals, or a named check, a check must decide it. AI writes the formula
   and the rationale; the gate is `proof audit`.
2. **Bool-only can be legitimate.** A mutex of two flags (SW-REQ-010) or a
   parse-or-raise with **zero** extracted Boolean decisions (SW-REQ-001
   `json.loads` + `validate`) may honestly be two bools. “Has only bools” is
   not the smell. The smell is **richer code or prose than the formula**.
3. **Do not invent a third campaign engine.** Bind `onboard_v1` steps to
   existing audit check IDs. Use `proof checklist reset --invalidate-dependents`
   for rewind. Do not route agents through `proof workflow`.
4. **No waiver-shaped close.** Canned `gap_reviews`, leaving L2 at `review`
   so completeness is a no-op, declaring only bools so nonbool/solver stay
   green, and `audit --mute` / workflow `--force` are not fixes.
5. **Dogfood every increment on this repo** before calling the increment
   done. Expected colors are spelled under each item.

---

## 3. Two spines today (keep audit + checklist, drop workflow from the loop)

| Spine | Grain | What it actually enforces | Use? |
|---|---|---|---|
| `proof audit` | ~177 named checks | Real pass/warn/error | **Yes — always** |
| `proof checklist` (`onboard_v1`) | 14-step DAG | Order + **stamps**. Builtin `verify` is `test -f proof.yaml` / `test -d specs`. `process_checklist` counts stamps, cache domains are **config only** | **Yes — after binding to audit checks** |
| `proof workflow` | 4 stages | Advance blocked on a stage bundle; `--force` exists | **No — do not dogfood or document this as the agent loop** |

Checklist already has the rewind primitive:

```bash
proof checklist reset --id spec-review-1 --invalidate-dependents
```

It is **manual**. The missing piece is: when a confirmed step’s
`required_checks` go red on `proof audit`, reset that step and its
dependents.

Builtin `onboard_v1` (embedded in `/tools/bin/proof`):

```text
init              verify: test -f proof.yaml     stamp: confirm+verify
research          notes_required                 stamp: confirm
skeleton          verify: test -d specs          stamp: confirm   # “not full l0 audit”
traces-light                                     stamp: confirm
variables                                        stamp: confirm
spec-review-1 / 2                                stamp: confirm
surface-matrix    verify: test -d proof          stamp: confirm
ac-sweep / hazard / residual                     stamp: confirm
annotations-heavy / coverage / debt-standing     stamp: confirm
```

Project override path (already supported):
`proof/checklists/definitions/onboard_v1.yaml`.

---

## 4. Why `under_modeled_requirements_clean` stayed green

This **is** the check that goes into code, counts decisions, and compares
them to spec vars. It is on (warning). Defaults:

| Knob | Default |
|---|---|
| `code_rich_max_meaningful_vars` | 4 |
| `code_rich_decision_multiplier` | 3 |
| `code_rich_decision_floor` | 3 |
| `witness_rich_max_meaningful_vars` | 1 |
| `family_min_obligation_classes` | 3 |

Why this fixture stayed clean:

1. **`code_mcdc` scope is `functions` only.** Retry `3` and debate `>= 3`
   live in `stacks/`. Unmeasured ⇒ 0 matched decisions ⇒ not “code-rich.”
2. **Tree-sitter skips `try/except`.** SW-001 has 0 extracted decisions.
3. **Default `proof mcdc compare` engine is Go.** Python implements are
   ignored unless `--engine python`. Under-modeled must use the **project
   language**, not Go-by-default.
4. **Family suppression.** SYS-001 / SW-006 / INT-004 share
   `implemented_by` and pool `nominal` + `error_handling` +
   `malformed_input` = 3 → family “adequate,” 13 vs 2 is hidden.
5. **Witness-rich ignores 2-var formulas** (`max_meaningful_vars: 1`).
6. **Cached `tests` domain was empty** on at least one run (SHA of empty).
7. **SW-004 is 2 decisions vs 2 vars** — ratio OK, formula still **false**
   (scores present and all `<= 0` raises). Richness ≠ fidelity.

`proof mcdc compare SW-REQ-006 --engine python` already shows the intended
signal: **13 code decisions, 2 spec vars**, spec-gap on FRETish rows.

---

## 5. Re-review of this fixture (decomposition + FRETish vs code)

Verdicts from a full pass over STK / SYS / SW / INT against shipped Python
and CDK. **MATCH** = formula is the real decision. **PARTIAL** = implication
holds, bound/algorithm missing. **MISMATCH** = wrong property or false
child.

### Software

| Req | FRETish claim | Code actually decides | Fidelity | Decomposition |
|---|---|---|---|---|
| SW-001 | invalid payload ⇒ raise | `json.loads` **or** schema validate; SFN vs Flows event shape | PARTIAL | UNDER |
| SW-002 | parse-error “at limit” ⇒ Fail | `number_less_than(parse_error_count, **3**)` | PARTIAL | UNDER — `3` not in formula |
| SW-003 | task-token wait ⇒ PAUSED | last event, `invoke.waitForTaskToken`; `seek_user_input` is a no-op | PARTIAL | FALSE of SYS-003 |
| SW-004 | scores present ⇒ winner | argmax, `highest_score = 0`, strict `>`; all `<= 0` **raises** | **MISMATCH** | FALSE of SYS-004 |
| SW-005 | map results ⇒ merged | `[:-2]` prefix + `[-2:]` tails; empty `IndexError` | PARTIAL | FALSE of SYS-001 |
| SW-006 | invalid URL ⇒ reject | regex + example URL; 3 extract attempts; `len > 5000`; HTTP 200/400/500 | **MISMATCH** as one leaf | FALSE of SYS-001 |
| SW-007 | itinerary ready ⇒ presigned URL | upload + `ExpiresIn=900`; missing bucket still “succeeds” | PARTIAL | FALSE of SYS-001 |
| SW-008 | failed metric ⇒ composite exists | 7 SMs, `threshold=1`, SNS **only on composite** | PARTIAL | UNDER |
| SW-009 | documented SFN name ⇒ stack | SFN 9 / Flows 6; Flows half not in FRETish | PARTIAL | UNDER |
| SW-010 | conflicting options ⇒ raise | `initial_assistant_text and pass_conversation` | **MATCH** | FALSE of SYS-001 |

### System / integration / stakeholder

| Req | Issue |
|---|---|
| SYS-001 | Kitchen-sink parent. MoviePitch can stay PAUSED. Merge/PDF/GitHub/builder dumped here. |
| SYS-002 | “Three” only in prose. Only Story/Meal/Validation parse JSON. |
| SYS-003 | INT-002 (`StartExecution`) is not a pause child. |
| SYS-004 | Bound is `agree=yes OR debate_round>=3` in the stack Choice. SW-004 is argmax, not that bound. |
| SYS-005 | CDK existence ≠ runtime publish. Techniques not alarmed; STK text said “demo or technique.” |
| SYS-006 | No name enums. SFN 9 vs Flows 6. |
| INT-002 | Tautological start⇒StartExecution; false child of SYS-001/003. |
| STK ACs | Testable; `witness_deferred` honest. SYS-002 over-traced onto demos that never parse JSON. |

**None of the 23 formalized formulas is a complete model of its implementing
function.** One (SW-010) is an honest one-guard leaf.

This fixture stays as the regression corpus. Deepening the 26 reqs is a
**later dogfood campaign** after the gates exist; otherwise agents will
just stamp a new skeleton.

---

## 6. Improvements

Each item: problem, change, **dogfood** (always `proof audit` / named
check / checklist on `/workspace`).

Ship order is the numbering. Do not skip dogfood.

---

### P0 — Bind `onboard_v1` steps to named audit checks

**Status: in-repo-applied / engine-blocked.** Override `proof/checklists/definitions/onboard_v1.yaml`. `proof audit --check process_checklist` → **warn**. `proof checklist check onboard_v1` → EXIT 1 (`verify_failed: coverage`). Auto-rewind not in binary.

**Problem.** Confirm is a diary. `process_checklist` does not re-run work.
Builtin `verify` is `test -f proof.yaml`.

**Change.**

- Add `required_checks: [check-id, …]` on checklist steps (or treat
  `verify:` as `proof audit --check a --check b` with `stamp: confirm+verify`).
- Refuse `proof checklist confirm` unless those checks are green at the
  configured fail-level (**warn**, same as a normal `proof audit`).
- Persist per-check `{id, status, at}` on the stamp, not only
  `{exit_code, passed}`.
- `process_checklist` **re-runs** each confirmed step’s checks. On
  warn/error: equivalent of
  `proof checklist reset --id <step> --invalidate-dependents`.
- Hash checklist state + bound check domains (today: config only).
- Suggested bindings for this fixture (adjust, do not use workflow stages):

  | Step | `required_checks` (minimum) |
  |---|---|
  | init | `validate_passes` after `proof.yaml` exists |
  | skeleton | `l0_stakeholder_complete`, `l1_system_complete`, `l2_software_complete`, `levels_connected` |
  | traces-light | `annotation_validity`, `orphan_code_clean` (or lint_clean) |
  | variables | `variable_orphans_clean`, `variables_declared`, `variable_drift` |
  | spec-review-1 | `spec_lint_decomposition_adds_refinement`, `spec_lint_formalization_quality`, `solver_modeling_opportunity`, `under_modeled_requirements_clean` |
  | spec-review-2 | `spec_lint_spec_conformance_review_grounded` (+ P6 if shipped) |
  | annotations-heavy | `annotation_validity`, `obligation_witness_grounded` |
  | coverage | `code_mcdc_coverage`, `code_mcdc_measure` |
  | debt-standing | `process_checklist` itself consistent; open KIs listed, no waivers |

**Dogfood.**

1. Install a prototype override in
   `proof/checklists/definitions/onboard_v1.yaml` **or** a Proof build that
   understands `required_checks`.
2. `proof checklist reset --id skeleton --invalidate-dependents`.
3. `proof checklist confirm --id skeleton --note "expect refuse"` —
   must **refuse** until P2–P4 are green *or* (before those ship) until
   `l0/l1/l2/levels` pass (they already do).
4. After P2–P4 exist: confirm must refuse this fixture at `spec-review-1`
   because under-modeled / formalization-quality / solver-opportunity
   should be red.
5. `proof audit --check process_checklist` must go **warn/error**, not
   OK-complete, while those checks are red.
6. After a fake confirm (if you temporarily weaken the bind), break
   `levels_connected` and re-run `proof audit --check process_checklist`
   — dependents must show pending. Restore the spec.
7. Never use `proof workflow advance` in this script.

---

### P1 — `under_modeled_requirements_clean` must see this repo’s Python

**Status: in-repo-applied / engine-blocked.** Knobs in `proof.yaml`. `proof audit --check under_modeled_requirements_clean` → **pass** (still no 13-vs-N finding).

**Problem.** The richness check exists and stayed green for the reasons
in §4.

**Change.**

- Default compare / under-modeled engine = project `code_mcdc` language
  (here: python), not Go.
- Match implements paths even when they sit outside `targets[].scope`
  **or** document that unmeasured implements are `mapping-gap` (warn),
  not “not under-modeled.”
- Family suppression must not hide `decisions >= vars * multiplier`.
  Either disable family suppress for the code-rich ratio, or emit both
  family-ok **and** a still-visible per-req ratio finding.
- Raise `witness_rich_max_meaningful_vars` so 2-var specs can fire.
- Count `try/except` that implements the FRETish action (raise) **or**
  treat “0 decisions + raise-based guarantee” as a documented exception,
  not a silent pass for every envelope.
- Publish thresholds in `proof help under_modeled_requirements_clean`
  (they are already `proof config get`-able).

**Dogfood.**

```bash
proof mcdc measure ./functions --engine python
proof mcdc compare SW-REQ-006 --engine python
proof audit --check under_modeled_requirements_clean --verbose
```

**Expect after the fix:** SW-REQ-006 **warn** (13 vs 2). SW-REQ-010 stay
clean. SW-REQ-001 stay clean or an explicit “no boolean AST” note.
SW-REQ-002 **warn or mapping-gap** (implements in `stacks/`, not
`functions/`) — not a silent pass.

Then:

```bash
proof audit --check process_checklist
```

If P0 is in, `spec-review-1` / later steps must unconfirm.

---

### P2 — `solver_modeling_opportunity`: drop the bool-only hide

**Status: engine-blocked / in-repo-applied.** Numeric FRETish on SW-002/004/006 and SYS-004. `proof audit --check solver_modeling_opportunity` → **pass** (1 signal modeled; bool-only gate still hides the rest).

**Problem.** Descriptions already say “three”, “highest score”, “example
repository.” The check treats all-bool models as “0 enumerable-domain
signals.”

**Change.** If description/rationale (or implements-code compare) has a
numeral, bound, enum list, or max, and no `range:` / `data_constraint` /
`domain.tables` is on a variable **that requirement names**, **warn**.
Do not pass with “bool-only gate / no opportunity.”

`description_grammar_enumeration_complete` is the **wrong** check (parser
bracket-trailers, default off). Do not turn it on as a substitute.

**Dogfood.**

```bash
proof audit --check solver_modeling_opportunity --verbose
```

**Expect:** SYS-REQ-002 (“three”), SW-REQ-002, SW-REQ-004 (“highest”),
SW-REQ-006 (“https” / example repo) **warn**. SW-REQ-010 stay clean if
prose has no numeral.

---

### P3 — `nonbool_inputs_constrained` polarity when code has numbers

**Status: engine-blocked / in-repo-applied.** Declared `parse_error_count`, `winning_score`, `readme_len`, `debate_round` with `range:`. `proof audit --check nonbool_inputs_constrained` → **pass** (“3 non-bool … carry a domain model”).

**Problem.** Severity is already **error**, but 0 non-bools ⇒ pass.

**Change.** If implements-set (or measured decisions) contain a numeric
compare / length / status and the requirement still has only bools,
**fail** (or warn at first, then error). Vacuous “no ints declared” is
not a pass when those compares exist.

Keep today’s error for “declared int without range.”

**Dogfood.**

```bash
proof audit --check nonbool_inputs_constrained --verbose
```

**Expect:** SW-002 / SW-004 / SW-006 fail or warn. SW-010 pass.

Do **not** “fix” the fixture by deleting the Python compares.

---

### P4 — `spec_lint_formalization_quality` reject rich two-bool envelopes

**Status: engine-blocked.** `proof audit --check spec_lint_formalization_quality` → **pass**.

**Problem.** `!P | Q` over two bools is well-formed and green even when
description, tests, or code are richer.

**Change.** Fail when the formula is equivalent to `!P | Q` over exactly
two bools **and** any of:

- description/rationale contains a cardinal/bound/URL grammar;
- matched implements-function has more extracted decisions than spec vars
  (reuse P1 counts);
- a verifying test name/body contains a literal not in the formula
  (`5000`, `3`).

Do **not** fail SW-010 or a documented 0-decision raise handler.

**Dogfood.**

```bash
proof audit --check spec_lint_formalization_quality --verbose
```

**Expect:** SW-002, SW-004, SW-006, SYS-002, SYS-004 **warn**. SW-010
clean.

---

### P5 — `spec_lint_decomposition_adds_refinement` is semantic

**Status: engine-blocked / in-repo-applied.** SYS-REQ-007..010; SW-005/006/007/010 and INT-004/006 re-parented. `proof audit --check spec_lint_decomposition_adds_refinement` → **pass**.

**Problem.** Jaccard-on-approved-only + “new identifier” lets renamed
`!A|B` through. Identical `gap_reviews` (“covered at a different
identifier; no additional child”) stamped all 6 SYS-REQs in one edit.

**Change.**

- Apply at `review` as well as `approved`.
- Pass only if the child is **stronger**: extra conjunct, numeric
  tightening, or a new case the parent does not name.
- Fail same `!A|B` with renamed bools.
- Reject `gap_reviews` whose reason is reused on ≥2 requirements or that
  say “different identifier” without a stronger child.

**Dogfood.**

```bash
proof audit --check spec_lint_decomposition_adds_refinement --verbose
```

**Expect:** SYS-001 children SW-005/006/007/010, SYS-003←INT-002,
SYS-004←SW-004 **warn**. After a real child
(`parse_error_count >= 3 ⇒ Fail`) the pair SYS-002 / SW-002 can go green.

---

### P6 — `software_formalization_complete` includes `review`

**Status: engine-blocked.** `proof audit --check software_formalization_complete` → **pass** (vacuous: no approved L2).

**Problem.** “No approved guarantees to check” is a pass while all 10
SW-REQs sit at `review`.

**Change.** Every non-draft, non-retired L2/INT guarantee must have a
non-envelope formalization. Status `review` is not a holiday.

**Dogfood.**

```bash
proof audit --check software_formalization_complete --check interface_formalization_complete
```

**Expect:** fail or warn on this fixture until P4 is green (or formulas
are deepened). Do not `proof req edit --status approved` to silence it.

---

### P7 — New `spec_conformance_review_predicates_in_formula`

**Status: engine-blocked.** Check id missing. `proof audit --check spec_lint_spec_conformance_review_grounded` → **pass**.

**Problem.** REVIEW-2 says “after three failures”; formula has no `3`.
REVIEW-6 names owner/repo and example URL; formula has one bool.

**Change.** A `kind: spec_conformance` review **fails** if the comment
cites a numeral, bound, or concrete token that is not a FRETish /
`variables:` identifier.

**Dogfood.**

```bash
proof audit --check spec_lint_spec_conformance_review_grounded
# plus the new check id once named
proof audit --check spec_conformance_review_predicates_in_formula
```

**Expect:** REVIEW-2, REVIEW-6 **warn**. After formulas include `3` /
URL grammar, reviews can be rewritten and the check goes green.

---

### P8 — Optional new `code_predicates_modeled`

**Status: engine-blocked.** No such check in this binary.

**Problem.** P1–P4 are ratio and prose. Maintainers may want an explicit
per-predicate inventory.

**Change.** For each `# Implements:` function in scope: every
load-bearing compare is a spec variable used in FRETish, or a
**per-predicate** `not_modeled` reason naming the literal. Routing
`api_path` switches may be `not_modeled: dispatcher` if the req does not
claim routing.

**Dogfood.**

```bash
proof audit --check code_predicates_modeled --verbose
```

**Expect:** SW-006 README `len>5000` and Bedrock `range(3)` listed.
SW-010 empty. Agents must not mass-`not_modeled` to go green — if they
do, add a count cap or require `[ki:]`.

---

### P9 — Onboard and spec-review **prompts** (still gated by audit)

**Status: engine-blocked.** Roles are in the binary. This dogfood used only `proof audit` / `proof checklist`.

**Problem.** Onboard: “skeleton = FRETish present + linked +
requirement-first vars.” Spec-review: bool-hiding-numeric is **judgment**,
not an exit check. EXIT CHECKS are prompt text;
`role_references_resolve` only checks the role name exists.

**Change.** Role text (ASD-STE100):

1. Read the implementing function before the formula.
2. List every decide-condition (compare, length, retry, regex, enum).
3. Put each in FRETish as a typed variable. If the code has `3` or
   `5000`, the vars file has `3` or `5000`.
4. A four-layer tree of `!A | B` is a **stub**. Confirm is refused by
   P0+P1+P4, not by hoping the agent feels guilty.
5. Spec-review: do not stamp `gap_reviews` for decomposition; change the
   child formula. Realize/consistency/vacuity on two bools is not quality.
6. Every “run workflow / advance” sentence in roles becomes
   `proof audit --check …` + `proof checklist confirm` only if audit is
   green.

**Dogfood.**

1. Point an agent at a **clean clone** of this repo (or a worktree with
   specs deleted) with the new role text **and** P0–P4 built.
2. Allowed commands: `proof audit`, `proof audit --check`,
   `proof checklist *`, `proof req`, `proof mcdc *`. **Forbidden:**
   `proof workflow`, `proof waive`.
3. Success: agent cannot `checklist confirm spec-review-1` until
   under-modeled / formalization-quality fire and then get a real formula
   change (or an honest KI that does **not** make the check green).
4. Failure: agent confirms skeleton with 26 `!A|B` and
   `process_checklist` is OK.

---

### P10 — Formal-proof role: bool Kind2 ≠ valid software model

**Status: engine-blocked / in-repo-applied.** `proof verify` with z3+kind2 on PATH → realizability/consistency/vacuity **PASS** on numeric formulas. Cached “8 failed” was Kind2 “No SMT Solver found,” not unrealizable ints.

**Problem.** Realize / consistency / vacuity pass on two bools;
`formalization_status: valid` follows.

**Change.** If implements-set (or P1 counts) has ints/compares and the
Kind2/Z3 model is bool-only, do **not** report valid completeness.
Encode the bound (`parse_error_count < 3`) and prove **that**.

**Dogfood.**

```bash
proof verify
proof audit --check system_formalization_complete --check variables_declared
```

**Expect:** after P2/P3, `proof verify` is not a clean “23 cached PASS”
story until bounds are in the model. Do not skip Kind2 to hide this.

---

### P11 — Measure implements, not only `functions/`

**Status: in-repo-applied.** `code_mcdc.targets` includes `stacks/util.py`. `proof audit --check code_mcdc_coverage` → **warn** (util 5/9). KI-code-mcdc-util-polarities.

**Problem.** Onboard note claimed MC/DC on functions/webapp/stacks.
`proof.yaml` target is `functions`. Stacks hold the real bounds.

**Change.** Default Python target (or a second target) includes paths
that `# Implements:` actually names. Or under-modeled treats “implements
outside measure scope” as mapping-gap **warn**.

**Dogfood.**

```bash
proof mcdc measure ./stacks --engine python
proof mcdc compare SW-REQ-002 --engine python
proof audit --check code_mcdc_coverage --check under_modeled_requirements_clean
```

**Expect:** SW-002 grows matched decisions around `number_less_than(..., 3)`.
`code_mcdc_coverage` may drop below 100% until tests drive those
branches — leftover is a KI or a test, not a mute.

---

### P12 — Session mistakes become named checks

**Status: done (honest amber).** Product correction: IAM `Action=*
Resource=*` and untrusted template/HTML-to-PDF are **not** obligatory
project-specific audit checks. They are **reusable code-signal rules**
in Proof's Python signal pack (`builtin:python/default` /
`py.privilege.unconstrained_grant`, `py.template.untrusted_string_render`),
auto-selected when a repo has `.py` and `signals.defaults: auto`. The
reusable *gate* is the existing `code_signal_obligations_reviewed` /
`proof signals` machinery, not a new default-on check named after AWS
or WeasyPrint.

What stays as named checks (general Proof process gates):
`role_prompt_hygiene`, `acceptance_witness_quality`,
`code_predicates_modeled`, `required_checks` rewind, history-mine bind.

Do not claim 0/0. `process_checklist` rewind of `variables` is still
general (drift / declared). `process_checklist` rewind only re-runs
`required_checks` on confirmed steps
(`ReevaluateConfirmedRequiredChecks` skips steps with empty
RequiredChecks). A confirm+verify `verify:` command is a shell
soft-check; it does **not** feed rewind.

**Problem.** This fixture's override used `verify: "proof audit --check …"`
on init / skeleton / traces / variables / spec-review / coverage /
annotations-heavy. That is a shell soft-check. Hazard-sweep returned
`[]` while Codex had already found `Action=* Resource=*` and
md2pdf/WeasyPrint SSTI/SSRF. History-mine and role-prompt hygiene were
chat interventions, not stamp gates.

The wrong product reaction was to mint obligatory default-on checks
named `iam_wildcard_policy_clean` and `untrusted_renderer_clean`. Those
names encode AWS IAM and WeasyPrint/md2pdf. They are not general Proof
process. The right reaction is to treat those code smells as reusable
signal-pack rules, gated by `code_signal_obligations_reviewed` after
`proof signals` selects the Python pack.

**Change.** Bind load-bearing `onboard_v1` steps to `required_checks`
(same ids as builtin Proof, plus *general* session-lesson checks). Keep
`verify:` only as a soft file existence check (`test -f proof.yaml`,
`test -d specs`, `test -d proof`). Do **not** file KnownIssues for
process/audit gaps. Do **not** add `iam_wildcard_policy_clean` or
`untrusted_renderer_clean` to `hazard.required_checks`. Hazard stays
`spec_lint_hazard_consequence` only. Do **not** delete product IAM
`*:*` or md2pdf — those stay as product defects; they surface via the
Python signal pack when the engine lands, not via obligatory named
checks.

| Check / gate | Session mistake | Expected color on this fixture |
|---|---|---|
| `builtin:python/default` `py.privilege.unconstrained_grant` via `proof signals` / `code_signal_obligations_reviewed` | Codex found Action=* Resource=* in `pipeline/pipeline_stack.py`; hazard-sweep returned `[]` | signal present when `.py` + `signals.defaults: auto`; obligations reviewed after engine lands. **Not** `proof audit --check iam_wildcard_policy_clean` |
| `builtin:python/default` `py.template.untrusted_string_render` via `proof signals` / `code_signal_obligations_reviewed` | md2pdf/WeasyPrint SSTI/SSRF in `functions/trip_planner/pdf_creator` | same: pack rule, not a WeasyPrint-named check |
| `role_prompt_hygiene` | empty-list-is-success / Max 3 / Prefer 0 in role prompts | pass on current builtin roles |
| `acceptance_witness_quality` | `:acceptance` on the same test as SYS/SW/INT verifies | already implemented |
| `code_predicates_modeled` | load-bearing compares unmodeled | already implemented |
| history-mine on `onboard_v1` | history sweep was a chat intervention | already bound |
| fixture `required_checks` parity | `verify: proof audit --check` does not rewind | this YAML fix |

**Dogfood** (`/home/dev/src/proof-bin/proof`, 2026-08-14):

| Command | Color | Observation |
|---|---|---|
| `proof signals` / pack presence / `code_signal_obligations_reviewed` | after engine lands | Judge IAM `Action=* Resource=*` and untrusted HTML-to-PDF here (`builtin:python/default`: `py.privilege.unconstrained_grant`, `py.template.untrusted_string_render`). Do **not** judge via `proof audit --check iam_wildcard_policy_clean` or `untrusted_renderer_clean`. |
| `proof audit --check role_prompt_hygiene` | **pass** | `no empty-is-win or finding-quota language in 41 role(s)` |
| `proof audit --check code_predicates_modeled` | **pass** | 17 implemented FRETish reqs; constructor kwargs (`indent=2`, `memory_size=256`) no longer count as predicates |
| `proof audit --check process_checklist` | **warn** | Rewound `variables` (`variable_drift` + `variables_declared`). Dependents pending. That rewind is still general. |
| `proof checklist check onboard_v1` | EXIT 1 | next: `variables`. Do not confirm over red. |

Unknown check ids fail-closed on `proof checklist confirm`. Do not use
`--mute` or `--fail-level error`. Do not run `proof workflow`. Do not
claim 0/0.

---

## 7. What must not be used as a close-out

- `gap_reviews` with a canned “different identifier” sentence
- `audit_ignore` on envelope-formula lints
- Promoting reqs to `approved` so P6 goes quiet without stronger FRETish
- Declaring only bools so P2/P3 stay green
- A KI that says “bool envelope is enough for a sample CDK repo”
- Withdrawing MC/DC KIs while the spec still omits `5000` / `3`
- `proof workflow advance --force` or `--skip-check`
- `proof audit --mute` / `--fail-level error` to hide warns
- `approval.agent_autonomous_for.all: true` used to self-approve
  gap_reviews on formulas the same agent wrote

Modeling debt is a **missing or weak requirement**, not a known issue on
the application code — unless the code is actually wrong (SW-004’s
`highest_score = 0` vs “scores present ⇒ winner” is a **spec** defect;
the raise-on-non-positive path is the code’s real rule).

---

## 8. Suggested Proof issue titles

1. Checklist steps `required_checks` + fail-closed `confirm` +
   `process_checklist` rewind via `reset --invalidate-dependents`.
2. `under_modeled_requirements_clean` uses project language engine;
   family suppress cannot hide decision/var ratio.
3. `solver_modeling_opportunity` bool-only gate hides description/code
   bounds.
4. `nonbool_inputs_constrained` fails when implements have numeric
   compares and the spec has zero ints.
5. `spec_lint_formalization_quality` rejects two-bool envelopes against
   richer description/code/tests.
6. `spec_lint_decomposition_adds_refinement` requires a stronger child;
   reject copy-paste `gap_reviews`.
7. `software_formalization_complete` includes `status: review`.
8. New `spec_conformance_review_predicates_in_formula`.
9. Optional `code_predicates_modeled`.
10. Rewrite onboard / spec-review / formal-proof: FRETish names code
    predicates; agent loop is `proof audit`, not `proof workflow`.
11. Python MC/DC / under-modeled cover `# Implements:` paths, not only
    `functions/`.

---

## 9. Dogfood campaign (this repo, audit only)

Run after **each** P-item, not once at the end.

```bash
# Always
export PATH="/home/dev/.proof/tools/probe/0.6.0-rc330:/usr/bin:/bin:$PATH"   # or the build under test

proof audit --check <the-check-just-changed> --verbose --max-findings 0
proof audit                          # default warn; no --mute, no --fail-level
proof checklist show onboard_v1
proof checklist check onboard_v1
```

Record for each P-item:

| Field | Value |
|---|---|
| Proof version / commit | |
| Command | `proof audit --check …` |
| Expected color on this fixture | red / green / mapping-gap |
| Actual color | |
| Checklist step that should rewind | e.g. `spec-review-1` |
| Did `process_checklist` rewind? | yes / no |

When several P-items are in one build, run **one** full `proof audit`
and paste the finding-id set. Dual-run the full audit twice only when
claiming “no flake.”

Deepening SW-002 / SW-004 / SW-006 / SYS-004 FRETish is the **second**
campaign, after P0–P5 exist, so this repo can flip from red fixture to
green fixture on purpose.

---

## 10. AI vs deterministic (keep the mix)

**Machine (`proof audit --check`):** graph completeness, lint IDs,
richness ratio, numeral-in-prose, confirm/rewind, MC/DC measure.

**AI (stamp + note, never a silent pass):** research stakeholders, AC
wording, hazard ACCEPT/SUPPRESS rationale, close-call 2-vs-2 modeling
(did the bool hide `score > 0`?), review prose.

If it can be a check, it is not a role EXIT CHECK.
