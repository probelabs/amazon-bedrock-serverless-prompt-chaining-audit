# Security Review: workspace

## Scope

Repository-wide standard security scan of the Amazon Bedrock serverless prompt-chaining sample (Streamlit webapp, Step Functions/Bedrock Flows demos, Lambdas, CDK stacks, and optional CodePipeline).

- Scan mode: repository
- Target kind: git_worktree
- Target ID: target_sha256_9c826f8d9cc2afc996b79e2289250a22b530769679c01fccbc0c30eb7a86c6d4
- Revision: 92098a6052a8dae63f3cf4becd066489704c7068
- Snapshot digest: codex-security-snapshot/v1:sha256:711374b23039d4108d030d214aa09c1799528d726c8449bf8afad28df36fd060
- Inventory strategy: repository
- Included paths: .
- Excluded paths: none
- Runtime or test status: Static review with dependency source inspection and local Jinja SSTI probes; AWS runtime (Lambda/ECS) not executed in this host.
- Artifacts reviewed: artifacts/01_context/threat_model.md, artifacts/01_context/security_guidance.md, artifacts/02_discovery/in_scope_files.txt, artifacts/02_discovery/candidate_ledger.jsonl, artifacts/03_coverage/repository_coverage_ledger.md
- Scan context: Threat model generated during this scan; no repository SECURITY.md policy found.

Limitations and exclusions:
- No live AWS deployment, Bedrock invocation, or WeasyPrint native runtime in this environment.
- GitHub PAT scopes are operator-configured and not present in the repository.
- PNG screenshots and binary assets were inventoried without pixel-level analysis.
- Excluded \*\*/.git/\*\*: VCS metadata excluded from review inventory tooling
- Excluded \*\*/__pycache__/\*\*: Bytecode cache not security source

### Scan Summary

| Field | Value |
| --- | --- |
| Reportable findings | 6 |
| Severity mix | high: 3, medium: 3 |
| Confidence mix | high: 6 |
| Coverage | complete |
| Validation mode | compact standard-scan static validation with library-source confirmation and Jinja probe artifacts |

Canonical artifacts: `scan-manifest.json`, `findings.json`, and `coverage.json`. This report is a deterministic projection of those files.

## Threat Model

AWS sample for serverless Bedrock prompt chaining with a Cognito-protected Streamlit UI, Step Functions/Lambda workflows, GitHub-PAT agent tools, S3 PDF generation, and an optional high-privilege CodePipeline. Primary risks are untrusted content reaching PDF/template renderers, over-broad agent tool access to GitHub with a PAT, and unrestricted CI deploy roles.

### Assets

- AWS account privileges (especially CodeBuild deploy roles)
- GitHub PAT in Secrets Manager
- Cognito demo user access
- User prompts and generated content
- S3 itinerary PDFs and presigned URLs
- Step Functions task tokens

### Trust Boundaries

- Internet browser to ALB/Cognito to Streamlit ECS
- Shared ECS task role to Step Functions APIs
- Step Functions to Lambda/Bedrock/tools
- Lambda to GitHub API, S3, and WeasyPrint fetches
- CodePipeline/CodeBuild to AWS control plane

### Attacker Capabilities

- Authenticated Cognito demo user submitting free-text workflow inputs
- Indirect influence via model outputs and scraped GitHub content
- Pipeline source or CodeStar connection compromise for CI stages

### Security Objectives

- Prevent RCE/SSTI and SSRF from demo inputs
- Constrain GitHub PAT tool use to intended public repositories
- Keep deploy-time IAM least-privilege
- Preserve Cognito gate on the demo UI

### Assumptions

- Demos are invite-only Cognito users when webapp stack is deployed as designed
- Model outputs are untrusted when fed to tools and renderers
- GitHub PAT scope is an operator choice the code should still constrain

## Findings

