# Parent system requirement: SYS-REQ-001
"""Unit tests for the Bedrock Agents trending-repo lookup handler.

Drives lookup_trending_repo_agent with a mocked invoke_agent so the
retry, URL-extract, and example-URL rejection branches run without AWS.
"""

from unittest.mock import MagicMock

import pytest

from tests.conftest import load_module

AGENT_PATH = "functions/most_popular_repo_bedrock_agent/agent/index.py"


def _completion(text):
    return {
        "ResponseMetadata": {"RequestId": "req-1"},
        "completion": [{"chunk": {"bytes": text.encode("utf-8")}}],
    }


def _load(monkeypatch, invoke_side_effect):
    monkeypatch.setenv("BEDROCK_AGENT_ID", "agent-id")
    monkeypatch.setenv("BEDROCK_AGENT_ALIAS_ID", "alias-id")
    mod = load_module("bedrock_agent_lookup", AGENT_PATH)
    client = MagicMock()
    client.invoke_agent.side_effect = invoke_side_effect
    mod.bedrock_agent_client = client
    return mod, client


def test_lookup_accepts_first_real_github_url(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:nominal:nominal
    # SW-REQ-006:error_handling:nominal
    # SW-REQ-006:malformed_input:nominal
    mod, client = _load(
        monkeypatch,
        [_completion("Top repo is https://github.com/owner/realrepo today")],
    )
    result = mod.lookup_trending_repo_agent({}, None)
    assert result["repo"] == "https://github.com/owner/realrepo"
    assert client.invoke_agent.call_count == 1


def test_lookup_retries_after_example_url_then_accepts_real(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:error_handling:negative
    # SW-REQ-006:malformed_input:negative
    mod, client = _load(
        monkeypatch,
        [
            _completion("https://github.com/orgname/reponame"),
            _completion("https://github.com/owner/second"),
        ],
    )
    result = mod.lookup_trending_repo_agent({}, None)
    assert result["repo"] == "https://github.com/owner/second"
    assert client.invoke_agent.call_count == 2


def test_lookup_raises_when_no_url_extracted(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:error_handling:negative
    mod, client = _load(
        monkeypatch,
        [
            _completion("no url here"),
            _completion("still none"),
            _completion("nope"),
        ],
    )
    with pytest.raises(Exception, match="Could not find URL from Bedrock Agent responses"):
        mod.lookup_trending_repo_agent({}, None)
    assert client.invoke_agent.call_count == 3
