# Requirements map

This document is documentation evidence for the ReqProof four-layer skeleton.

## Stakeholder

- STK-REQ-001 — Demo user obtains a completed result for a named prompt-chaining application.
- STK-REQ-002 — Operator receives a notification when a named demo or technique workflow fails.
- STK-REQ-003 — Technique operator executes an isolated prompt-chaining technique example.

## System

- SYS-REQ-001 — Demo orchestrator takes each named demo execution to a terminal state.
- SYS-REQ-002 — Invalid model JSON is rejected. Parse retry is bounded to three attempts.
- SYS-REQ-003 — Human-gated workflows pause until a yes or no choice arrives.
- SYS-REQ-004 — Meal debate stops at agreement or debate round three.
- SYS-REQ-005 — Failed demo workflows publish an alarm notification.
- SYS-REQ-006 — Named technique executions exist for documented SFN techniques and implemented Flows techniques.

## Software

- SW-REQ-001 — parse_json_response raises on invalid JSON or schema failure.
- SW-REQ-002 — JSON retry step fails the chain at parse error count three.
- SW-REQ-003 — stepfn client reports PAUSED on wait-for-task-token.
- SW-REQ-004 — meal_choose_winner selects the highest score or raises.
- SW-REQ-005 — merge_map_output merges Map iterator conversations.
- SW-REQ-006 — GitHub lookup rejects invalid or example repository URLs.
- SW-REQ-007 — pdf_creator uploads a private object and returns a presigned URL.
- SW-REQ-008 — Alarms stack defines per-demo failed-execution alarms and a composite SNS alarm.
- SW-REQ-009 — Technique apps define SFN stacks for documented techniques and Flows stacks for implemented techniques.
- SW-REQ-010 — Invoke-chain builder raises when initial assistant text and pass-conversation are both set.

## Integration

- INT-REQ-001 — Bedrock invoke sends a Messages API body.
- INT-REQ-002 — Webapp starts demos with Step Functions StartExecution.
- INT-REQ-003 — SFN parse-JSON Lambda event supplies response_string and json_schema.
- INT-REQ-004 — GitHub trending lookup issues HTTP GET to github.com/trending.
- INT-REQ-005 — Composite alarm publishes to bedrock-serverless-prompt-chaining-notifications.
- INT-REQ-006 — PDF object is stored in PDF_BUCKET and returned as a presigned GET URL.
- INT-REQ-007 — Flows test runner invokes the named flow through alias live.

Documents: STK-REQ-001 STK-REQ-002 STK-REQ-003 SYS-REQ-001 SYS-REQ-002 SYS-REQ-003 SYS-REQ-004 SYS-REQ-005 SYS-REQ-006 SW-REQ-001 SW-REQ-002 SW-REQ-003 SW-REQ-004 SW-REQ-005 SW-REQ-006 SW-REQ-007 SW-REQ-008 SW-REQ-009 SW-REQ-010 INT-REQ-001 INT-REQ-002 INT-REQ-003 INT-REQ-004 INT-REQ-005 INT-REQ-006 INT-REQ-007
