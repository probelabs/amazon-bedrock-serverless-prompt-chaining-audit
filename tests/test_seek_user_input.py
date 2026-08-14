from tests.conftest import load_module


def test_handler_is_noop_and_returns_event():
    # Verifies: SW-REQ-003
    # Verifies: SYS-REQ-003
    # SW-REQ-003:nominal:nominal
    # SYS-REQ-003:nominal:nominal
    handler = load_module(
        "seek_user_input",
        "functions/generic/seek_user_input/index.py",
    ).handler
    event = {
        "question": "Should we keep this movie pitch?",
        "taskToken": "AAAA",
        "executionName": "streamlit-sess-1",
    }

    result = handler(event, None)

    assert result is event
    assert result["question"] == event["question"]
    assert result["taskToken"] == event["taskToken"]
