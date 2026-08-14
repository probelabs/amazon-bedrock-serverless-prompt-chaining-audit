"""Reproducers for Bedrock agent Lambda invoke resource-policy wildcards."""
from pathlib import Path

import pytest

BEDROCK_AGENT_STACK = Path(
    "/workspace/stacks/most_popular_repo_bedrock_agent_stack.py"
)


# Reproduces: KI-bedrock-agent-invoke-wildcard
@pytest.mark.xfail(
    strict=True,
    reason="KI-bedrock-agent-invoke-wildcard: grant_invoke SourceArn is agent/*",
)
def test_github_actions_invoke_source_arn_is_pinned_to_this_agent():
    source = BEDROCK_AGENT_STACK.read_text()
    assert "agent/*" not in source, (
        "github_agent_actions_lambda.grant_invoke SourceArn must pin this "
        "agent ARN, not arn:aws:bedrock:{region}:{account}:agent/*"
    )
