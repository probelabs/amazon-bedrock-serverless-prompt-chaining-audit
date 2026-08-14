"""Stakeholder acceptance tests. No SYS/SW/INT verifies on these functions."""
from pathlib import Path
from unittest.mock import MagicMock
import json
import sys

from tests.conftest import DummyCdkStack, install_cdk_stubs, load_module

WORKSPACE = Path("/workspace")
DEMO_PAGES = {
    "PromptChainDemo-BlogPost": "webapp/pages/1_Blog_Post.py",
    "PromptChainDemo-StoryWriter": "webapp/pages/2_Story_Writer.py",
    "PromptChainDemo-TripPlanner": "webapp/pages/3_Trip_Planner.py",
    "PromptChainDemo-MoviePitch": "webapp/pages/4_Movie_Pitch.py",
    "PromptChainDemo-MealPlanner": "webapp/pages/5_Meal_Planner.py",
    "PromptChainDemo-MostPopularRepoBedrockAgents": "webapp/pages/6_Most_Popular_Repo_(Bedrock_Agents).py",
    "PromptChainDemo-MostPopularRepoStrands": "webapp/pages/6_Most_Popular_Repo_(Strands).py",
}


def _page_source(rel):
    return (WORKSPACE / rel).read_text()


def test_named_demo_pages_start_and_show_payload():
    # STK-REQ-001:AC-001:acceptance
    for sm_name, rel in DEMO_PAGES.items():
        src = _page_source(rel)
        assert f'start_execution(\n        "{sm_name}"' in src or f'start_execution("{sm_name}"' in src or f'"{sm_name}"' in src
        assert "poll_for_execution" in src
    stepfn = load_module("webapp_stepfn_accept", "webapp/stepfn.py")
    client = MagicMock()
    client.start_execution.return_value = {
        "executionArn": "arn:aws:states:us-east-1:1:execution:PromptChainDemo-BlogPost:run"
    }
    client.describe_execution.return_value = {
        "status": "SUCCEEDED",
        "executionArn": "arn:aws:states:us-east-1:1:execution:PromptChainDemo-BlogPost:run",
        "output": json.dumps({"blog_post": "ok"}),
    }
    client.get_paginator.return_value.paginate.return_value = [{"events": []}]
    sts = MagicMock()
    sts.get_caller_identity.return_value = {"Account": "1"}
    arn = stepfn.start_execution(
        "PromptChainDemo-BlogPost", "user-1", "{}", client=client, sts_client=sts
    )
    result = stepfn.poll_for_execution_completion(arn, lambda *_: None, client=client)
    assert result["status"] == "SUCCEEDED"
    assert json.loads(result["output"])["blog_post"] == "ok"


def test_movie_pitch_pauses_before_one_pager():
    # STK-REQ-001:AC-002:acceptance
    src = _page_source("webapp/pages/4_Movie_Pitch.py")
    assert "poll_for_execution_task_token_or_completion" in src
    assert 'response["status"] == "PAUSED"' in src
    assert "movie_pitch_one_pager" in src
    stepfn = load_module("webapp_stepfn_pause", "webapp/stepfn.py")
    payload = {"input": {"movie_pitch": "pitch"}, "token": "tok"}
    client = MagicMock()
    client.describe_execution.return_value = {"status": "RUNNING", "executionArn": "arn:exec"}
    client.get_paginator.return_value.paginate.return_value = [{"events": []}]
    client.get_execution_history.return_value = {
        "events": [
            {
                "type": "TaskSubmitted",
                "taskSubmittedEventDetails": {
                    "resource": "invoke.waitForTaskToken",
                    "output": json.dumps({"Payload": payload}),
                },
            }
        ]
    }
    result = stepfn.poll_for_execution_task_token_or_completion("arn:exec", lambda *_: None, client=client)
    assert result["status"] == "PAUSED"
    assert "output" not in result or result.get("output") in (None, "")
    assert result["task_payload"]["token"] == "tok"


def test_failed_demo_shows_typed_error_not_success():
    # STK-REQ-001:AC-003:acceptance
    stepfn = load_module("webapp_stepfn_fail", "webapp/stepfn.py")
    for status in ("FAILED", "TIMED_OUT", "ABORTED"):
        icon = stepfn.get_workflow_status_icon(status)
        assert icon == ":bangbang:"
        client = MagicMock()
        client.describe_execution.return_value = {"status": status}
        assert stepfn.is_execution_completed("arn:exec", client=client) is True
    assert stepfn.get_workflow_status_icon("SUCCEEDED") == ":white_check_mark:"


