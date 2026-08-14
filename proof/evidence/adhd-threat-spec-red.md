# ADHD review — threat-kickoff + spec-red

Pack: threat-kickoff / spec-red (user opt-in). Mode: full (5 isolated frames).
Already-filed KIs (banned from diverge): pipeline `*:*,` md2pdf SSTI, WeasyPrint SSRF, PAT README allowlist.

## Brief

Re-review the Bedrock prompt-chaining sample and STK/SYS/SW/INT specs against an extended threat model. Prefer non-bool spec features.

## Converge (shortlist)

| ★ | Cluster | Score (N/V/F) | Trap? |
|---|---|---|---|
| ★ | Shared ECS role + task-token confused deputy (List/Describe/SendTaskSuccess) | 8.4 | Not OOS: Cognito users share the task role |
| ★ | Streamlit `requests.get(itinerary_url)` + SFN output harvest of others' presigns | 8.1 | Distinct from WeasyPrint SSRF |
| | PDF_BUCKET missing still returns URL / SUCCEEDED | 7.6 | |
| | Poller 1s + maxResults=1 hides waitForTaskToken | 7.4 | |
| | JSON-repair concatenates Cause into next prompt; no byte cap | 7.2 | |
| | pitch `string_matches 1*` forces Red | 7.0 | |
| | Meal `winning_score>0` hides ties / chef-key KeyError | 6.8 | |
| | Alarms only 7 demo SMs; techniques silent | 6.5 | |
| | GitHub trending GET no timeout; unanchored regex | 6.4 | |
| | Unbounded form fields / Map fan-out cost | 6.2 | DoS-ish; keep as spec range |
| trap | "bleach/batteries" meal list | — | Content-policy, not this sample's contract |
| trap | Invent new High without PoC | — | ADHD rule |

★ pick: verify token ownership + itinerary_url fetch in code, then file product KIs if confirmed. Specs get enums/ranges/tables for those paths.

## Handoff

hazard-sweep verify (not empty-success) → product KIs if real_novel → spec-review non-bool deepen.