| Finding | Severity | Confidence | Detailed write-up |
| --- | --- | --- | --- |
| [DeployExamples CodeBuild role grants actions=\* on resources=\*](#finding-1) | high | high | inline below |
| [DeployDemoApp CodeBuild role grants actions=\* on resources=\*](#finding-2) | high | high | inline below |
| [Trip planner PDF path evaluates attacker-controlled markdown as Jinja2 (SSTI)](#finding-3) | high | high | inline below |
| [Trip planner PDF rendering can fetch attacker-controlled URLs via WeasyPrint](#finding-4) | medium | high | inline below |
| [Bedrock GitHub agent action fetches arbitrary repository READMEs with a shared PAT](#finding-5) | medium | high | inline below |
| [Strands GitHub README tool uses the PAT without an allowlist](#finding-6) | medium | high | inline below |

### Confidence Scale

| Label | Meaning |
| --- | --- |
| high | Direct evidence supports the finding with no material unresolved blocker. |
| medium | Evidence supports a plausible issue, but material runtime or reachability proof remains. |
| low | Evidence is incomplete and the item is retained only for explicit follow-up. |

<a id="finding-1"></a>

### [1] DeployExamples CodeBuild role grants actions=\* on resources=\*

| Field | Value |
| --- | --- |
| Severity | high |
| Confidence | high |
| Confidence rationale | Explicit PolicyStatement(actions=\['\*'\], resources=\['\*'\]) in pipeline_stack.py. |
| Category | insecure-configuration |
| CWE | CWE-269, CWE-250 |
| Affected lines | pipeline/pipeline_stack.py:167-169, pipeline/pipeline_stack.py:150-169 |

#### Summary

The pipeline's DeployExamples CodeBuild project receives an IAM policy allowing all actions on all resources while running cdk deploy with --require-approval=never. Compromise of pipeline source or the CodeBuild execution therefore yields account-admin equivalent privileges.

#### Root Cause

The DeployExamples CodeBuild service role is granted unrestricted IAM (actions=\*, resources=\*), so any code executed in that project can administer the entire account.

**pipeline/pipeline_stack.py:167** — `pipeline/pipeline_stack.py:167-169`

Missing or broken security control that should constrain the untrusted value.

```python
        deploy_examples_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

**pipeline/pipeline_stack.py:150** — `pipeline/pipeline_stack.py:150-169`

Supporting wiring that preserves attacker control into the sink.

```python
                            ],
                        },
                        "build": {
                            "commands": [
                                "cd techniques_step_functions/",
                                "cdk deploy --app 'python3 technique_stacks.py' --all --require-approval=never",
                                "cd ../techniques_bedrock_flows/",
                                "cdk deploy --app 'python3 technique_stacks.py' --all --require-approval=never",
                            ]
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5
            ),
        )
        deploy_examples_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

#### Validation

pipeline_stack.py deploy_examples_project.add_to_role_policy(PolicyStatement(actions=\['\*'\], resources=\['\*'\])).

Validation method: static source trace

**pipeline/pipeline_stack.py:167** — `pipeline/pipeline_stack.py:167-169`

Missing or broken security control that should constrain the untrusted value.

```python
        deploy_examples_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

**pipeline/pipeline_stack.py:150** — `pipeline/pipeline_stack.py:150-169`

Supporting wiring that preserves attacker control into the sink.

```python
                            ],
                        },
                        "build": {
                            "commands": [
                                "cd techniques_step_functions/",
                                "cdk deploy --app 'python3 technique_stacks.py' --all --require-approval=never",
                                "cd ../techniques_bedrock_flows/",
                                "cdk deploy --app 'python3 technique_stacks.py' --all --require-approval=never",
                            ]
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5
            ),
        )
        deploy_examples_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

#### Dataflow

Malicious or compromised pipeline source -\> DeployExamples CodeBuild with \*:\* -\> cdk deploy can create/modify arbitrary account resources and IAM

- **Source:** Pipeline source artifact / CodeBuild execution of deploy stage

- **Sink:** IAM role policy \*:\*

- **Outcome:** Account-admin equivalent deploy role is a crown-jewel CI/CD failure. Likelihood medium because source control and connection compromise are non-trivial but standard pipeline threat models include them.

#### Reachability

Requires pipeline stack deployment and ability to influence the CodeStar-connected branch or CodeBuild execution. Not anonymous webapp users.

- **Attacker:** authenticated demo user or pipeline source influencer (per finding)

- **Entry point:** pipeline/pipeline_stack.py

- **Outcome:** Account-admin equivalent deploy role is a crown-jewel CI/CD failure. Likelihood medium because source control and connection compromise are non-trivial but standard pipeline threat models include them.

#### Severity

**High** — Unrestricted deploy-time IAM is a crown-jewel CI/CD weakness. Likelihood is medium because source-control compromise is non-trivial, but pipeline threat models treat it as in-scope.

Lower if the pipeline stack is never deployed or a permissions boundary blocks star-star. Raise toward critical if untrusted contributors can trigger deploy without review.

#### Remediation

Replace Action=\* Resource=\* with least-privilege permissions required for the specific CDK deployments (CloudFormation, targeted service APIs, scoped IAM PassRole), and attach a permissions boundary that forbids unrestricted admin.

Tests:
- Assert DeployExamples project role policies do not contain Action=\* with Resource=\*.
- Policy unit test: cdk deploy of technique stacks succeeds with the reduced policy set in a test account.

Preventive controls:
- Use cdk-nag or IAM Access Analyzer checks in CI to fail on unrestricted deploy roles.
- Require manual approval actions before deploy stages.

<a id="finding-2"></a>

### [2] DeployDemoApp CodeBuild role grants actions=\* on resources=\*

| Field | Value |
| --- | --- |
| Severity | high |
| Confidence | high |
| Confidence rationale | Explicit star-star policy on deploy_project in pipeline_stack.py. |
| Category | insecure-configuration |
| CWE | CWE-269, CWE-250 |
| Affected lines | pipeline/pipeline_stack.py:286-288, pipeline/pipeline_stack.py:270-288 |

#### Summary

The DeployDemoApp CodeBuild project is also granted actions=\['\*'\] and resources=\['\*'\] for cdk deploy --all --require-approval=never, providing a second account-admin equivalent deploy principal.

#### Root Cause

The DeployDemoApp CodeBuild service role is granted unrestricted IAM (actions=\*, resources=\*), creating a second account-admin deploy principal.

**pipeline/pipeline_stack.py:286** — `pipeline/pipeline_stack.py:286-288`

Missing or broken security control that should constrain the untrusted value.

```python
        deploy_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

**pipeline/pipeline_stack.py:270** — `pipeline/pipeline_stack.py:270-288`

Supporting wiring that preserves attacker control into the sink.

```python
                                "source .venv/bin/activate",
                                "pip install -r requirements.txt",
                            ],
                        },
                        "build": {
                            "commands": [
                                "cdk deploy --app 'python3 cdk_stacks.py' --all --require-approval=never",
                            ]
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5
            ),
        )
        deploy_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

