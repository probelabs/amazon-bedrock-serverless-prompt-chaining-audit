# History-mine memo

Role: `history-mine` (SYS-REQ-1390).
Repo: amazon-bedrock-serverless-prompt-chaining.
Mined: 2026-08-14 against HEAD `92098a6052a8dae63f3cf4becd066489704c7068`.
No audited tag / last-release marker in this worktree; last 40 commits are almost entirely dependabot, so behavior-changing commits were sampled from `functions/`, `stacks/`, `webapp/`, and `pipeline/` beyond that window.

Do not treat this memo as a spec edit. Spec absorption recommendations below are for the spec-owning agent.

## 1. Last 40 commits (`git log -n 40 --oneline`)

All 40 are dependency / pin bumps except one runtime bump. None change product control flow.

| SHA | Date | Subject | Class |
|-----|------|---------|-------|
| 92098a6 | 2026-08-03 | Bump boto3 | refactor |
| 043853a | 2026-08-01 | Bump aws-cdk-aws-lambda-python-alpha 2.262.2a0 (#752) | refactor |
| 5ea6147 | 2026-08-01 | Bump boto3 in /webapp (#760) | refactor |
| fb6fc6f | 2026-08-01 | Bump aws-cdk-lib 2.262.2 (#762) | refactor |
| 91ba3e7 | 2026-08-01 | Bump boto3 1.43.58 (#761) | refactor |
| c1964f4 | 2026-08-01 | Bump strands-agents (#767) | refactor |
| b696185 | 2026-08-01 | Bump boto3 in strands (#766) | refactor |
| df594ca | 2026-08-01 | streamlit >=1.60.0 (#763) | refactor |
| 5d5cbb2 | 2026-08-01 | Bump boto3 in bedrock agent (#759) | refactor |
| cfa0f13 | 2026-08-01 | Bump boto3 in pdf_creator (#758) | refactor |
| 36f1eee | 2026-08-01 | streamlit >=1.60.0 in /webapp (#755) | refactor |
| fa28826 | 2026-08-01 | constructs >=10.7.2 (#754) | refactor |
| e3c0fe8 | 2026-07-01 | Bump boto3 in strands (#745) | refactor |
| 3a3128b | 2026-07-01 | Bump lambda-python-alpha 2.260.0a0 (#732) | refactor |
| 700b9a3 | 2026-07-01 | Bump strands-agents (#744) | refactor |
| 772e841 | 2026-07-01 | Bump beautifulsoup4 (#743) | refactor |
| cb76030 | 2026-07-01 | Bump boto3 in pdf_creator (#737) | refactor |
| 15603fb | 2026-07-01 | Bump boto3 (#736) | refactor |
| 2307165 | 2026-07-01 | Bump boto3 in bedrock agent (#735) | refactor |
| 92e9e6c | 2026-07-01 | Bump boto3 1.43.38 (#734) | refactor |
| cf2083a | 2026-07-01 | Bump boto3 in /webapp (#733) | refactor |
| 2f2c8f7 | 2026-07-01 | Bump aws-cdk-lib in /pipeline (#731) | refactor |
| ac0cfdd | 2026-07-01 | Bump aws-cdk-lib (#730) | refactor |
| 102f0d1 | 2026-06-02 | Bump lambda-python-alpha 2.257.0a0 (#699) | refactor |
| 6e12031 | 2026-06-03 | streamlit >=1.58.0 in /webapp (#702) | refactor |
| 7e2bbb1 | 2026-06-03 | Bump requests in strands (#719) | refactor |
| a3d0ad5 | 2026-06-03 | Bump requests (#708) | refactor |
| 330082b | 2026-06-03 | Bump boto3 in strands (#720) | refactor |
| f355ab4 | 2026-06-03 | Bump strands-agents (#718) | refactor |
| 55b54f5 | 2026-06-03 | Bump boto3 in bedrock agent (#709) | refactor |
| a544984 | 2026-06-03 | Bump boto3 (#707) | refactor |
| cadec4a | 2026-06-03 | Bump boto3 in pdf_creator (#706) | refactor |
| 561f543 | 2026-06-03 | Bump aws-cdk-lib 2.257.0 (#705) | refactor |
| 9ada074 | 2026-06-03 | Bump boto3 in /webapp (#703) | refactor |
| bf9bfe6 | 2026-06-03 | Bump boto3 1.43.20 (#701) | refactor |
| 9842b5c | 2026-06-03 | Bump aws-cdk-lib in /pipeline (#700) | refactor |
| 619c21f | 2026-05-05 | Bump lambda-python-alpha 2.252.0a0 (#673) | refactor |
| 4915e9f | 2026-05-05 | Bump aws-cdk-lib 2.252.0 (#675) | refactor |
| 2b56163 | 2026-05-05 | Bump boto3 in strands (#687) | refactor |
| 4709765 | 2026-05-05 | Upgrade streamlit to Python 3.13 | refactor |

`4709765` is the only last-40 commit that is not a dependabot pin. It is a runtime bump (Streamlit / Python 3.13), not a product-behavior change.

## 2. Sampled behavior-changing commits

Sampled diffs under `functions/`, `stacks/`, `webapp/`, `pipeline/`. Classification is refactor / fix / feature (plus migration when the commit is a wholesale swap that also ports bugs).

| SHA | Date | Subject | Paths | Class | Notes |
|-----|------|---------|-------|-------|-------|
| 08848a5 | 2026-02-03 | Breaking changes in md2pdf | `functions/trip_planner/pdf_creator/index.py` | fix (API) / class-worsening | `md_content=` → `raw=`. Current SSTI path. See DEFECT-260814-MD2P. |
| 6dc7231 | 2026-02-04 | Migrate from Langchain → Strands | `functions/most_popular_repo_strands/`, stacks, webapp | feature / migration | Ports PAT tool, no-timeout GET, unanchored `re.match`. Sibling of Bedrock actions. |
| e46a8b3 | 2026-03-01 | Switch agents to Nova Pro | stacks / functions | feature | Model-id swap. |
| fff85a4 | 2026-02-01 | Upgrade to Haiku 4.5 | stacks | feature | Model-id swap. |
| d4bdce4 | 2026-02-02 | Add bedrock:GetPrompt permission | `techniques_bedrock_flows/stacks/*` | feature | IAM add, scoped action. |
| 2e0be65 | 2025-04-07 | Increase retries on Bedrock Agents client | `functions/.../agent/index.py` | fix | botocore retries=6. |
| 329cf17 | 2024-12-02 | Trim READMEs to 5k chars | github_agent_actions, langchain | fix | 10000 → 5000. Range already on SW-REQ-006. |
| 3d207b6 | 2024-06-26 | Use GitHub PAT for API calls | functions + stacks | feature | Introduces shared PAT on README tools. KIs: PAT-no-allowlist. |
| 0a837eb | 2024-02-27 | Migrate movie pitch to native Bedrock | `stacks/movie_pitch_stack.py` | feature | Introduces `string_matches f'{i+1}*'`. DEFECT-260814-PTCH. |
| 3d4f547 | 2024-03-08 | Actually insert the pitches into the chooser | `stacks/movie_pitch_stack.py` | fix | Wiring; glob selector left intact. |
| 3d36db2 | 2024-03-13 | Enforce JSON schema validation | parse_json_response, stacks/util | feature | New validator Lambda. |
| 36d293a | 2024-01-08 | Add demo of chaining Bedrock Agents | functions + stacks + webapp | feature | Introduces trending GET (no timeout), unanchored `re.search`, `agent/*` invoke. |
| 69c9ad4 | 2024-04-26 | Deploy Bedrock Agent resources using CloudFormation | `stacks/most_popular_repo_bedrock_agent_stack.py` | feature | CFN wiring; `agent/*` SourceArn remains. |
| 6fad924 | 2023-11-03 | Add CDK pipeline to deploy demo | `pipeline/pipeline_stack.py` | feature | First `actions=["*"], resources=["*"]`. DEFECT-260814-STAR. |
| a71c85a | 2024-05-21 | Add simpler prompt chaining technique examples | pipeline + techniques | feature | Clones star-star onto DeployTechniqueExamples. |
| f64685a | 2024-03-12 | Move Lambda function code around | functions/ | refactor | Path move `agents/` → `functions/`; pdf_creator behavior unchanged. |
| 83b1536 | 2025-01-20 | Bedrock flows — connect input node in all cases | techniques_bedrock_flows | fix | Wiring. |
| a6fe207 | 2025-01-17 | Fix output | techniques test runner | fix | `python3 run-test-execution.sh` → `./run-test-execution.sh`. |
| 92f2d3d | (initial dump) | Initial dump of examples | agents/trip_planner/pdf_creator | feature | First untrusted interpolation into md2pdf. Origin of SSTI class. |

Cross-module porting note (role §4.2): `6dc7231` replaced Langchain with Strands and **copied** `requests.get` without `timeout=`, the unanchored GitHub URL regex, and the PAT README tool. A localized "fix" in one agent is not a closed class until both `github_agent_actions/index.py` and `most_popular_repo_strands/index.py` change.

No CHG records were filed. Last-40 and sampled behavior commits that are genuine features (Strands migration, Nova/Haiku, PAT, pipeline, native Bedrock movie pitch, Bedrock Agents demo) predate the ledger; filing CHGs without a spec-update signal would fail `change_evidence_complete` honesty if those reviews later declared `feature`. The three records below are DEFECTs for live product bugs, not process tickets.

## 3. Recurring failure classes

Recurrence ≥2 (same class in two or more introducing/porting commits or sibling modules) is marked SYSTEMATIC.

| Class | Recurrence | Introducing / porting commits | Live KIs | Spec absorber | Target specs |
|-------|------------|-------------------------------|----------|---------------|--------------|
| **iam_wildcard** (`Action=*` / `Resource=*` / `agent/*`) | SYSTEMATIC (3) | `6fad924` Deploy; `a71c85a` DeployExamples clone; `36d293a`/`69c9ad4` `agent/*` SourceArn | KI-pipeline-deploy-demo-star-star, KI-pipeline-deploy-examples-star-star, KI-bedrock-agent-invoke-wildcard | **data_constraint** (forbid `actions=["*"]` ∧ `resources=["*"]`; pin `aws:SourceArn` to this agent ARN). Optional **table** of allowed action prefixes × resource ARNs. Not range. | SYS-REQ-006 (pipeline host today), SYS-REQ-007 / SW-REQ-006 (agent invoke). A dedicated pipeline-IAM parent would be cleaner; do not stretch technique-catalog counts. |
| **untrusted_renderer** (SSTI + WeasyPrint SSRF) | SYSTEMATIC (2) | `92f2d3d` interpolation; `08848a5` `raw=` | KI-pdf-md2pdf-ssti, KI-pdf-weasyprint-ssrf | **data_constraint** (location/itinerary are data-only; no Jinja, no URL fetch) + **mutex** (untrusted input XOR template/URL renderer). Not range (`expires_in` already has 60–900 and does not catch this). | SW-REQ-007, SYS-REQ-008, INT-REQ-006. pdf_creator.vars.yaml needs a `renderer_is_data_only` / `template_eval_disabled` bool. |
| **pat_tool_no_allowlist** | SYSTEMATIC (2) | `3d207b6` Bedrock+Langchain PAT; `6dc7231` Strands port | KI-github-bedrock-readme-pat-no-allowlist, KI-github-strands-readme-pat-no-allowlist | **data_constraint** (README fetch URL ∈ {trending-selected public repo}; fullmatch `^https://github.com/[^/]+/[^/]+$`). **enum** is the wrong shape (repos are not a closed set). | SW-REQ-006, SYS-REQ-007, INT-REQ-004. |
| **glob_choice** (`string_matches N*`) | 1 (sibling clean) | `0a837eb` | KI-moviepitch-pitch-glob-1star | **enum** `{1,2,3}` exact, not **range** 1–3. Range already exists on `pitch_choice` and is false safety against prefix glob. MealPlanner already uses `string_equals` — port that. Optional **table** digit → Red/Blue/Green. | SYS-REQ-003, SW-REQ-003. stepfn_client.vars.yaml / human_gate.vars.yaml: change `pitch_choice` from range to enum. |
| **no_timeout** (`requests.get` without `timeout=`) | SYSTEMATIC (2) | `36d293a` Bedrock actions; `6dc7231` Strands | KI-github-trending-no-timeout | **range** `requests_timeout_s` ∈ [1, 30]. Already declared on SW-REQ-006 / SYS-REQ-007 / INT-REQ-004 / github_repo_lookup.vars.yaml. Code does not implement it. | SW-REQ-006, SYS-REQ-007, INT-REQ-004. |
| **unanchored_regex** (`re.search` / `re.match` not `fullmatch`) | SYSTEMATIC (2) | `36d293a` Bedrock `re.search`; `6dc7231` Strands `re.match` | KI-github-url-unanchored-match | **data_constraint** already on `url_is_full_github_repo` (starts_with https://github.com/). Strengthen condition to fullmatch `^https://github.com/[^/]+/[^/]+$` (reject prefix/suffix/embedded). Not range. | SW-REQ-006, SYS-REQ-007. |
| **missing_bucket_mock** | 1 (test harness) | n/a (test added in this engagement) | none (not a product defect) | **error_handling** obligation on INT-REQ-006 / SW-REQ-007, not a new data property. `test_missing_pdf_bucket_is_passed_through_to_s3` documents that `PDF_BUCKET=None` is forwarded to S3. Do not file a DEFECT — harness observation, not a historical product incident. | SW-REQ-007, INT-REQ-006 (keep as negative error_handling row). |

Pattern recurrence (role §4.1): IAM wildcard (3), untrusted renderer (2), PAT tool (2), no timeout (2), unanchored regex (2). IAM wildcard is the strongest systematic gap.

Prior-audit blacklist (role §4.3): do not refile the ten reviewed product KIs listed in `proof/known-issues/` (SSTI, WeasyPrint SSRF, both star-star roles, both PAT tools, no-timeout, unanchored regex, pitch glob, agent/* invoke). Withdrawn accept/MC/DC KIs are process coverage, not product bugs.

On-chain / TVL (role §4.4): not applicable. This is an AWS demo, not a DeFi protocol.

Code-signal (role §5): no new detector. No measured precision/recall/leakage bed. Keep classes in this memo + KI sanitizer tags (`manual:ssti`, `manual:iam-star-star`, `manual:choice-glob`, `manual:missing-timeout`, `manual:unanchored-regex`, `manual:missing-allowlist`, `manual:iam-agent-wildcard`).

## 4. DEFECT / CHG IDs filed

| ID | Kind | Class | Links | Disposition |
|----|------|-------|-------|-------------|
| DEFECT-260814-MD2P | DEFECT | untrusted_renderer (SSTI) | KI-pdf-md2pdf-ssti; sibling KI-pdf-weasyprint-ssrf | covered_by_known_issue |
| DEFECT-260814-STAR | DEFECT | iam_wildcard | KI-pipeline-deploy-demo-star-star, KI-pipeline-deploy-examples-star-star; sibling KI-bedrock-agent-invoke-wildcard | covered_by_known_issue |
| DEFECT-260814-PTCH | DEFECT | glob_choice | KI-moviepitch-pitch-glob-1star | covered_by_known_issue |

No CHG records. No process defects invented. Specs/** not edited.

Introducing commits (bisected, not fabricated):

- SSTI interpolation: `92f2d3d53ac473af78ab8fc551cea77fa6342682` (first write). Current `raw=` call: `08848a57ff5166632edfb43ad1a7578709056d9e`.
- Star-star IAM: `6fad9246642a22f315d10a09f1f970826de0687d`. Clone onto examples: `a71c85a00c5dc3a5d800dbe0db0a1b77731d15be`.
- Pitch glob: `0a837eb9c84d8c13bbbe7ea1ac234b7bc99c3331`.

None of the three ever worked correctly; they are new_defect-at-first-write, not regressions.

## 5. What specs should absorb (for the spec-owning agent)

Do not implement these here.

1. **SW-REQ-007 / SYS-REQ-008 / INT-REQ-006** — add a data_constraint (and mutex with template eval) that itinerary/location are not interpreted as Jinja or fetched as URLs. Current `expires_in` range is orthogonal.
2. **SYS-REQ-006** (or a new pipeline-IAM child) — data_constraint / table: DeployExamples and DeployDemoApp roles must not carry `actions=["*"]` + `resources=["*"]`.
3. **SYS-REQ-003 / SW-REQ-003** — replace `pitch_choice` range 1–3 with enum `{1,2,3}` (and a digit→color table). Range cannot reject `"10"`.
4. Already absorbed as range/data_constraint but unimplemented in code: `requests_timeout_s` 1–30 and `url_is_full_github_repo` (SW-REQ-006 / SYS-REQ-007 / INT-REQ-004). Specs should stay; code and KI remain the live gap.

## 6. Audit colors

Command: `proof audit --check problem_reports_reviewed --check change_evidence_complete --verbose`

| Check | Color | Detail |
|-------|-------|--------|
| `problem_reports_reviewed` | **info** (`i`) | 3 report(s): 8 triage-debt. Exit 0. Errors 0, Warnings 0. |
| `change_evidence_complete` | **green** (`✓`) | every in-branch-changed change-typed review has complete backing evidence |

Triage-debt (advisory, expected — specs/** are owned by another agent; no obligation attach / new req / regression-test link was added):

- DEFECT-260814-MD2P: no `hardening.added_obligations` for `untrusted_renderer`; `missing_requirement` without new/strengthened reqs; `missing_test_partition` without `hardening.regression_tests`
- DEFECT-260814-STAR: same three for `iam_wildcard`
- DEFECT-260814-PTCH: no `hardening.added_obligations` for `glob_choice`; `missing_test_partition` without `hardening.regression_tests`

`proof problem-report validate`: 3 report(s), 0 dangerous, 0 advisory.
