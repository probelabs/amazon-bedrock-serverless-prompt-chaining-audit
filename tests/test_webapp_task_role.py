"""Shared Fargate task-role grants vs unprivileged Movie Pitch token path."""
from pathlib import Path

import pytest

WEBAPP_STACK = Path("/workspace/stacks/webapp_stack.py")
MOVIE_PITCH = Path("/workspace/webapp/pages/4_Movie_Pitch.py")
STEPFN = Path("/workspace/webapp/stepfn.py")

DEMO_SUFFIXES = (
    "BlogPost",
    "TripPlanner",
    "StoryWriter",
    "MoviePitch",
    "MealPlanner",
    "MostPopularRepoBedrockAgents",
    "MostPopularRepoStrands",
)


def _grant_task_response_count(source: str) -> int:
    return source.count("grant_task_response(")


# Reproduces: KI-webapp-shared-task-role-any-token
@pytest.mark.xfail(
    strict=True,
    reason=(
        "KI-webapp-shared-task-role-any-token: one Fargate task role still "
        "gets grant_task_response on every PromptChainDemo state machine"
    ),
)
def test_fargate_task_role_does_not_grant_task_response_on_every_demo():
    source = WEBAPP_STACK.read_text()
    for suffix in DEMO_SUFFIXES:
        assert f'PromptChainDemo-{suffix}' in source
    assert _grant_task_response_count(source) == 0, (
        "WebappStack must not grant_task_response on the shared Fargate "
        "task role for every PromptChainDemo-* machine "
        "(stacks/webapp_stack.py:89-91)"
    )


def test_movie_pitch_continue_does_not_take_a_user_supplied_task_token():
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    """Unprivileged IDOR cannot happen via the Streamlit form.

    The IAM role can SendTaskSuccess for any demo token, but the only
    continue_execution call site passes st.session_state.movie_pitch_task_token
    (set from this session's own poll). There is no token widget or query
    param. Without Fargate/task-role compromise, a Cognito user cannot feed
    another execution's token.
    """
    pitch = MOVIE_PITCH.read_text()
    stepfn = STEPFN.read_text()
    assert "st.session_state.movie_pitch_task_token" in pitch
    assert "continue_execution(" in pitch
    assert "query_params" not in pitch
    assert 'st.text_input(\n                "task' not in pitch
    assert "taskToken" not in pitch
    assert "send_task_success" in stepfn
    # Only Movie Pitch continues a task token; it does not read a token field.
    assert pitch.count("continue_execution(") == 1
    assert "st.session_state.movie_pitch_task_token" in pitch.split(
        "def continue_state_machine"
    )[1].split("def handle_stepfn_response")[0]