#### Validation

deploy_project.add_to_role_policy(PolicyStatement(actions=\['\*'\], resources=\['\*'\])).

Validation method: static source trace

**pipeline/pipeline_stack.py:286** — `pipeline/pipeline_stack.py:286-288`

Missing or broken security control that should constrain the untrusted value.

```python
        deploy_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

**pipeline/pipeline_stack.py:270** — `pipeline/pipeline_stack.py:270-288`

Supporting wiring that preserves attacker control into the sink.

```python
                                "source .venv/bin/activate",
                                "pip install -r requirements.txt",
                            ],
                        },
                        "build": {
                            "commands": [
                                "cdk deploy --app 'python3 cdk_stacks.py' --all --require-approval=never",
                            ]
                        },
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5
            ),
        )
        deploy_project.add_to_role_policy(
            iam.PolicyStatement(actions=["*"], resources=["*"])
        )
```

#### Dataflow

Pipeline source -\> DeployDemoApp CodeBuild \*:\* -\> cdk deploy --all of demo stacks

- **Source:** Pipeline source artifact / CodeBuild execution of DeployDemoApp

- **Sink:** IAM role policy \*:\*

- **Outcome:** Second admin-equivalent deploy stage; same severity class.

#### Reachability

Same class as DeployExamples; independent role attachment.

- **Attacker:** authenticated demo user or pipeline source influencer (per finding)

- **Entry point:** pipeline/pipeline_stack.py

- **Outcome:** Second admin-equivalent deploy stage; same severity class.

#### Severity

**High** — Independent unrestricted deploy role with the same account-takeover impact class as DeployExamples.

Same as the DeployExamples admin instance.

#### Remediation

Scope the DeployDemoApp role to the demo application services and CloudFormation resources it must manage; remove blanket admin.

Tests:
- Assert DeployDemoApp role policies do not contain Action=\* with Resource=\*.
- Deploy demo stacks in a sandbox with the reduced policy and confirm success without admin.

Preventive controls:
- Split bootstrap/admin pipeline updates from application deploy roles.
- Enforce permission boundaries on all CodeBuild service roles.

<a id="finding-3"></a>

### [3] Trip planner PDF path evaluates attacker-controlled markdown as Jinja2 (SSTI)

| Field | Value |
| --- | --- |
| Severity | high |
| Confidence | high |
| Confidence rationale | Direct source-to-sink trace plus md2pdf 3.1.1 source showing unconditional Jinja render, confirmed with local Jinja probes exposing builtins. |
| Category | ssti |
| CWE | CWE-1336, CWE-94 |
| Affected lines | functions/trip_planner/pdf_creator/index.py:15-33, functions/trip_planner/pdf_creator/index.py:30-33, webapp/pages/3_Trip_Planner.py:72-81, webapp/pages/3_Trip_Planner.py:38-44, stacks/trip_planner_stack.py:164-168 |

#### Summary

The trip planner PDF Lambda embeds the user-supplied trip location and model itinerary into a markdown string and passes it to md2pdf(), which always runs unsandboxed jinja2.Template(raw).render() before HTML/PDF conversion. An authenticated demo user can therefore achieve server-side template injection and code execution inside the Lambda.

#### Root Cause

The violated invariant is that untrusted workflow input must not be evaluated as a template. pdf_creator interpolates location and itinerary into a raw markdown string and hands it to md2pdf, which always executes jinja2.Template(raw).render() with no sandbox.

**functions/trip_planner/pdf_creator/index.py:15** — `functions/trip_planner/pdf_creator/index.py:15-33`

Missing or broken security control that should constrain the untrusted value.

```python
    location = event["location"]
    itinerary_content = f"""
# Your Weekend Vacation

Here is your three day itinerary for your visit to {location}, created by generative AI.  Enjoy!

{event["itinerary"]}
"""

    s3_object_key = f"itinerary-{uuid.uuid4()}.pdf"

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_tmp:
        pdf_tmp_path = pdf_tmp.name

    try:
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**functions/trip_planner/pdf_creator/index.py:30** — `functions/trip_planner/pdf_creator/index.py:30-33`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**webapp/pages/3_Trip_Planner.py:72** — `webapp/pages/3_Trip_Planner.py:72-81`

User-facing or pipeline entry that starts the vulnerable path.

```python
        location_text = st.text_input(
            "Enter a location for your trip:", "Paris, France"
        )
        started = st.form_submit_button("Start")
        if started:
            with st.spinner("Wait for it..."):
                if "trip_planner_execution_arn" in st.session_state:
                    del st.session_state["trip_planner_execution_arn"]
                display_no_state_machine_status()
                response = execute_state_machine(location_text)
```

**webapp/pages/3_Trip_Planner.py:38** — `webapp/pages/3_Trip_Planner.py:38-44`

Attacker-influenced value is accepted here and forwarded into the workflow or tool path.

```python
def execute_state_machine(location):
    input = {"location": location}
    execution_arn = stepfn.start_execution(
        "PromptChainDemo-TripPlanner",
        st.session_state.user_id,
        json.dumps(input),
    )
```

#### Validation

pdf_creator/index.py interpolates location/itinerary into raw markdown and calls md2pdf. Extracted md2pdf/core.py shows Template(raw).render(context) before markdown/WeasyPrint. Jinja2 Template('{{7\*7}}').render() =\> '49'; Template accessing self.__init__.__globals__.__builtins__ returns builtins including eval/exec/open.

