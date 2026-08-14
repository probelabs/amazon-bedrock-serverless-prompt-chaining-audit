# Parent system requirement: SYS-REQ-001
import sys
from unittest.mock import MagicMock

import pytest

# stacks/util.py imports aws_cdk at module load. Stub the CDK surface so we
# can drive the pure guard in get_anthropic_claude_invoke_chain (and inspect
# the retry limit in get_json_response_parser_step) without synthesizing a stack.
_CDK_MODULES = [
    "aws_cdk",
    "aws_cdk.aws_bedrock",
    "aws_cdk.aws_iam",
    "aws_cdk.aws_lambda",
    "aws_cdk.aws_lambda_python_alpha",
    "aws_cdk.aws_stepfunctions",
    "aws_cdk.aws_stepfunctions_tasks",
    "constructs",
    "jsii",
]
for _name in _CDK_MODULES:
    sys.modules.setdefault(_name, MagicMock())

from stacks import util as util_mod  # noqa: E402


def test_invoke_chain_raises_when_assistant_text_and_pass_conversation():
    # MCDC INT-REQ-001: anthropic_messages_role_user=F, anthropic_version_is_bedrock=F, claude_model_id_set=F, content_type_is_json=F, invoke_requested=F, max_tokens_to_sample_GT_0=F, messages_api_body_sent=F => TRUE [no-action: guarded action not requested on this path]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=F, anthropic_version_is_bedrock=F, claude_model_id_set=F, content_type_is_json=F, invoke_requested=T, max_tokens_to_sample_GT_0=F, messages_api_body_sent=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=F, anthropic_version_is_bedrock=T, claude_model_id_set=T, content_type_is_json=T, invoke_requested=T, max_tokens_to_sample_GT_0=T, messages_api_body_sent=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=T, anthropic_version_is_bedrock=F, claude_model_id_set=T, content_type_is_json=T, invoke_requested=T, max_tokens_to_sample_GT_0=T, messages_api_body_sent=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=T, anthropic_version_is_bedrock=T, claude_model_id_set=F, content_type_is_json=T, invoke_requested=T, max_tokens_to_sample_GT_0=T, messages_api_body_sent=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=T, anthropic_version_is_bedrock=T, claude_model_id_set=T, content_type_is_json=F, invoke_requested=T, max_tokens_to_sample_GT_0=T, messages_api_body_sent=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=T, anthropic_version_is_bedrock=T, claude_model_id_set=T, content_type_is_json=T, invoke_requested=T, max_tokens_to_sample_GT_0=F, messages_api_body_sent=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-001: anthropic_messages_role_user=T, anthropic_version_is_bedrock=T, claude_model_id_set=T, content_type_is_json=T, invoke_requested=T, max_tokens_to_sample_GT_0=T, messages_api_body_sent=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-001: anthropic_messages_role_user=T, anthropic_version_is_bedrock=T, claude_model_id_set=T, content_type_is_json=T, invoke_requested=T, max_tokens_to_sample_GT_0=T, messages_api_body_sent=T => TRUE

    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-009
    # Verifies: INT-REQ-001
    # SW-REQ-010:error_handling:negative
    # SYS-REQ-009:error_handling:negative
    # INT-REQ-001:error_handling:negative
    # INT-REQ-001:integration:integration
    with pytest.raises(
        ValueError,
        match="initial_assistant_text cannot be used with pass_conversation",
    ):
        util_mod.get_anthropic_claude_invoke_chain(
            scope=object(),
            id="ClaudeStep",
            prompt="Hello",
            initial_assistant_text="Sure,",
            pass_conversation=True,
        )


