# Threat Model: Amazon Bedrock Serverless Prompt Chaining

## Overview

This repository is an AWS sample that demonstrates serverless prompt chaining with Amazon Bedrock, AWS Step Functions, Amazon Bedrock Flows, and a Streamlit demo web application. Operators deploy CDK stacks that create Step Functions state machines, Lambda functions, optional Bedrock Agents, an HTTPS Streamlit UI behind an ALB with Cognito authentication, S3 storage for trip itinerary PDFs, Secrets Manager for a GitHub token, CloudWatch alarms, and an optional CodePipeline that deploys and tests the demos.

Primary product/runtime surfaces:

- Streamlit webapp (`webapp/`) invoking named Step Functions demos and rendering model outputs (blog post, story writer, trip planner PDF, movie pitch human-in-the-loop, meal planner, most-popular-repo agents).
- Lambda handlers under `functions/` for JSON schema validation, map-output merge, human-input pause, meal winner selection, PDF generation (`md2pdf`/WeasyPrint), and GitHub agent tools (trending scrape + README fetch with a PAT).
- CDK orchestration stacks under `stacks/` and technique samples under `techniques_step_functions/` and `techniques_bedrock_flows/`.
- Optional CI/CD under `pipeline/` that self-mutates and deploys the application with broad IAM.

Docs, specs, and `proof/` artifacts are development/assurance material, not the live attack surface, unless they document runtime configuration.

## Threat Model, Trust Boundaries, and Assumptions

### Assets and privileges that matter

- AWS account privileges used by Step Functions, Lambdas, ECS/Fargate task role, Bedrock agents, and especially CodeBuild deploy roles.
- GitHub personal access token in Secrets Manager (`BedrockPromptChainGitHubToken`) used to read repository READMEs.
- Cognito user pool identities for the demo webapp and ALB authentication.
- Customer/demo user prompt text and generated content (blog posts, itineraries, movie pitches).
- S3 itinerary PDFs and their short-lived presigned URLs.
- Step Functions task tokens for human-in-the-loop movie pitch approvals.
- Model invocation spend and throttling budgets on Bedrock.

### Trust boundaries

1. **Internet browser → ALB/Cognito → Streamlit (ECS)**  
   Unauthenticated users should only hit Cognito login; authenticated demo users submit free-text inputs and receive model outputs.

2. **Streamlit task role → Step Functions / Bedrock / AWS APIs**  
   The ECS task role can start and read the named demo state machines and send task success for wait-for-token workflows. All Cognito users share this backend privilege.

3. **Step Functions → Lambda / Bedrock InvokeModel / Bedrock Agents**  
   Workflow definitions control prompts, retries, and which Lambda tools run. Execution input is largely user- or model-influenced.

4. **Lambda → external systems**  
   - PDF Lambda → local WeasyPrint rendering and S3 put/get + presign.  
   - GitHub action Lambdas → `https://github.com/trending` (unauthenticated HTTP) and GitHub API with a secret PAT.  
   - Agent Lambdas → Bedrock Agent Runtime.

5. **CI/CD → AWS account**  
   CodePipeline/CodeBuild roles that deploy stacks are a high-privilege control plane separate from the demo UI.

6. **Technique stacks / local docker-compose**  
   Local compose binds host `~/.aws` into the container for developer demos; technique stacks are educational and may be deployed separately.

### Assumptions

- Deployed demos are intended for trusted operators and invited Cognito users, not arbitrary public self-signup (`self_sign_up_enabled=False`).
- GitHub PATs are operator-provisioned; least-privilege PAT scope is an operator responsibility but code should still constrain tool use.
- Bedrock model outputs are untrusted content when fed into parsers, PDF renderers, or further tools.
- No multi-tenant isolation beyond Cognito authentication; the sample is a shared demo account pattern.

### Attacker-controlled vs operator-controlled inputs

**Attacker / demo-user controlled (when authenticated to the webapp or able to start state machines):**

- Free-text fields: novel title, story description, trip location, movie description, meal ingredients.
- Human choices on movie pitch greenlight (yes/no) and continuation payload fields returned with task tokens.
- Indirectly: model outputs that are re-injected into later prompts, JSON repair loops, PDF markdown, or agent tool arguments.
- Indirectly: content of the public GitHub Trending page and public READMEs consumed by tools.

**Operator / deployer controlled:**

- CDK parameters (parent domain), Secrets Manager token value and scopes, Cognito users, pipeline connection to GitHub, IAM of deploy roles, whether pipeline is deployed at all.

**Developer-controlled only:**

- Local docker-compose, unit tests, proof harnesses, technique test inputs.

## Attack Surface, Mitigations, and Attacker Stories