Validation method: static source trace + library behavior confirmation

**functions/trip_planner/pdf_creator/index.py:15** — `functions/trip_planner/pdf_creator/index.py:15-33`

Missing or broken security control that should constrain the untrusted value.

```python
    location = event["location"]
    itinerary_content = f"""
# Your Weekend Vacation

Here is your three day itinerary for your visit to {location}, created by generative AI.  Enjoy!

{event["itinerary"]}
"""

    s3_object_key = f"itinerary-{uuid.uuid4()}.pdf"

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_tmp:
        pdf_tmp_path = pdf_tmp.name

    try:
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**functions/trip_planner/pdf_creator/index.py:30** — `functions/trip_planner/pdf_creator/index.py:30-33`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**webapp/pages/3_Trip_Planner.py:72** — `webapp/pages/3_Trip_Planner.py:72-81`

User-facing or pipeline entry that starts the vulnerable path.

```python
        location_text = st.text_input(
            "Enter a location for your trip:", "Paris, France"
        )
        started = st.form_submit_button("Start")
        if started:
            with st.spinner("Wait for it..."):
                if "trip_planner_execution_arn" in st.session_state:
                    del st.session_state["trip_planner_execution_arn"]
                display_no_state_machine_status()
                response = execute_state_machine(location_text)
```

**webapp/pages/3_Trip_Planner.py:38** — `webapp/pages/3_Trip_Planner.py:38-44`

Attacker-influenced value is accepted here and forwarded into the workflow or tool path.

```python
def execute_state_machine(location):
    input = {"location": location}
    execution_arn = stepfn.start_execution(
        "PromptChainDemo-TripPlanner",
        st.session_state.user_id,
        json.dumps(input),
    )
```

#### Dataflow

Cognito user enters location in Trip Planner -\> Streamlit start_execution(PromptChainDemo-TripPlanner, {location}) -\> Step Functions passes $$.Execution.Input.location to PDF Lambda -\> f-string markdown -\> md2pdf Jinja2 Template.render -\> attacker code runs in Lambda

- **Source:** webapp/pages/3_Trip_Planner.py location_text -\> stepfn.start_execution input.location

- **Sink:** md2pdf(..., raw=itinerary_content) -\> jinja2.Template(raw).render()

- **Outcome:** Authenticated users get server-side template injection leading to code execution in the PDF Lambda. Not critical because Cognito authentication is required and the Lambda IAM is relatively narrow (S3 itinerary), but RCE on a production demo path is high.

#### Reachability

Authenticated demo user (or any caller of the state machine). No special admin role required beyond normal webapp use.

- **Attacker:** authenticated demo user or pipeline source influencer (per finding)

- **Entry point:** webapp/pages/3_Trip_Planner.py

- **Outcome:** Authenticated users get server-side template injection leading to code execution in the PDF Lambda. Not critical because Cognito authentication is required and the Lambda IAM is relatively narrow (S3 itinerary), but RCE on a production demo path is high.

#### Severity

**High** — Authenticated users reach unsandboxed Jinja2 evaluation on a live demo workflow, yielding code execution in the PDF Lambda. Not critical because Cognito authentication is required in the designed deployment and the Lambda role is relatively narrow.

Raise to critical if the webapp is exposed without Cognito or the Lambda role is broadened. Lower only if untrusted strings are never Jinja-rendered (verified).

#### Remediation

Do not pass untrusted content through Jinja. Prefer a markdown-to-PDF path that disables template rendering, or escape/sandbox untrusted strings before any template engine; treat location and itinerary as data only.

Tests:
- Assert that a location value containing {{7\*7}} appears literally in the markdown passed to the renderer and is not evaluated to 49.
- Assert that payloads accessing self.__init__.__globals__ do not execute during PDF generation.

Preventive controls:
- Centralize document rendering behind a helper that forbids template evaluation of user/model content.
- Add an allowlist of safe markdown constructs and strip HTML/template syntax from location input at the webapp boundary.

<a id="finding-4"></a>

### [4] Trip planner PDF rendering can fetch attacker-controlled URLs via WeasyPrint

| Field | Value |
| --- | --- |
| Severity | medium |
| Confidence | high |
| Confidence rationale | md2pdf/WeasyPrint code paths show default URL fetching; untrusted markdown is under user/model control on the same PDF path. |
| Category | ssrf |
| CWE | CWE-918 |
| Affected lines | functions/trip_planner/pdf_creator/index.py:15-33, functions/trip_planner/pdf_creator/index.py:30-33, webapp/pages/3_Trip_Planner.py:72-81 |

#### Summary

Untrusted trip location and model-generated itinerary markdown are converted to HTML and rendered with WeasyPrint through md2pdf. WeasyPrint's default URL fetcher retrieves remote and file resources referenced by the document, enabling SSRF or local file access from the Lambda execution environment.

#### Root Cause

Untrusted markdown reaches HTML/PDF rendering without a restricted URL fetcher or sanitizer, so document-linked http(s)/file resources are retrieved with the Lambda network identity.

**functions/trip_planner/pdf_creator/index.py:15** — `functions/trip_planner/pdf_creator/index.py:15-33`

Missing or broken security control that should constrain the untrusted value.

```python
    location = event["location"]
    itinerary_content = f"""
# Your Weekend Vacation

Here is your three day itinerary for your visit to {location}, created by generative AI.  Enjoy!

{event["itinerary"]}
"""

    s3_object_key = f"itinerary-{uuid.uuid4()}.pdf"

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_tmp:
        pdf_tmp_path = pdf_tmp.name

    try:
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**functions/trip_planner/pdf_creator/index.py:30** — `functions/trip_planner/pdf_creator/index.py:30-33`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**webapp/pages/3_Trip_Planner.py:72** — `webapp/pages/3_Trip_Planner.py:72-81`

