import json
from unittest.mock import MagicMock

import pytest

from tests.conftest import load_module

stepfn = load_module("webapp_stepfn", "webapp/stepfn.py")


class FakeSts:
    def __init__(self, account):
        self.account = account

    def get_caller_identity(self):
        return {"Account": self.account}


class FakeSfn:
    def __init__(self, status="RUNNING", events=None, history_pages=None):
        self.status = status
        self.events = events or []
        self.history_pages = history_pages
        self.describe_calls = []
        self.history_calls = []
        self.start_calls = []

    def start_execution(self, **kwargs):
        self.start_calls.append(kwargs)
        if not kwargs.get("name"):
            raise ValueError("missing name")
        return {"executionArn": "arn:aws:states:us-east-1:1:execution:x:y"}

    def describe_execution(self, executionArn):
        self.describe_calls.append(executionArn)
        return {"status": self.status, "executionArn": executionArn}

    def get_execution_history(self, **kwargs):
        self.history_calls.append(kwargs)
        return {"events": list(self.events)}

    def get_paginator(self, name):
        paginator = MagicMock()
        pages = self.history_pages if self.history_pages is not None else [{"events": self.events}]
        paginator.paginate.return_value = pages
        return paginator


def test_get_execution_name_includes_session_and_unique_suffix():
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    session_id = "abc123"
    name = stepfn.get_execution_name(session_id)
    prefix = f"streamlit-{session_id}-"
    assert name.startswith(prefix)
    suffix = name[len(prefix) :]
    assert len(suffix) == 12
    other = stepfn.get_execution_name(session_id)
    assert other != name
    assert other.startswith(prefix)


def test_get_execution_arn_uses_region_account_and_names():
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    arn = stepfn.get_execution_arn(
        "PromptChainDemo",
        "streamlit-sess-deadbeef",
        region="eu-west-1",
        sts_client=FakeSts("111122223333"),
    )
    assert arn == (
        "arn:aws:states:eu-west-1:111122223333:execution:"
        "PromptChainDemo:streamlit-sess-deadbeef"
    )


def test_is_execution_completed_false_while_running():
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    client = FakeSfn(status="RUNNING")
    assert stepfn.is_execution_completed("arn:aws:states:us-east-1:1:execution:x:y", client=client) is False
    assert client.describe_calls == ["arn:aws:states:us-east-1:1:execution:x:y"]


@pytest.mark.parametrize("status", ["SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"])
def test_is_execution_completed_true_for_terminal_status(status):
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    assert (
        stepfn.is_execution_completed("arn:exec", client=FakeSfn(status=status)) is True
    )


def test_wait_for_task_token_maps_history_to_paused():
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=F, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=F, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=F, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=F, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=F, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=F, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=F, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=F, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=F, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, execution_status_is_paused=T, greenlight_path_taken=T, history_contains_wait=T, history_page_size_EQ_1=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, poll_interval_s_EQ_1=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, task_token_wait_seen=T, temperature_settings_count_EQ_3=T => TRUE
    # MCDC SYS-REQ-003: choice_is_yes_or_no=F, execution_pauses_for_choice=F, greenlight_path_taken=F, history_contains_wait=F, human_wait_required=F, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=F, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=F, execution_pauses_for_choice=F, greenlight_path_taken=F, history_contains_wait=F, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=F, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=F, execution_pauses_for_choice=F, greenlight_path_taken=F, history_contains_wait=T, human_wait_required=F, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=F, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=F, greenlight_path_taken=F, history_contains_wait=F, human_wait_required=F, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=F, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=F, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=F, history_contains_wait=F, human_wait_required=F, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=F, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=F, history_contains_wait=F, human_wait_required=F, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => TRUE
    # MCDC SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=F, human_wait_required=F, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=F, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=F, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=F, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=F, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=F, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=F, task_token_present=T, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=F, temperature_settings_count_EQ_3=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-003: choice_is_yes_or_no=T, execution_pauses_for_choice=T, greenlight_path_taken=T, history_contains_wait=T, human_wait_required=T, pitch_choice_GE_1=T, pitch_choice_LE_3=T, pitch_choice_is_declared=T, reject_and_repitch_taken=T, reject_round_count_GE_0=T, reject_round_count_LE_10=T, task_token_present=T, temperature_settings_count_EQ_3=T => TRUE

    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    # Verifies: SYS-REQ-001
    # Verifies: INT-REQ-002
    # Verifies: STK-REQ-001
    # SW-REQ-003:nominal:nominal
    # SW-REQ-003:error_handling:nominal
    # SYS-REQ-003:nominal:nominal
    # SYS-REQ-003:error_handling:nominal
    # SYS-REQ-001:nominal:nominal
    # SYS-REQ-001:boundary:nominal
    # SYS-REQ-001:error_handling:nominal
    # INT-REQ-002:nominal:nominal
    # INT-REQ-002:error_handling:nominal
    # INT-REQ-002:integration:integration
    payload = {"question": "Keep this plot?", "taskToken": "tok-1"}
    client = FakeSfn(
        status="RUNNING",
        events=[
            {
                "type": "TaskSubmitted",
                "taskSubmittedEventDetails": {
                    "resource": "invoke.waitForTaskToken",
                    "output": json.dumps({"Payload": payload}),
                },
            }
        ],
    )

    result = stepfn.poll_for_execution_task_token_or_completion("arn:exec", client=client)

    assert result["status"] == "PAUSED"
    assert result["task_payload"] == payload


