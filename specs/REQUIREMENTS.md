# Requirements map

This document is documentation evidence for the ReqProof four-layer skeleton.

## Stakeholder

- Documents: STK-REQ-001 Demo user obtains a completed result for a named prompt-chaining application.
- Documents: STK-REQ-002 Operator receives a notification when a named demo workflow fails. Technique stacks are not alarmed.
- Documents: STK-REQ-003 Technique operator executes an isolated prompt-chaining technique example.

## System

- Documents: SYS-REQ-001 Demo orchestrator takes each named demo execution to a terminal state. Demo names are BlogPost, TripPlanner, StoryWriter, MoviePitch, MealPlanner, MostPopularRepoBedrockAgents, MostPopularRepoStrands. Ingress is alb_cognito or docker_compose. max_input_chars is 1-4000.
- Documents: SYS-REQ-002 Invalid model JSON is rejected. Parse retry Fails when parse_error_count is not < 3.
- Documents: SYS-REQ-003 Human-gated workflows pause until a yes or no choice arrives. pitch_choice is in 1-3 (pitch_id table). reject_round_count is 0-10.
- Documents: SYS-REQ-004 Meal debate takes the winner path when chefs agree or debate_round >= 3.
- Documents: SYS-REQ-005 Failed demo workflows publish an alarm notification when failed_count is not < 1. Technique stacks are not alarmed.
- Documents: SYS-REQ-006 Named technique executions exist for documented SFN techniques (sfn_stack_count >= 9) and implemented Flows techniques (flows_stack_count >= 6). Pipeline deploy roles are actions=* resources=* residual (not least-privilege).
- Documents: SYS-REQ-007 Repository lookup rejects a URL that is not a full https GitHub owner/repo URL and truncates README text over 5000 characters. requests_timeout_s is 1-30. PAT has no allowlist. grant_invoke SourceArn is agent/*.
- Documents: SYS-REQ-008 Itinerary ready implies a presigned PDF URL is returned with expires_in in 60-900. Untrusted markdown is passed to md2pdf/WeasyPrint.
- Documents: SYS-REQ-009 Conflicting invoke-chain prompt options cause the builder to raise.
- Documents: SYS-REQ-010 Map results present implies conversations are merged.

## Software

- Documents: SW-REQ-001 parse_json_response raises on invalid JSON or schema failure.
- Documents: SW-REQ-002 JSON retry step fails the chain unless parse_error_count < 3.
- Documents: SW-REQ-003 stepfn client reports PAUSED on wait-for-task-token using history_page_size = 1 and poll_interval_s = 1. pitch_choice is in 1-3.
- Documents: SW-REQ-004 meal_choose_winner requires winning_score > 0 or the handler raises. chef_id is red or blue. winner key is in scores keys.
- Documents: SW-REQ-005 merge_map_output merges Map iterator conversations by appending arc_entry_count = 2 entries.
- Documents: SW-REQ-006 GitHub lookup rejects a URL that is not a full https owner/repo URL or that matches the example; README is truncated unless len(readme_content) <= 5000; trending GET raises unless status_code = 200; extract_attempt_count < 3 or a real URL is extracted; requests_timeout_s is 1-30.
- Documents: SW-REQ-007 pdf_creator uploads a private object and returns a presigned URL with expires_in in 60-900.
- Documents: SW-REQ-008 Alarms stack defines per-demo failed-execution alarms with alarm_threshold = 1, evaluation_periods = 1, and a composite SNS alarm. Technique stacks are not alarmed.
- Documents: SW-REQ-009 Technique apps define SFN stacks for documented techniques (sfn_stack_count >= 9) and Flows stacks for implemented techniques (flows_stack_count >= 6).
- Documents: SW-REQ-010 Invoke-chain builder raises when initial assistant text and pass-conversation are both set.

## Integration

- Documents: INT-REQ-001 Bedrock invoke sends a Messages API body with max_tokens_to_sample > 0.
- Documents: INT-REQ-002 Webapp starts demos with Step Functions StartExecution and returns the execution ARN.
- Documents: INT-REQ-003 SFN parse-JSON Lambda event supplies response_string and json_schema.
- Documents: INT-REQ-004 GitHub trending lookup issues HTTP GET to github.com/trending with requests_timeout_s in 1-30 and raises when status_code is not 200.
- Documents: INT-REQ-005 Composite alarm publishes to bedrock-serverless-prompt-chaining-notifications.
- Documents: INT-REQ-006 PDF object is stored in PDF_BUCKET and returned as a presigned GET URL with expires_in in 60-900.
- Documents: INT-REQ-007 Flows test runner invokes the named flow through alias live and raises unless completionReason is SUCCESS.