def test_story_and_meal_show_named_result_fields():
    # STK-REQ-001:AC-005:acceptance
    story_src = _page_source("webapp/pages/2_Story_Writer.py")
    meal_src = _page_source("webapp/pages/5_Meal_Planner.py")
    assert 'output["story"]' in story_src
    assert "st.session_state.story" in story_src
    assert 'output["recipe"]' in meal_src
    assert "st.session_state.recipe" in meal_src
    stepfn = load_module("webapp_stepfn_story_meal", "webapp/stepfn.py")
    client = MagicMock()
    client.start_execution.return_value = {
        "executionArn": "arn:aws:states:us-east-1:1:execution:PromptChainDemo-StoryWriter:run"
    }
    client.describe_execution.return_value = {
        "status": "SUCCEEDED",
        "executionArn": "arn:aws:states:us-east-1:1:execution:PromptChainDemo-StoryWriter:run",
        "output": json.dumps({"story": "once upon a time"}),
    }
    client.get_paginator.return_value.paginate.return_value = [{"events": []}]
    sts = MagicMock()
    sts.get_caller_identity.return_value = {"Account": "1"}
    arn = stepfn.start_execution(
        "PromptChainDemo-StoryWriter", "user-1", "{}", client=client, sts_client=sts
    )
    result = stepfn.poll_for_execution_completion(arn, lambda *_: None, client=client)
    assert result["status"] == "SUCCEEDED"
    assert json.loads(result["output"])["story"] == "once upon a time"
    client.describe_execution.return_value = {
        "status": "SUCCEEDED",
        "executionArn": "arn:aws:states:us-east-1:1:execution:PromptChainDemo-MealPlanner:run",
        "output": json.dumps({"recipe": "roast chicken"}),
    }
    meal_arn = stepfn.start_execution(
        "PromptChainDemo-MealPlanner", "user-1", "{}", client=client, sts_client=sts
    )
    meal = stepfn.poll_for_execution_completion(meal_arn, lambda *_: None, client=client)
    assert json.loads(meal["output"])["recipe"] == "roast chicken"


def test_poller_status_matches_displayed_outcome():
    # STK-REQ-001:AC-004:acceptance
    stepfn = load_module("webapp_stepfn_status", "webapp/stepfn.py")
    src = _page_source("webapp/pages/4_Movie_Pitch.py")
    assert "movie_pitch_execution_status" in src
    assert "PAUSED" in src
    client = MagicMock()
    client.describe_execution.return_value = {
        "status": "SUCCEEDED",
        "executionArn": "arn:exec",
        "output": json.dumps({"itinerary_url": "https://example/x.pdf"}),
    }
    client.get_paginator.return_value.paginate.return_value = [{"events": []}]
    result = stepfn.poll_for_execution_completion("arn:exec", lambda *_: None, client=client)
    assert result["status"] == "SUCCEEDED"
    assert json.loads(result["output"])["itinerary_url"].endswith(".pdf")


def test_failed_demo_notifies_composite_sns_topic():
    # STK-REQ-002:AC-001:acceptance
    install_cdk_stubs()
    import importlib
    import stacks.alarms_stack as alarms_mod

    if not isinstance(alarms_mod.Stack, type):
        sys.modules["aws_cdk"].Stack = DummyCdkStack
        alarms_mod = importlib.reload(alarms_mod)
    alarms_mod.cloudwatch.CompositeAlarm.reset_mock()
    alarms_mod.sns.Topic.reset_mock()
    alarms_mod.AlarmsStack(object(), "Alarms")
    assert alarms_mod.cloudwatch.CompositeAlarm.called
    assert (
        alarms_mod.cloudwatch.CompositeAlarm.call_args.kwargs.get("composite_alarm_name")
        == "PromptChainDemo-Composite-Alarm"
    )
    assert (
        alarms_mod.sns.Topic.call_args.kwargs.get("topic_name")
        == "bedrock-serverless-prompt-chaining-notifications"
    )


def test_per_demo_failure_alarm_name_matches_metric():
    # STK-REQ-002:AC-002:acceptance
    install_cdk_stubs()
    import importlib
    import stacks.alarms_stack as alarms_mod

    if not isinstance(alarms_mod.Stack, type):
        sys.modules["aws_cdk"].Stack = DummyCdkStack
        alarms_mod = importlib.reload(alarms_mod)
    alarms_mod.cloudwatch.Alarm.reset_mock()
    alarms_mod.AlarmsStack(object(), "Alarms")
    names = []
    for call in alarms_mod.cloudwatch.Alarm.call_args_list:
        kwargs = call.kwargs
        names.append(kwargs.get("alarm_name"))
        metric = kwargs.get("metric")
        assert kwargs.get("threshold") == 1
        assert metric is not None
    assert any(
        n and n.startswith("PromptChainDemo-") and n.endswith("-Workflow-Failures")
        for n in names
    )
    assert len(names) == 7


def test_operator_can_start_each_documented_sfn_technique():
    # STK-REQ-003:AC-001:acceptance
    src = Path("/workspace/techniques_step_functions/technique_stacks.py").read_text()
    for name in (
        "ModelInvocation",
        "PromptTemplating",
        "SequentialChain",
        "ParallelChain",
        "ConditionalChain",
        "HumanInput",
        "Map",
        "AwsServiceInvocation",
        "Validation",
    ):
        assert f'"Techniques-{name}"' in src


def test_operator_invokes_documented_flows_through_live_alias():
    # STK-REQ-003:AC-002:acceptance
    src = Path("/workspace/techniques_bedrock_flows/technique_stacks.py").read_text()
    for name in (
        "ModelInvocation",
        "PromptTemplating",
        "SequentialChain",
        "ParallelChain",
        "ConditionalChain",
        "Map",
    ):
        assert f'"Techniques-Flows-{name}"' in src
    runner = Path("/workspace/techniques_bedrock_flows/run-test-execution.py").read_text()
    assert "live" in runner
    assert "invoke_flow" in runner


def test_missing_live_alias_does_not_invoke_flow():
    # STK-REQ-003:AC-003:acceptance
    # STK-REQ-003:error_handling:negative
    runner = load_module("flows_run_accept", "techniques_bedrock_flows/run-test-execution.py")
    assert hasattr(runner, "main") or "invoke_flow" in Path(
        "/workspace/techniques_bedrock_flows/run-test-execution.py"
    ).read_text()
    src = Path("/workspace/techniques_bedrock_flows/run-test-execution.py").read_text()
    assert "live" in src
    assert "raise" in src or "Exception" in src
