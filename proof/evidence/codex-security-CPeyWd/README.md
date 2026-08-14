# Codex security scan CPeyWd

Portable copy of
`/home/dev/.codex/state/plugins/codex-security/scans/workspace/codex-security-workspace-CPeyWd`
(scan id `2f573ce7-f9b5-4f17-a45c-bba7c5f59e5e`). Hazard-sweep discover returned
`[]`; these six items are product defects, not process KIs.

Canonical write-up: [report.md](report.md). Structured records: [findings.json](findings.json).

| # | Finding | KI id | file:line |
| --- | --- | --- | --- |
| 1 | DeployExamples CodeBuild role `actions=* resources=*` | KI-pipeline-deploy-examples-star-star | `pipeline/pipeline_stack.py:167-169` |
| 2 | DeployDemoApp CodeBuild role `actions=* resources=*` | KI-pipeline-deploy-demo-star-star | `pipeline/pipeline_stack.py:286-288` |
| 3 | Trip planner PDF interpolates location/itinerary into md2pdf raw (Jinja SSTI) | KI-pdf-md2pdf-ssti | `functions/trip_planner/pdf_creator/index.py:15-33` |
| 4 | Same path: WeasyPrint default URL fetcher (SSRF) | KI-pdf-weasyprint-ssrf | `functions/trip_planner/pdf_creator/index.py:15-33` |
| 5 | Bedrock `get_readme` uses PAT with no allowlist | KI-github-bedrock-readme-pat-no-allowlist | `functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:42-62` |
| 6 | Strands `get_github_repository_readme` uses PAT with no allowlist | KI-github-strands-readme-pat-no-allowlist | `functions/most_popular_repo_strands/index.py:54-91` |

Jinja library probe (finding 3):
`artifacts/02_discovery/validation_artifacts/candidate-8f0e6e3f7eec765a/jinja_ssti_probe.txt`
(`probe1: visit to 49`, `builtins_open_exposed: True`).