User-facing or pipeline entry that starts the vulnerable path.

```python
        location_text = st.text_input(
            "Enter a location for your trip:", "Paris, France"
        )
        started = st.form_submit_button("Start")
        if started:
            with st.spinner("Wait for it..."):
                if "trip_planner_execution_arn" in st.session_state:
                    del st.session_state["trip_planner_execution_arn"]
                display_no_state_machine_status()
                response = execute_state_machine(location_text)
```

#### Validation

md2pdf uses markdown() then HTML(string=raw_html, base_url=cwd).write_pdf(). Weasyprint urls.py default_url_fetcher/URLFetcher.fetch performs outbound retrieval. Markdown image syntax and HTML resources become fetch targets.

Validation method: static source trace + dependency URL fetcher review

**functions/trip_planner/pdf_creator/index.py:15** — `functions/trip_planner/pdf_creator/index.py:15-33`

Missing or broken security control that should constrain the untrusted value.

```python
    location = event["location"]
    itinerary_content = f"""
# Your Weekend Vacation

Here is your three day itinerary for your visit to {location}, created by generative AI.  Enjoy!

{event["itinerary"]}
"""

    s3_object_key = f"itinerary-{uuid.uuid4()}.pdf"

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_tmp:
        pdf_tmp_path = pdf_tmp.name

    try:
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**functions/trip_planner/pdf_creator/index.py:30** — `functions/trip_planner/pdf_creator/index.py:30-33`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
        md2pdf(
            pdf_tmp_path,
            raw=itinerary_content,
        )
```

**webapp/pages/3_Trip_Planner.py:72** — `webapp/pages/3_Trip_Planner.py:72-81`

User-facing or pipeline entry that starts the vulnerable path.

```python
        location_text = st.text_input(
            "Enter a location for your trip:", "Paris, France"
        )
        started = st.form_submit_button("Start")
        if started:
            with st.spinner("Wait for it..."):
                if "trip_planner_execution_arn" in st.session_state:
                    del st.session_state["trip_planner_execution_arn"]
                display_no_state_machine_status()
                response = execute_state_machine(location_text)
```

#### Dataflow

User/model content in PDF markdown -\> HTML conversion -\> WeasyPrint fetches linked http(s)/file URLs using Lambda network identity

- **Source:** location and itinerary strings in PDF markdown

- **Sink:** WeasyPrint HTML.write_pdf resource fetch

- **Outcome:** Classic document-renderer SSRF from authenticated input. Impact is network-position dependent; no proof of credential theft via IMDS in this scan.

#### Reachability

Same authenticated trip planner path. Markdown image/link syntax is sufficient.

- **Attacker:** authenticated demo user or pipeline source influencer (per finding)

- **Entry point:** webapp/pages/3_Trip_Planner.py

- **Outcome:** Classic document-renderer SSRF from authenticated input. Impact is network-position dependent; no proof of credential theft via IMDS in this scan.

#### Severity

**Medium** — Authenticated document-renderer SSRF is realistic; impact depends on what the Lambda network identity can reach. No live IMDS credential theft was proven in this scan.

Raise if the function can reach sensitive internal services or disclose secrets via file/URL fetch. Lower if a deny-by-default custom URL fetcher is enforced.

#### Remediation

Supply WeasyPrint with a custom URL fetcher that denies all network and file URLs by default (or allowlists only required static assets), and sanitize markdown to remove images/links/HTML that introduce URLs.