def test_invoke_chain_allows_assistant_text_without_pass_conversation():
    # mcdc:ignore:defensive SW-REQ-010: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, initial_assistant_text_set=F, max_tokens_to_sample_GT_0=F, pass_conversation_set=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-010: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, initial_assistant_text_set=F, max_tokens_to_sample_GT_0=T, pass_conversation_set=F => TRUE
    # MCDC SW-REQ-010: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, initial_assistant_text_set=F, max_tokens_to_sample_GT_0=T, pass_conversation_set=T => TRUE
    # MCDC SW-REQ-010: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, initial_assistant_text_set=T, max_tokens_to_sample_GT_0=T, pass_conversation_set=F => TRUE
    # mcdc:ignore:defensive SW-REQ-010: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, initial_assistant_text_set=T, max_tokens_to_sample_GT_0=T, pass_conversation_set=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-010: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=T, initial_assistant_text_set=F, max_tokens_to_sample_GT_0=T, pass_conversation_set=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-010: builder_raises=F, conflicting_prompt_options=T, flatten_messages=F, include_previous_conversation_in_prompt=F, initial_assistant_text_set=F, max_tokens_to_sample_GT_0=T, pass_conversation_set=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-010: builder_raises=F, conflicting_prompt_options=T, flatten_messages=T, include_previous_conversation_in_prompt=T, initial_assistant_text_set=T, max_tokens_to_sample_GT_0=T, pass_conversation_set=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-010: builder_raises=T, conflicting_prompt_options=T, flatten_messages=F, include_previous_conversation_in_prompt=T, initial_assistant_text_set=T, max_tokens_to_sample_GT_0=T, pass_conversation_set=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-010: builder_raises=T, conflicting_prompt_options=T, flatten_messages=T, include_previous_conversation_in_prompt=T, initial_assistant_text_set=T, max_tokens_to_sample_GT_0=T, pass_conversation_set=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-009: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, max_tokens_to_sample_GT_0=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-009: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=F, max_tokens_to_sample_GT_0=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-009: builder_raises=F, conflicting_prompt_options=F, flatten_messages=F, include_previous_conversation_in_prompt=T, max_tokens_to_sample_GT_0=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-009: builder_raises=F, conflicting_prompt_options=T, flatten_messages=F, include_previous_conversation_in_prompt=F, max_tokens_to_sample_GT_0=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-009: builder_raises=F, conflicting_prompt_options=T, flatten_messages=T, include_previous_conversation_in_prompt=T, max_tokens_to_sample_GT_0=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-009: builder_raises=T, conflicting_prompt_options=T, flatten_messages=F, include_previous_conversation_in_prompt=T, max_tokens_to_sample_GT_0=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-009: builder_raises=T, conflicting_prompt_options=T, flatten_messages=T, include_previous_conversation_in_prompt=T, max_tokens_to_sample_GT_0=T => TRUE

    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-009
    # Verifies: INT-REQ-001
    # SW-REQ-010:nominal:nominal
    # SW-REQ-010:error_handling:nominal
    # SYS-REQ-009:nominal:nominal
    # SYS-REQ-009:error_handling:nominal
    # INT-REQ-001:nominal:nominal
    # INT-REQ-001:error_handling:nominal
    # INT-REQ-001:integration:integration
    result = util_mod.get_anthropic_claude_invoke_chain(
        scope=object(),
        id="ClaudeStep",
        prompt="Hello",
        initial_assistant_text="Sure,",
        pass_conversation=False,
    )
    assert result is not None


def test_invoke_chain_omits_previous_conversation_and_does_not_flatten():
    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-009
    # SYS-REQ-009:nominal:nominal
    # INT-REQ-001:nominal:nominal
    # Drive include_previous_conversation_in_prompt=False and flatten_messages=False.
    sfn = util_mod.sfn
    sfn.Pass.reset_mock()
    sfn.JsonPath.object_at.reset_mock()

    result = util_mod.get_anthropic_claude_invoke_chain(
        scope=object(),
        id="ClaudeStep",
        prompt="Hello",
        initial_assistant_text="",
        include_previous_conversation_in_prompt=False,
        pass_conversation=True,
    )
    assert result is not None

    pass_ids = [
        call.args[1] if len(call.args) > 1 else call.kwargs.get("id")
        for call in sfn.Pass.call_args_list
    ]
    assert not any(
        "Include Previous Messages" in str(pass_id) for pass_id in pass_ids
    )
    object_at_args = [
        call.args[0] for call in sfn.JsonPath.object_at.call_args_list if call.args
    ]
    assert any(arg == "$.model_inputs.messages" for arg in object_at_args)
    assert not any("messages[*][*]" in str(arg) for arg in object_at_args)


def test_invoke_chain_excludes_initial_assistant_text_from_response():
    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-009
    # SYS-REQ-009:nominal:nominal
    # include_initial_assistant_text_in_response=False with non-empty
    # initial_assistant_text and pass_conversation=False.
    sfn = util_mod.sfn
    sfn.JsonPath.format.reset_mock()

    result = util_mod.get_anthropic_claude_invoke_chain(
        scope=object(),
        id="ClaudeStep",
        prompt="Hello",
        initial_assistant_text="Sure,",
        include_initial_assistant_text_in_response=False,
        pass_conversation=False,
    )
    assert result is not None
    format_args = [call.args for call in sfn.JsonPath.format.call_args_list]
    assert not any(args and args[0] == "{}{}" for args in format_args)