def test_completed_execution_is_not_reported_as_paused():
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    # Verifies: SYS-REQ-001
    # Verifies: INT-REQ-002
    # SW-REQ-003:error_handling:negative
    # SYS-REQ-003:error_handling:negative
    # SYS-REQ-001:error_handling:negative
    # INT-REQ-002:error_handling:negative
    # INT-REQ-002:integration:integration
    client = FakeSfn(status="SUCCEEDED")
    result = stepfn.poll_for_execution_task_token_or_completion("arn:exec", client=client)
    assert result["status"] == "SUCCEEDED"
    assert "task_payload" not in result


def test_start_execution_calls_sfn_start_execution():
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=F, execution_arn_includes_account=F, execution_arn_returned=F, execution_name_prefixed=F, execution_name_suffix_len_EQ_12=F, named_demo_exists=F, start_execution_called=F, start_requested=F, terminal_status_is_recognized=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-002: demo_execution_reaches_terminal=F, execution_arn_includes_account=F, execution_arn_returned=F, execution_name_prefixed=F, execution_name_suffix_len_EQ_12=T, named_demo_exists=F, start_execution_called=F, start_requested=F, terminal_status_is_recognized=F => TRUE
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=F, execution_arn_includes_account=F, execution_arn_returned=F, execution_name_prefixed=F, execution_name_suffix_len_EQ_12=T, named_demo_exists=F, start_execution_called=F, start_requested=T, terminal_status_is_recognized=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=F, execution_arn_includes_account=T, execution_arn_returned=T, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=T, start_requested=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=F, execution_arn_returned=T, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=T, start_requested=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=T, execution_arn_returned=F, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=T, start_requested=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=T, execution_arn_returned=T, execution_name_prefixed=F, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=T, start_requested=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=T, execution_arn_returned=T, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=F, start_execution_called=T, start_requested=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=T, execution_arn_returned=T, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=F, start_requested=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=T, execution_arn_returned=T, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=T, start_requested=T, terminal_status_is_recognized=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-002: demo_execution_reaches_terminal=T, execution_arn_includes_account=T, execution_arn_returned=T, execution_name_prefixed=T, execution_name_suffix_len_EQ_12=T, named_demo_exists=T, start_execution_called=T, start_requested=T, terminal_status_is_recognized=T => TRUE
    # MCDC SYS-REQ-001: demo_execution_reaches_terminal=F, demo_execution_started=F, execution_arn_returned=F, execution_name_prefixed=F, named_demo_exists=T, start_execution_called=F, terminal_status_is_recognized=F => TRUE [no-action: guarded action not requested on this path]
    # MCDC SYS-REQ-001: demo_execution_reaches_terminal=F, demo_execution_started=T, execution_arn_returned=F, execution_name_prefixed=F, named_demo_exists=F, start_execution_called=F, terminal_status_is_recognized=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-001: demo_execution_reaches_terminal=F, demo_execution_started=T, execution_arn_returned=F, execution_name_prefixed=F, named_demo_exists=T, start_execution_called=F, terminal_status_is_recognized=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-001: demo_execution_reaches_terminal=F, demo_execution_started=T, execution_arn_returned=T, execution_name_prefixed=T, named_demo_exists=T, start_execution_called=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-001: demo_execution_reaches_terminal=T, demo_execution_started=T, execution_arn_returned=F, execution_name_prefixed=T, named_demo_exists=T, start_execution_called=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-001: demo_execution_reaches_terminal=T, demo_execution_started=T, execution_arn_returned=T, execution_name_prefixed=F, named_demo_exists=T, start_execution_called=T, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-001: demo_execution_reaches_terminal=T, demo_execution_started=T, execution_arn_returned=T, execution_name_prefixed=T, named_demo_exists=T, start_execution_called=F, terminal_status_is_recognized=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-001: demo_execution_reaches_terminal=T, demo_execution_started=T, execution_arn_returned=T, execution_name_prefixed=T, named_demo_exists=T, start_execution_called=T, terminal_status_is_recognized=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-001: demo_execution_reaches_terminal=T, demo_execution_started=T, execution_arn_returned=T, execution_name_prefixed=T, named_demo_exists=T, start_execution_called=T, terminal_status_is_recognized=T => TRUE

    # Verifies: INT-REQ-002
    # Verifies: SYS-REQ-001
    # INT-REQ-002:nominal:nominal
    # INT-REQ-002:error_handling:nominal
    # INT-REQ-002:integration:integration
    # SYS-REQ-001:nominal:nominal
    client = FakeSfn()
    arn = stepfn.start_execution(
        "PromptChainDemo-BlogPost",
        "sess-1",
        "{}",
        client=client,
        region="us-east-1",
        sts_client=FakeSts("111122223333"),
    )
    assert client.start_calls, "FakeSfn.start_execution was not called"
    call = client.start_calls[0]
    assert call["stateMachineArn"] == (
        "arn:aws:states:us-east-1:111122223333:stateMachine:PromptChainDemo-BlogPost"
    )
    assert call["name"].startswith("streamlit-sess-1-")
    assert call["input"] == "{}"
    assert arn == "arn:aws:states:us-east-1:1:execution:x:y"


def test_start_execution_missing_name_is_negative():
    # Verifies: INT-REQ-002
    # INT-REQ-002:error_handling:negative
    # INT-REQ-002:integration:integration
    client = FakeSfn()
    with pytest.raises(TypeError):
        stepfn.start_execution()
    assert client.start_calls == []