Tests:
- Assert PDF generation does not perform HTTP GETs when markdown contains !\[x\](http://example.invalid/poc).
- Assert file:// URLs in markdown do not read local filesystem content into the PDF pipeline.

Preventive controls:
- Run PDF rendering with network isolation (no egress) when external resources are not required.
- Disable raw HTML in markdown conversion where possible.

<a id="finding-5"></a>

### [5] Bedrock GitHub agent action fetches arbitrary repository READMEs with a shared PAT

| Field | Value |
| --- | --- |
| Severity | medium |
| Confidence | high |
| Confidence rationale | Handler and helper code show unrestricted get_repo/get_readme with PAT; OpenAPI schema leaves repo unconstrained. |
| Category | authorization-bypass |
| CWE | CWE-862, CWE-200 |
| Affected lines | functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:42-62, functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:81-93, stacks/most_popular_repo_bedrock_agent_stack.py:48-61 |

#### Summary

The Bedrock agent GitHub action Lambda accepts any repo parameter, strips only a https://github.com/ prefix, and uses the Secrets Manager GitHub PAT to read that repository's README. There is no allowlist binding the tool to the selected trending public repository, so a steered agent can access any repository the token can read.

#### Root Cause

The tool treats the model-supplied repo string as authorized input. After a prefix strip it authenticates with a PAT and reads any get_repo target the token can access, without binding to the intended trending public repository.

**functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:42** — `functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:42-62`

Missing or broken security control that should constrain the untrusted value.

```python
def get_github_repository_readme_agent_action(input):
    github_token_secret_value = secrets_client.get_secret_value(
        SecretId=github_token_secret_name
    )
    github_token = json.loads(github_token_secret_value["SecretString"])["token"]
    github_client = Github(auth=Auth.Token(github_token))

    repo_name = input.replace("https://github.com/", "")
    try:
        readme_content = (
            github_client.get_repo(repo_name)
            .get_readme()
            .decoded_content.decode("utf-8")
        )
        if len(readme_content) > 5000:
            response = f"Here are the first 5,000 characters of the README for {input}."
            response += "\n" + readme_content[:5000]
        else:
            response = f"Here are the full contents of the README for {input}."
            response += "\n" + readme_content
        return response
```

**functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:81** — `functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:81-93`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
        elif api_path == "/get_github_repository_readme":
            params = event["parameters"]
            if not params:
                response_code = 400
                response_body = {"error": "Missing parameter: repo"}
            else:
                repo_params = [p for p in params if p["name"] == "repo"]
                if not repo_params:
                    response_code = 400
                    response_body = {"error": "Missing parameter: repo"}
                else:
                    repo_url = repo_params[0]["value"]
                    body = get_github_repository_readme_agent_action(repo_url)
```

**stacks/most_popular_repo_bedrock_agent_stack.py:48** — `stacks/most_popular_repo_bedrock_agent_stack.py:48-61`

Supporting wiring that preserves attacker control into the sink.

```python
        github_secret = secrets.Secret.from_secret_name_v2(
            scope=self, id="GitHubToken", secret_name="BedrockPromptChainGitHubToken"
        )
        github_agent_actions_lambda = lambda_python.PythonFunction(
            self,
            "GitHubAgentActions",
            function_name="PromptChainDemo-MostPopularRepoBedrockAgents-GitHubActions",
            runtime=lambda_.Runtime.PYTHON_3_13,
            entry="functions/most_popular_repo_bedrock_agent/github_agent_actions",
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={"GITHUB_TOKEN_SECRET": github_secret.secret_name},
        )
        github_secret.grant_read(github_agent_actions_lambda)
```

#### Validation

get_github_repository_readme_agent_action strips only https://github.com/ prefix and calls get_repo().get_readme() with Secrets Manager token. Handler passes repo query parameter unsanitized.

Validation method: static source trace

**functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:42** — `functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:42-62`

Missing or broken security control that should constrain the untrusted value.

```python
def get_github_repository_readme_agent_action(input):
    github_token_secret_value = secrets_client.get_secret_value(
        SecretId=github_token_secret_name
    )
    github_token = json.loads(github_token_secret_value["SecretString"])["token"]
    github_client = Github(auth=Auth.Token(github_token))

    repo_name = input.replace("https://github.com/", "")
    try:
        readme_content = (
            github_client.get_repo(repo_name)
            .get_readme()
            .decoded_content.decode("utf-8")
        )
        if len(readme_content) > 5000:
            response = f"Here are the first 5,000 characters of the README for {input}."
            response += "\n" + readme_content[:5000]
        else:
            response = f"Here are the full contents of the README for {input}."
            response += "\n" + readme_content
        return response
```

**functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:81** — `functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py:81-93`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
        elif api_path == "/get_github_repository_readme":
            params = event["parameters"]
            if not params:
                response_code = 400
                response_body = {"error": "Missing parameter: repo"}
            else:
                repo_params = [p for p in params if p["name"] == "repo"]
                if not repo_params:
                    response_code = 400
                    response_body = {"error": "Missing parameter: repo"}
                else:
                    repo_url = repo_params[0]["value"]
                    body = get_github_repository_readme_agent_action(repo_url)
```

**stacks/most_popular_repo_bedrock_agent_stack.py:48** — `stacks/most_popular_repo_bedrock_agent_stack.py:48-61`

Supporting wiring that preserves attacker control into the sink.

```python
        github_secret = secrets.Secret.from_secret_name_v2(
            scope=self, id="GitHubToken", secret_name="BedrockPromptChainGitHubToken"
        )
        github_agent_actions_lambda = lambda_python.PythonFunction(
            self,
            "GitHubAgentActions",
            function_name="PromptChainDemo-MostPopularRepoBedrockAgents-GitHubActions",
            runtime=lambda_.Runtime.PYTHON_3_13,
            entry="functions/most_popular_repo_bedrock_agent/github_agent_actions",
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={"GITHUB_TOKEN_SECRET": github_secret.secret_name},
        )
        github_secret.grant_read(github_agent_actions_lambda)
```

#### Dataflow

Workflow invokes Bedrock agent -\> agent calls GitHubAPIs /get_github_repository_readme with attacker/model-chosen repo -\> PAT-authenticated get_readme -\> contents returned to agent/UI summary

- **Source:** Bedrock agent tool parameter repo (model/tool-chosen; influenceable via tool-visible content)

- **Sink:** Github.get_repo().get_readme() with PAT

- **Outcome:** Missing tool allowlist is a real broken control. Severity medium because confidential impact depends on PAT scope and successful agent steering, which is realistic for agent systems but not guaranteed.

#### Reachability

Any principal that can start PromptChainDemo-MostPopularRepoBedrockAgents (webapp users). Steering may use indirect prompt injection via trending page/README content.

- **Attacker:** authenticated demo user or pipeline source influencer (per finding)

- **Entry point:** functions/most_popular_repo_bedrock_agent/github_agent_actions/index.py

- **Outcome:** Missing tool allowlist is a real broken control. Severity medium because confidential impact depends on PAT scope and successful agent steering, which is realistic for agent systems but not guaranteed.

#### Severity

**Medium** — Broken tool authorization is clear; confidential impact requires an over-scoped PAT and successful agent/tool steering (including via indirect prompt injection).

Raise to high if the PAT is documented/expected to access private organization repositories or if forced tool invocation is demonstrated reliably. Lower if the tool enforces an allowlist of a single public repo URL selected earlier in the workflow.

#### Remediation

Allowlist README fetches to the single repository URL selected by the trending lookup step; validate strict https://github.com/{owner}/{repo} form; use a least-privilege PAT (public-only) and reject other hosts/paths.

Tests:
- Assert requests for repos other than the workflow-selected trending repo are rejected before GitHub API calls.
- Assert non-https or non-github hosts never reach get_repo.

Preventive controls:
- Pass the selected repo as a workflow-side argument rather than letting the model supply arbitrary tool parameters.
- Monitor/alert on GitHub API access to unexpected repositories.

<a id="finding-6"></a>

### [6] Strands GitHub README tool uses the PAT without an allowlist

| Field | Value |
| --- | --- |
| Severity | medium |
| Confidence | high |
| Confidence rationale | Tool implementation and summarize agent registration show unconstrained PAT usage. |
| Category | authorization-bypass |
| CWE | CWE-862, CWE-200 |
| Affected lines | functions/most_popular_repo_strands/index.py:54-91, functions/most_popular_repo_strands/index.py:71-76, stacks/most_popular_repo_strands_stack.py:46-58 |

#### Summary

The Strands get_github_repository_readme tool loads the shared GitHub PAT and fetches whatever repository string the agent supplies after a simple prefix strip. URL validation exists only for structured trending-repo extraction, not at this tool boundary.

#### Root Cause

The README tool boundary does not reuse the structured-output URL validator. Any agent-supplied string can trigger a PAT-authenticated get_readme.

**functions/most_popular_repo_strands/index.py:54** — `functions/most_popular_repo_strands/index.py:54-91`

Missing or broken security control that should constrain the untrusted value.

```python
@tool
def get_github_repository_readme(input: str) -> str:
    """Retrieves the content of a GitHub repository's README file.
    
    Use this when you need to get information about a specific GitHub repository. 
    Provide the URL of the GitHub repository as the input. The output will be 
    the contents of the readme.
    
    Args:
        input: The URL of the GitHub repository
    """
    github_token_secret_value = secrets_client.get_secret_value(
        SecretId=github_token_secret_name
    )
    github_token = json.loads(github_token_secret_value["SecretString"])["token"]
    github_client = Github(auth=Auth.Token(github_token))

    repo_name = input.replace("https://github.com/", "")
    try:
        readme_content = (
            github_client.get_repo(repo_name)
            .get_readme()
            .decoded_content.decode("utf-8")
        )
        if len(readme_content) > 5000:
            response = f"Here are the first 5,000 characters of the README for {input}, inside <readme></readme> XML tags."
            response += "\n<readme>"
            response += "\n" + readme_content[:5000]
        else:
            response = (
                f"Here is the README for {input}, inside <readme></readme> XML tags."
            )
            response += "\n<readme>"
            response += "\n" + readme_content
        response += "\n</readme>"
        return response
    except UnknownObjectException:
        return f"Could not find a README for the repository {input}. It may not exist in the repository."
```

**functions/most_popular_repo_strands/index.py:71** — `functions/most_popular_repo_strands/index.py:71-76`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
    repo_name = input.replace("https://github.com/", "")
    try:
        readme_content = (
            github_client.get_repo(repo_name)
            .get_readme()
            .decoded_content.decode("utf-8")
```

**stacks/most_popular_repo_strands_stack.py:46** — `stacks/most_popular_repo_strands_stack.py:46-58`

Supporting wiring that preserves attacker control into the sink.

```python
        summarize_repo_lambda = lambda_python.PythonFunction(
            self,
            "SummarizeRepoAgent",
            runtime=lambda_.Runtime.PYTHON_3_13,
            entry="functions/most_popular_repo_strands",
            handler="summarize_repo_readme_agent",
            bundling=get_lambda_bundling_options(),
            timeout=Duration.minutes(2),
            memory_size=512,
            environment={"GITHUB_TOKEN_SECRET": github_secret.secret_name},
        )
        summarize_repo_lambda.add_to_role_policy(get_bedrock_iam_policy_statement())
        github_secret.grant_read(summarize_repo_lambda)
```

#### Validation

get_github_repository_readme @tool uses token and get_repo(input.replace(...)) without Pydantic validation. summarize_repo_readme_agent constructs Agent(tools=\[get_github_repository_readme\]).

Validation method: static source trace

**functions/most_popular_repo_strands/index.py:54** — `functions/most_popular_repo_strands/index.py:54-91`

Missing or broken security control that should constrain the untrusted value.

```python
@tool
def get_github_repository_readme(input: str) -> str:
    """Retrieves the content of a GitHub repository's README file.
    
    Use this when you need to get information about a specific GitHub repository. 
    Provide the URL of the GitHub repository as the input. The output will be 
    the contents of the readme.
    
    Args:
        input: The URL of the GitHub repository
    """
    github_token_secret_value = secrets_client.get_secret_value(
        SecretId=github_token_secret_name
    )
    github_token = json.loads(github_token_secret_value["SecretString"])["token"]
    github_client = Github(auth=Auth.Token(github_token))

    repo_name = input.replace("https://github.com/", "")
    try:
        readme_content = (
            github_client.get_repo(repo_name)
            .get_readme()
            .decoded_content.decode("utf-8")
        )
        if len(readme_content) > 5000:
            response = f"Here are the first 5,000 characters of the README for {input}, inside <readme></readme> XML tags."
            response += "\n<readme>"
            response += "\n" + readme_content[:5000]
        else:
            response = (
                f"Here is the README for {input}, inside <readme></readme> XML tags."
            )
            response += "\n<readme>"
            response += "\n" + readme_content
        response += "\n</readme>"
        return response
    except UnknownObjectException:
        return f"Could not find a README for the repository {input}. It may not exist in the repository."
```

**functions/most_popular_repo_strands/index.py:71** — `functions/most_popular_repo_strands/index.py:71-76`

Dangerous operation that executes, fetches, or discloses based on the unconstrained value.

```python
    repo_name = input.replace("https://github.com/", "")
    try:
        readme_content = (
            github_client.get_repo(repo_name)
            .get_readme()
            .decoded_content.decode("utf-8")
```

**stacks/most_popular_repo_strands_stack.py:46** — `stacks/most_popular_repo_strands_stack.py:46-58`

Supporting wiring that preserves attacker control into the sink.

```python
        summarize_repo_lambda = lambda_python.PythonFunction(
            self,
            "SummarizeRepoAgent",
            runtime=lambda_.Runtime.PYTHON_3_13,
            entry="functions/most_popular_repo_strands",
            handler="summarize_repo_readme_agent",
            bundling=get_lambda_bundling_options(),
            timeout=Duration.minutes(2),
            memory_size=512,
            environment={"GITHUB_TOKEN_SECRET": github_secret.secret_name},
        )
        summarize_repo_lambda.add_to_role_policy(get_bedrock_iam_policy_statement())
        github_secret.grant_read(summarize_repo_lambda)
```

#### Dataflow

Strands summarize agent -\> get_github_repository_readme tool -\> PAT get_readme -\> summary to UI

- **Source:** Strands tool input string

- **Sink:** Github.get_repo().get_readme() with PAT

- **Outcome:** Sibling unrestricted PAT tool on Strands path with the same PAT-scope precondition.

#### Reachability

Webapp users starting MostPopularRepo Strands workflow; tool available to the agent during summarization.

- **Attacker:** authenticated demo user or pipeline source influencer (per finding)

- **Entry point:** functions/most_popular_repo_strands/index.py

- **Outcome:** Sibling unrestricted PAT tool on Strands path with the same PAT-scope precondition.

#### Severity

**Medium** — Same unrestricted PAT-backed README fetch pattern as the Bedrock agent actions path.

Same as the Bedrock agent README tool instance.

#### Remediation

Validate and allowlist tool input to the workflow-selected public repository; apply the same strict URL checks used in GitHubRepo.validate_github_url at the tool boundary before any PAT use.

Tests:
- Assert the README tool rejects repos not equal to the selected trending URL.
- Assert PAT is not loaded when validation fails.

Preventive controls:
- Prefer non-token public raw README fetch for public repos when authentication is unnecessary.
- Scope Secrets Manager token to public-only fine-grained PAT permissions.

## Reviewed Surfaces

| Surface | Risk Area | Outcome | Notes |
| --- | --- | --- | --- |
| Trip planner PDF generation | SSTI/SSRF | Reported | md2pdf Jinja SSTI and WeasyPrint URL fetch Evidence: artifacts/02_discovery/candidate_ledger.jsonl |
| GitHub agent README tools | Authorization/secrets | Reported | Bedrock actions and Strands tool unrestricted PAT use Evidence: artifacts/02_discovery/candidate_ledger.jsonl |
| CodePipeline deploy IAM | Privilege escalation | Reported | DeployExamples and DeployDemoApp star-star policies Evidence: artifacts/02_discovery/candidate_ledger.jsonl |
| Streamlit Cognito auth | Authentication | Rejected | Weak password complexity suppressed; invite-only pool Evidence: artifacts/02_discovery/candidate_ledger.jsonl |
| Shared ECS task role / task tokens | Confused deputy | Rejected | No direct user IDOR; needs prior compromise Evidence: artifacts/02_discovery/candidate_ledger.jsonl |
| JSON response parse/repair | Injection | No issue found | Developer-fixed schemas; bounded repair loop |
| Other prompt-chaining demos | Prompt injection | No issue found | Residual LLM integrity/cost without additional high-impact sinks |
| Technique SFN/Flows samples | Demo orchestration | No issue found | Educational stacks reviewed for dangerous sinks |
| Source secret scanning | Secrets | No issue found | No hardcoded cloud credentials found |
| docker-compose local AWS mount | Local development | Not applicable | Developer workstation trust model |
| Docs/specs/proof/tests | Non-runtime | Not applicable | Inventoried; not live privileged surfaces |

## Open Questions And Follow Up

- What scopes does the operator-provisioned BedrockPromptChainGitHubToken PAT actually have in real deployments?
- Is the optional pipeline stack deployed in the environments that matter for this sample?