### Important vulnerability classes in this repository context

1. **Injection into document/PDF renderers** — User or model markdown reaching `md2pdf`/WeasyPrint can trigger template evaluation, HTML rendering, or outbound URL fetches (SSTI, SSRF, local file read).
2. **LLM tool privilege abuse / prompt injection** — Agents with GitHub PAT-backed tools can be steered (directly or via scraped content) to access repositories outside the intended trending/public set if the token allows it.
3. **Overly broad IAM** — Especially CodeBuild `actions: ["*"], resources: ["*"]` for deploy stages; also any accidental wildcard on data-plane roles.
4. **Task-token / workflow confused deputy** — Shared ability to `SendTaskSuccess` and read execution history could let a compromised UI backend finish another user's paused workflow.
5. **Prompt injection for cost/DoS and content integrity** — Expected residual risk for generative demos; severity depends on sinks beyond the model (PDF, tools, AWS side effects).
6. **Authn/authz of the webapp** — Cognito at ALB is the primary gate; weak password policy and shared backend roles reduce defense in depth.
7. **Secret handling** — GitHub token only in Secrets Manager (good); local compose mounting AWS credentials (dev-only risk).
8. **JSON parsing of model output** — Schema validation with retry/fix loop; schema is developer-defined, so classic validator attacks are lower risk unless schema becomes attacker-controlled.

### Existing mitigations observed

- Cognito authentication on the ALB with self-signup disabled; default listener returns 403 for non-matching hosts.
- S3 itinerary bucket blocks public access; objects expire via lifecycle; presigned URLs expire in 15 minutes.
- Bedrock invoke IAM for app roles is scoped to Claude/Nova foundation models and inference profiles rather than `*`.
- GitHub agent Lambda resource policy conditions `aws:SourceAccount` / `aws:SourceArn` for Bedrock agents.
- README content truncation (5,000 chars) limits some prompt-injection payload size (not a complete control).
- Strands lookup validates structured GitHub URL format for the trending-repo selection step.
- JSON response parsing validates against fixed schemas with bounded repair attempts.
- No obvious hardcoded cloud credentials in source.

### Realistic attacker stories

- Authenticated demo user supplies a malicious trip **location** that is embedded into markdown and processed by `md2pdf`, achieving SSTI or causing WeasyPrint to fetch internal/file URLs during PDF creation.
- Authenticated user (or attacker who can start the most-popular-repo workflows) triggers agent tools; malicious trending/README content or agent steering causes README fetches for private repositories accessible to the configured PAT; summaries surface in the UI.
- Attacker who can modify the pipeline source branch or compromise the CodeStar connection pushes code that the pipeline deploys using admin-equivalent CodeBuild roles, taking over the AWS account.
- Compromised Streamlit process uses the shared task role to list executions and complete another user's movie-pitch task token.

### Out-of-scope / less relevant attacker stories

- Unauthenticated internet exploitation of Streamlit pages when Cognito and ALB rules are deployed as designed (login required).
- Pure model-output quality / bias issues without a security sink.
- Specs/`proof/` documentation correctness as a runtime exploit path.
- Attacks that require the operator to already be root in the AWS account, except where the finding is privilege escalation from a lower CI or demo role.

## Severity Calibration

### Critical

- Unauthenticated remote code execution or account takeover of the AWS account.
- Unauthenticated exfiltration of the GitHub PAT or other account-wide secrets.
- Example: public unauthenticated path to SSTI/RCE in a Lambda that can assume broad roles (not the designed ALB+Cognito path).

### High

- Authenticated demo user achieves RCE in Lambda via PDF/template injection, or can pivot to meaningful AWS credentials/data beyond their own itinerary.
- CI/CD deploy roles with unrestricted `*:*` that a repository contributor or source-compromise can exercise to take over the deployment account.
- Cross-user workflow takeover that changes security-relevant decisions at scale when multi-user demos are exposed.

### Medium

- SSRF/local file fetch from the PDF renderer with Lambda network identity, without full RCE.
- Agent tools that can read arbitrary repositories the PAT can access when combined with realistic prompt injection and a broader-than-needed PAT.
- Missing allowlists / weak validation on tool inputs that expand blast radius of model compromise.

### Low

- Weak Cognito password complexity settings for an invite-only demo pool.
- Benign information leaks in agent error strings.
- Residual prompt-injection that only affects generated prose without tool/PDF/AWS side effects.
- Local docker-compose mounting developer AWS credentials (developer workstation trust model).

Repository: target_sha256_9c826f8d9cc2afc996b79e2289250a22b530769679c01fccbc0c30eb7a86c6d4
Version: 92098a6052a8dae63f3cf4becd066489704c7068
