# Proof (ReqProof) CLI issues found during audit work

Ad-hoc log of `proof` CLI bugs and UX confusions observed while closing audit
warnings on `AWS-prompt-chaining/Audit`. Each entry: symptom, impact, and a
suggested fix. Not a spec — a running "papercut" list.

## 1. Stale `proof` binary produced a confusing `not_modeled` guard

- **Symptom:** two `proof` binaries were on disk; `/tools/bin/proof` was older
  than the source at `/home/dev/src/reqproof`. The stale binary rejected valid
  `known_issue_complete` dispositions with a `not_modeled` error.
- **Impact:** misleading "your KnownIssue is malformed" failures that had
  nothing to do with the project.
- **Fix:** rebuild from source (`go build -o ... ./cmd/proof`). The tool should
  print its build/commit on `--version` and warn when the binary is older than
  the `proof.yaml` tool version it claims.

## 2. `proof audit --format json` emits NDJSON, not a JSON document

- **Symptom:** `proof audit --format json` prints one JSON object per line
  (`{"event":"stage_start",...}` etc.), so a plain `json.load()` fails with
  "Extra data".
- **Impact:** scripts that assume `--format json` returns one document break.
- **Fix:** either emit a single JSON document, or rename the flag to
  `--format jsonl` / document it as line-delimited.

## 3. Ad-hoc `proof mcdc measure <narrow-scope>` clobbers the canonical suite

- **Symptom:** `proof mcdc measure functions --engine python` wrote to
  `.proof/mcdc/python/latest.json` (the canonical path) even though it only
  measured the `functions` subtree, overwriting the aggregate evidence for the
  configured multi-target policy.
- **Impact:** the next `code_mcdc_coverage` run reported
  "decision-python-util runner produced no MC/DC data" because the
  `stacks/util.py` target's evidence had been wiped. The
  `proof help code_mcdc_measure` text says narrower runs land in `adhoc/`, but
  the CLI wrote the canonical path instead.
- **Fix:** make `proof mcdc measure` write to `adhoc/` when the requested scope
  is narrower than the configured targets (matching the documented behavior),
  and refuse/`--force` when it would overwrite canonical evidence.

## 4. Flaky `sys.monitoring` branch capture → non-deterministic code MC/DC

- **Symptom:** the branch `len(readme_content) > 5000` in
  `functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:get_github_repository_readme_agent_action`
  is driven by tests on both polarities, but the Python recorder (PEP 669
  `sys.monitoring`) intermittently records 0 samples for it
  (`samples: 0`, verdict `feasibility_unknown`). The bytecode-identical
  `get_github_repository_readme` in
  `functions/most_popular_repo_strands/index.py` is captured reliably.
- **Impact:** the same `proof audit` / `tests_pass` run flips between 100% and
  96.2% code-level MC/DC non-deterministically, so `code_mcdc_coverage`
  warning state is unstable run-to-run.
- **Fix:** investigate why the recorder drops the branch for one file but not
  its twin (suspected: the `if/else` with an early `return response` compiles
  with duplicated `RETURN_VALUE` and no `JUMP_FORWARD`, unlike the Strands twin
  which has a trailing statement). At minimum the recorder should log when it
  instruments a decision but captures zero samples so this doesn't look like a
  missing test.

## 5. `proof checklist confirm` can rewind itself (confirm → rewind loop)

- **Symptom:** confirming the `coverage` onboarding step runs its
  `code_mcdc_measure` required check, which re-measures. With issue #4's flaky
  recorder, a re-measure can drop below 100%, failing `code_mcdc_coverage`,
  which then rewinds the just-confirmed `coverage` step.
- **Impact:** the operator is stuck confirming the same step repeatedly; the
  checklist never reaches "campaign complete".
- **Fix:** decouple `confirm` from a full re-measure (confirm against the
  cached result), or only rewind on a *deterministic* failure rather than a
  transient measurement dip.

## 6. `proof mcdc measure` error message is Go-specific

- **Symptom:** running `proof mcdc measure` with no pattern prints
  "provide either a package pattern or an explicit `go test` command".
- **Impact:** confusing for a Python-only project.
- **Fix:** emit an engine-aware hint (e.g. `python3 -m pytest` for Python).

## 7. `proof checklist confirm` package-scope error doesn't name valid keys

- **Symptom:** `proof checklist confirm --id coverage` fails with
  "step \"coverage\" is package-scoped; pass package key" but doesn't list the
  valid keys.
- **Impact:** the operator must guess (`pipeline` is what the state file uses).
- **Fix:** include the valid package key(s) in the error, e.g. from the
  checklist state's `scope_key`.

## 8. `# mcdc:ignore:capability-gap` requires a KnownIssue, undiscoverable

- **Symptom:** a code-level `# mcdc:ignore:capability-gap <reason>` annotation
  without a `[ki: <slug>]` reference is accepted by the extractor but fails
  `mcdc_ignore_classified` with "capability-gap without a resolvable
  KnownIssue".
- **Impact:** the requirement to file/link a KnownIssue for the
  `capability-gap` category is not visible from the annotation syntax or the
  `mcdc measure` output.
- **Fix:** surface the category→KnownIssue requirement in
  `proof help mcdc_ignore_classified` examples and in the `mcdc report`
  hotspot hint.

## 9. KI evidence freshness hashes the whole test file

- **Symptom:** editing a test file that contains any `// Reproduces:` comment
  (even a comment tweak or an unused-import cleanup) invalidates the freshness
  hash of every KnownIssue whose reproducer lives in that file, requiring a
  separate `proof evidence refresh <slug>` per KI.
- **Impact:** routine test maintenance triggers a batch of "stale evidence"
  findings.
- **Fix:** hash per-reproducer (function) rather than per-file, or offer a
  single `proof evidence refresh --all` for the affected KIs.
