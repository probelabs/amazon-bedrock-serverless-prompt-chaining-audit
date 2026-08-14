# Repository Coverage Ledger

## Inventory

- Strategy: repository-wide `rg --files` inventory (250 paths).
- Reviewed: all in-scope paths accounted for; binaries (PNG screenshots) inventoried without deep content analysis; `__pycache__` and `.git` excluded by inventory tooling patterns where applicable.
- SECURITY.md: none present; guidance resolver recorded empty/no policy.

## Surfaces

| Surface | Risk Area | Outcome | Notes |
| --- | --- | --- | --- |
| Trip planner PDF generation (`functions/trip_planner/pdf_creator`, webapp page, stack) | SSTI / SSRF | reported | md2pdf Jinja SSTI and WeasyPrint URL fetch |
| GitHub agent tools (Bedrock Actions + Strands) | PAT tool abuse | reported | unrestricted README fetch |
| CI/CD pipeline deploy roles | Privilege escalation | reported | CodeBuild `*:*` on two deploy stages |
| Streamlit webapp + Cognito/ALB | Authn | rejected | weak password policy suppressed (invite-only) |
| Shared ECS task role / task tokens | Confused deputy | rejected | requires prior UI compromise; no direct IDOR |
| JSON parse/repair (`parse_json_response`, util retry) | Injection/DoS | no_issue_found | schema developer-fixed; bounded retries |
| Meal planner / story / blog / movie pitch prompts | Prompt injection | no_issue_found | residual LLM integrity/cost risk only; no extra sinks beyond intended generation (movie pitch human token handled as shared-role note) |
| Technique SFN/Flows stacks | Demo orchestration | no_issue_found | educational; human_input SNS task token is operator technique, not multi-tenant product |
| Alarms SNS | Notification abuse | no_issue_found | publish limited to codestar-notifications principal pattern |
| Secrets / hardcoded credentials | Secret exposure | no_issue_found | no cloud keys in source; GitHub token via Secrets Manager |
| Docker/local compose | Dev credential mount | not_applicable | local developer workflow only |
| Specs/docs/proof/tests | Non-runtime | not_applicable | assurance artifacts without live privileged sinks |
| Dependabot / GitHub Actions CI | Supply chain | no_issue_found | contents:read; pytest/cdk synth only |

## Candidate outcomes

- reportable: SSTI, SSRF, two GitHub tool instances, two pipeline admin instances
- suppressed: Cognito password policy, shared task-response role
