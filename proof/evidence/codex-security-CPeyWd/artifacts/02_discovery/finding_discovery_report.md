# Finding Discovery Report

Standard repository-wide review of 250 inventoried paths.

## Method

- Built deterministic `in_scope_files.txt` via `rg --files`.
- Reviewed runtime surfaces (webapp, functions, stacks, pipeline, techniques) and inventoried docs/tests/proof/binaries.
- Collected 8 raw candidates; normalized to 8 ledger rows.

## Candidates

| ID | Instance | Outcome after validation/attack-path |
| --- | --- | --- |
| candidate-8f0e6e3f7eec765a | location-field-ssti | reportable (high) |
| candidate-dc4100642a3b5dd9 | weasyprint-url-fetch | reportable (medium) |
| candidate-6bf5f309b08138e5 | bedrock-agent-readme-tool | reportable (medium) |
| candidate-842a695123c8fd05 | strands-readme-tool | reportable (medium) |
| candidate-c2876d1586f97a76 | deploy-examples-admin | reportable (high) |
| candidate-dca88aa80d196424 | deploy-demo-app-admin | reportable (high) |
| candidate-1a63a454e050fffb | cognito-password-policy | suppressed |
| candidate-815b49c8474b54dc | shared-task-response-role | suppressed |