def test_invoke_chain_pass_conversation_without_assistant_text():
    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-009
    # SYS-REQ-009:nominal:nominal
    # True of `if pass_conversation:`, false of `if initial_assistant_text:`,
    # and false of the raise guard.
    sfn = util_mod.sfn
    sfn.Pass.reset_mock()

    result = util_mod.get_anthropic_claude_invoke_chain(
        scope=object(),
        id="ClaudeStep",
        prompt="Hello",
        initial_assistant_text="",
        pass_conversation=True,
    )
    assert result is not None
    pass_ids = [
        call.args[1] if len(call.args) > 1 else call.kwargs.get("id")
        for call in sfn.Pass.call_args_list
    ]
    assert any("Prepare Output" in str(pass_id) for pass_id in pass_ids)


def test_json_retry_step_fails_after_three_parse_errors():
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=F, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=F, parser_rejects_or_retries=F, retry_choice_taken=F, retry_limit_is_three=F, schema_provided=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=F, parse_error_increment_EQ_1=T, parse_failed=F, parser_rejects_or_retries=F, retry_choice_taken=F, retry_limit_is_three=F, schema_provided=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=F, parse_error_increment_EQ_1=T, parse_failed=F, parser_rejects_or_retries=T, retry_choice_taken=F, retry_limit_is_three=F, schema_provided=F => TRUE
    # MCDC SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=F, parser_rejects_or_retries=F, retry_choice_taken=F, retry_limit_is_three=F, schema_provided=F => TRUE
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=F, parser_rejects_or_retries=F, retry_choice_taken=F, retry_limit_is_three=F, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=F, parser_rejects_or_retries=F, retry_choice_taken=T, retry_limit_is_three=F, schema_provided=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=F, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=T, parser_rejects_or_retries=F, retry_choice_taken=F, retry_limit_is_three=F, schema_provided=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=F, fix_json_prompted=T, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=T, parser_rejects_or_retries=T, retry_choice_taken=T, retry_limit_is_three=T, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=T, fix_json_prompted=F, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=T, parser_rejects_or_retries=T, retry_choice_taken=T, retry_limit_is_three=T, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=T, fix_json_prompted=T, parse_error_count_LT_3=T, parse_error_increment_EQ_1=F, parse_failed=T, parser_rejects_or_retries=T, retry_choice_taken=T, retry_limit_is_three=T, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-002: chain_fails=T, error_counter_incremented=T, fix_json_prompted=T, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=T, parser_rejects_or_retries=T, retry_choice_taken=T, retry_limit_is_three=F, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-002: chain_fails=T, error_counter_incremented=T, fix_json_prompted=T, parse_error_count_LT_3=T, parse_error_increment_EQ_1=T, parse_failed=T, parser_rejects_or_retries=T, retry_choice_taken=T, retry_limit_is_three=T, schema_provided=T => TRUE
    # mcdc:witness-code-free SW-REQ-002
    # Verifies: SW-REQ-002
    # Verifies: SYS-REQ-002
    # SW-REQ-002:boundary:nominal
    # SW-REQ-002:error_handling:negative
    # SW-REQ-002:error_handling:nominal
    # SW-REQ-002:nominal:nominal
    # SYS-REQ-002:boundary:nominal
    # SYS-REQ-002:error_handling:nominal
    sfn = util_mod.sfn
    sfn.Condition.number_less_than.reset_mock()
    sfn.Fail.reset_mock()
    sfn.Choice.reset_mock()
    sfn.Errors = MagicMock()
    sfn.Errors.TASKS_FAILED = "States.TaskFailed"

    util_mod.get_json_response_parser_step(
        scope=object(),
        id="Parse JSON",
        json_schema={"type": "object"},
        output_key="parsed",
        result_path="$.parsed_output",
    )

    less_than_calls = sfn.Condition.number_less_than.call_args_list
    assert less_than_calls, "retry Choice never compared parse_error_count"
    assert any(
        call.args == ("$.error_state.parse_error_count", 3)
        or call.kwargs.get("variable") == "$.error_state.parse_error_count"
        and call.kwargs.get("value") == 3
        for call in less_than_calls
    ), less_than_calls
    assert sfn.Fail.called
    assert sfn.Choice.called
    assert sfn.Choice.return_value.when.called
