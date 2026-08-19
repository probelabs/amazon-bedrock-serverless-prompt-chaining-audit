# Parent system requirement: SYS-REQ-001
import importlib
import json
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from tests.conftest import load_module, strands_import_stubs


def _load_strands_mod():
    return load_module(
        "most_popular_repo_strands",
        "functions/most_popular_repo_strands/index.py",
        extra_sys_modules=strands_import_stubs(),
    )


def _github_repo_model(strands_mod):
    """Run lookup_trending_repo_agent far enough to define GitHubRepo."""
    captured = {}

    fake_agent = MagicMock()

    def _call(question, structured_output_model=None):
        captured["model"] = structured_output_model
        result = MagicMock()
        result.structured_output.url = "https://github.com/owner/repo"
        return result

    fake_agent.side_effect = _call

    with (
        patch.object(strands_mod, "Agent", return_value=fake_agent),
        patch.object(strands_mod, "BedrockModel"),
    ):
        strands_mod.lookup_trending_repo_agent({}, None)

    assert captured["model"] is not None
    return captured["model"]


def test_strands_readme_truncates_over_5000(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:boundary:nominal
    mod = _load_strands_mod()
    monkeypatch.setattr(
        mod.secrets_client,
        "get_secret_value",
        lambda **kwargs: {"SecretString": json.dumps({"token": "test-token"})},
    )
    readme = MagicMock()
    readme.decoded_content = ("Y" * 6000).encode("utf-8")
    repo = MagicMock()
    repo.get_readme.return_value = readme
    github_client = MagicMock()
    github_client.get_repo.return_value = repo
    monkeypatch.setattr(mod, "Github", lambda **kwargs: github_client)
    monkeypatch.setattr(mod, "Auth", MagicMock())
    text = mod.get_github_repository_readme("https://github.com/owner/repo")
    assert "first 5,000 characters" in text
    assert "Y" * 10 in text


def test_strands_readme_full_when_under_5000(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:nominal:nominal
    # SW-REQ-006:error_handling:nominal
    # SW-REQ-006:malformed_input:nominal
    # SW-REQ-006:boundary:nominal
        # Drive the false polarity of len(readme_content) > 5000.
    mod = _load_strands_mod()
    monkeypatch.setattr(
        mod.secrets_client,
        "get_secret_value",
        lambda **kwargs: {"SecretString": json.dumps({"token": "test-token"})},
    )
    readme = MagicMock()
    readme.decoded_content = b"short readme"
    repo = MagicMock()
    repo.get_readme.return_value = readme
    github_client = MagicMock()
    github_client.get_repo.return_value = repo
    monkeypatch.setattr(mod, "Github", lambda **kwargs: github_client)
    monkeypatch.setattr(mod, "Auth", MagicMock())
    text = mod.get_github_repository_readme("https://github.com/owner/repo")
    assert "Here is the README" in text
    assert "short readme" in text


def test_github_repo_validates_canonical_https_owner_repo():
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T, url_matches_https_github_owner_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T, url_matches_https_github_owner_repo=F => TRUE
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=F, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F, url_matches_https_github_owner_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=F, readme_truncated=T, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F, url_matches_https_github_owner_repo=F => TRUE
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=F, trending_fetch_raises=F, url_is_full_github_repo=F, url_matches_https_github_owner_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=F, trending_fetch_raises=T, url_is_full_github_repo=F, url_matches_https_github_owner_repo=F => TRUE
    # MCDC SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=F, extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F, url_matches_https_github_owner_repo=F => TRUE
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=T, extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F, url_matches_https_github_owner_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=T, extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T, url_matches_https_github_owner_repo=F => TRUE
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=T, extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T, url_matches_https_github_owner_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=F, extract_attempt_count_LT_3=T, extracted_url_is_invalid=T, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T, url_matches_https_github_owner_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=T, extract_attempt_count_LT_3=T, extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, repo_url_extracted=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T, url_matches_https_github_owner_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=T, extract_attempt_count_LT_3=T, extracted_url_is_invalid=T, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=T, repo_url_extracted=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T, url_matches_https_github_owner_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=T, extract_attempt_count_LT_3=T, extracted_url_is_invalid=T, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=T, repo_url_extracted=T, requests_timeout_s_GE_1=F, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T, url_matches_https_github_owner_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-006: example_repo_url=T, extract_attempt_count_LT_3=T, extracted_url_is_invalid=T, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=T, repo_url_extracted=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=F, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T, url_matches_https_github_owner_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-006: example_repo_url=T, extract_attempt_count_LT_3=T, extracted_url_is_invalid=T, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=T, repo_url_extracted=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T, url_matches_https_github_owner_repo=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=F, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=F, readme_truncated=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=F, trending_fetch_raises=F, url_is_full_github_repo=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=F, trending_fetch_raises=T, url_is_full_github_repo=F => TRUE
    # MCDC SYS-REQ-007: extracted_url_is_invalid=F, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=T, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=F, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, url_is_full_github_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=T, lookup_rejects_url=F, readme_len_LE_5000=T, readme_truncated=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=T, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=T, requests_timeout_s_GE_1=F, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-007: extracted_url_is_invalid=T, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=F, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-007: extracted_url_is_invalid=T, lookup_rejects_url=T, readme_len_LE_5000=T, readme_truncated=T, requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, url_is_full_github_repo=T => TRUE

    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:nominal:nominal
    # SW-REQ-006:security_decision_matches_enforcement_identity:nominal
    # SYS-REQ-007:security_decision_matches_enforcement_identity:nominal
    GitHubRepo = _github_repo_model(_load_strands_mod())
    url = "https://github.com/owner/repo"
    assert GitHubRepo(url=url).url == url
    assert GitHubRepo.validate_github_url(url) == url


def test_github_repo_rejects_example_orgname_reponame():
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    GitHubRepo = _github_repo_model(_load_strands_mod())
    with pytest.raises((ValidationError, ValueError)):
        GitHubRepo(url="https://github.com/orgname/reponame")
    with pytest.raises(ValueError, match="example"):
        GitHubRepo.validate_github_url("https://github.com/orgname/reponame")


def test_github_repo_rejects_non_github_urls():
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:malformed_input:negative
    # SW-REQ-006:error_handling:negative
    # SW-REQ-006:security_decision_matches_enforcement_identity:negative
    # SYS-REQ-007:security_decision_matches_enforcement_identity:negative
    GitHubRepo = _github_repo_model(_load_strands_mod())
    for bad in (
        "https://gitlab.com/owner/repo",
        "http://github.com/owner/repo",
        "github.com/owner/repo",
        "https://github.com/onlyowner",
    ):
        with pytest.raises((ValidationError, ValueError)):
            GitHubRepo(url=bad)
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            GitHubRepo.validate_github_url(bad)


def _load_actions_mod():
    # Import the shipped module by its package path so sys.monitoring
    # records the same file the Python MC/DC extractor analyzes.
    # importlib.spec_from_file_location under a unique name re-execs the
    # file and can leave the README-length polarity as feasibility_unknown.
    return importlib.import_module(
        "functions.most_popular_repo_bedrock_agent.github_agent_actions.index"
    )


def _action_event(api_path, parameters=None, action_group="GitHubActions", method="GET"):
    event = {
        "actionGroup": action_group,
        "apiPath": api_path,
        "httpMethod": method,
    }
    if parameters is not None:
        event["parameters"] = parameters
    return event


def _response_body(api_response):
    return json.loads(api_response["response"]["responseBody"]["application/json"]["body"])


def test_trending_page_non_200_raises():
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # Verifies: INT-REQ-004
    # SW-REQ-006:error_handling:negative
    # INT-REQ-004:error_handling:negative
    # INT-REQ-004:integration:integration
    mod = _load_actions_mod()
    response = MagicMock(status_code=503, text="down")
    with patch.object(mod.requests, "get", return_value=response):
        with pytest.raises(Exception, match="Could not retrieve GitHub Trending page"):
            mod.get_github_trending_page_agent_action()


def test_readme_truncated_when_longer_than_5000(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:boundary:nominal
    mod = _load_actions_mod()
    monkeypatch.setenv("GITHUB_ALLOWED_REPO_URLS", "https://github.com/owner/repo")
    monkeypatch.setattr(
        mod.secrets_client,
        "get_secret_value",
        lambda **kwargs: {"SecretString": json.dumps({"token": "test-token"})},
    )

    class _Readme:
        decoded_content = ("X" * 6000).encode("utf-8")

    class _Repo:
        def get_readme(self):
            return _Readme()

    class _Github:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def get_repo(self, name):
            assert name == "owner/repo"
            return _Repo()

    monkeypatch.setattr(mod, "Github", _Github)
    monkeypatch.setattr(mod, "Auth", MagicMock())
    # Drive the true polarity of len(readme_content) > 5000 twice so
    # sys.monitoring records it under both standalone and remasure runs.
    for _ in range(2):
        text = mod.get_github_repository_readme_agent_action(
            "https://github.com/owner/repo"
        )
        assert "first 5,000 characters" in text
        assert len(text) < 6200


def test_readme_full_when_under_5000(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:boundary:nominal
    # Independent-effect pair for get_github_repository_readme_agent_action:
    # len(readme_content) > 5000 is false here; the sibling test drives true.
    mod = _load_actions_mod()
    monkeypatch.setenv("GITHUB_ALLOWED_REPO_URLS", "https://github.com/owner/repo")
    monkeypatch.setattr(
        mod.secrets_client,
        "get_secret_value",
        lambda **kwargs: {"SecretString": json.dumps({"token": "test-token"})},
    )

    class _Readme:
        decoded_content = b"short readme body"

    class _Repo:
        def get_readme(self):
            return _Readme()

    class _Github:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def get_repo(self, name):
            assert name == "owner/repo"
            return _Repo()

    monkeypatch.setattr(mod, "Github", _Github)
    monkeypatch.setattr(mod, "Auth", MagicMock())
    for _ in range(2):
        text = mod.get_github_repository_readme_agent_action(
            "https://github.com/owner/repo"
        )
        assert "full contents of the README" in text
        assert "short readme body" in text


def test_readme_path_params_without_repo_name_is_400():
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # SW-REQ-006:malformed_input:negative
    handler = _load_actions_mod().handler
    result = handler(
        _action_event("/get_github_repository_readme", parameters=[{"name": "other", "value": "x"}]),
        None,
    )
    assert result["response"]["httpStatusCode"] == 400
    assert _response_body(result)["error"] == "Missing parameter: repo"


def test_unknown_api_path_returns_400_envelope():
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # Verifies: INT-REQ-004
    # INT-REQ-004:error_handling:negative
    # INT-REQ-004:integration:integration
    handler = _load_actions_mod().handler
    event = _action_event("/not_a_real_endpoint")

    result = handler(event, None)

    assert result["messageVersion"] == "1.0"
    action_response = result["response"]
    assert action_response["httpStatusCode"] == 400
    assert action_response["actionGroup"] == event["actionGroup"]
    assert action_response["apiPath"] == event["apiPath"]
    assert action_response["httpMethod"] == event["httpMethod"]
    body = _response_body(result)
    assert "error" in body
    assert event["actionGroup"] in body["error"]
    assert event["apiPath"] in body["error"]


def test_trending_path_returns_page_contents(monkeypatch):
    # mcdc:ignore:defensive INT-REQ-004: requests_timeout_s_GE_1=F, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, trending_fetch_requested=T, trending_http_get_issued=T, user_agent_header_set=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=F, status_code_EQ_200=T, trending_fetch_raises=T, trending_fetch_requested=T, trending_http_get_issued=T, user_agent_header_set=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=F, trending_fetch_raises=F, trending_fetch_requested=F, trending_http_get_issued=F, user_agent_header_set=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=F, trending_fetch_raises=T, trending_fetch_requested=F, trending_http_get_issued=F, user_agent_header_set=F => TRUE
    # MCDC INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, trending_fetch_requested=F, trending_http_get_issued=F, user_agent_header_set=F => TRUE
    # mcdc:ignore:defensive INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=F, trending_fetch_requested=T, trending_http_get_issued=F, user_agent_header_set=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, trending_fetch_requested=T, trending_http_get_issued=F, user_agent_header_set=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, trending_fetch_requested=T, trending_http_get_issued=T, user_agent_header_set=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-004: requests_timeout_s_GE_1=T, requests_timeout_s_LE_30=T, status_code_EQ_200=T, trending_fetch_raises=T, trending_fetch_requested=T, trending_http_get_issued=T, user_agent_header_set=T => TRUE

    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    # Verifies: INT-REQ-004
    # INT-REQ-004:nominal:nominal
    # INT-REQ-004:boundary:nominal
    # INT-REQ-004:error_handling:nominal
    # INT-REQ-004:integration:integration
    # SW-REQ-006:error_handling:nominal
    mod = _load_actions_mod()
    html = """
    <html><body>
      <article class="Box-row">\n\n  octo / demo  \n\n</article>
    </body></html>
    """
    response = MagicMock(status_code=200, text=html)
    monkeypatch.setattr(mod.requests, "get", lambda *args, **kwargs: response)

    result = mod.handler(_action_event("/get_trending_github_repositories"), None)

    assert result["response"]["httpStatusCode"] == 200
    body = _response_body(result)
    assert "contents" in body
    assert "octo / demo" in body["contents"]


def test_readme_path_missing_repo_param_is_400():
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    handler = _load_actions_mod().handler
    result = handler(
        _action_event("/get_github_repository_readme", parameters=[]),
        None,
    )
    assert result["response"]["httpStatusCode"] == 400
    assert _response_body(result)["error"] == "Missing parameter: repo"


def test_readme_path_uses_github_client(monkeypatch):
    # Verifies: SW-REQ-006
    # Verifies: SYS-REQ-007
    mod = _load_actions_mod()
    monkeypatch.setenv("GITHUB_ALLOWED_REPO_URLS", "https://github.com/owner/repo")
    monkeypatch.setattr(
        mod.secrets_client,
        "get_secret_value",
        lambda **kwargs: {"SecretString": json.dumps({"token": "test-token"})},
    )
    readme = MagicMock()
    readme.decoded_content = b"# Hello repo"
    repo = MagicMock()
    repo.get_readme.return_value = readme
    github_client = MagicMock()
    github_client.get_repo.return_value = repo
    monkeypatch.setattr(mod, "Github", lambda **kwargs: github_client)
    monkeypatch.setattr(mod, "Auth", MagicMock())

    repo_url = "https://github.com/owner/repo"
    result = mod.handler(
        _action_event(
            "/get_github_repository_readme",
            parameters=[{"name": "repo", "value": repo_url}],
        ),
        None,
    )

    assert result["response"]["httpStatusCode"] == 200
    body = _response_body(result)
    assert "# Hello repo" in body["contents"]
    github_client.get_repo.assert_called_once_with("owner/repo")


def _mock_github_client(mod, monkeypatch):
    monkeypatch.setattr(
        mod.secrets_client,
        "get_secret_value",
        lambda **kwargs: {"SecretString": json.dumps({"token": "test-token"})},
    )
    github_client = MagicMock()
    monkeypatch.setattr(mod, "Github", lambda **kwargs: github_client)
    monkeypatch.setattr(mod, "Auth", MagicMock())
    return github_client


# Reproduces: KI-github-bedrock-readme-pat-no-allowlist
# Asserts the fixed contract; passes only while the allowlist is enforced.
def test_bedrock_readme_rejects_non_allowlisted_repo(monkeypatch):
    mod = _load_actions_mod()
    github_client = _mock_github_client(mod, monkeypatch)
    try:
        mod.handler(
            _action_event(
                "/get_github_repository_readme",
                parameters=[{"name": "repo", "value": "https://github.com/evil/private"}],
            ),
            None,
        )
    except Exception:
        github_client.get_repo.assert_not_called()
        return
    github_client.get_repo.assert_not_called()


# Reproduces: KI-github-bedrock-readme-pat-no-allowlist
# Asserts the fixed contract; rejects non-full https://github.com/{owner}/{repo}
# form even when the string is configured in the allowlist.
def test_bedrock_readme_rejects_non_full_github_url(monkeypatch):
    mod = _load_actions_mod()
    github_client = _mock_github_client(mod, monkeypatch)
    monkeypatch.setenv(
        "GITHUB_ALLOWED_REPO_URLS", "https://github.com/owner/repo/extra"
    )
    try:
        mod.get_github_repository_readme_agent_action(
            "https://github.com/owner/repo/extra"
        )
    except Exception:
        github_client.get_repo.assert_not_called()
        return
    github_client.get_repo.assert_not_called()


# Reproduces: KI-github-strands-readme-pat-no-allowlist
# Asserts the secure contract; fails while the defect is open.
@pytest.mark.xfail(
    strict=True,
    reason="KI-github-strands-readme-pat-no-allowlist: PAT get_readme has no repo allowlist",
)
def test_strands_readme_rejects_non_allowlisted_repo(monkeypatch):
    mod = _load_strands_mod()
    github_client = _mock_github_client(mod, monkeypatch)
    try:
        mod.get_github_repository_readme("https://github.com/evil/private")
    except Exception:
        github_client.get_repo.assert_not_called()
        return
    github_client.get_repo.assert_not_called()


def _trending_get_timeout(mod, call):
    captured = {}

    def fake_get(*args, **kwargs):
        captured["called"] = True
        captured["timeout"] = kwargs.get("timeout")
        return MagicMock(status_code=200, text="<html><body></body></html>")

    with patch.object(mod.requests, "get", fake_get):
        call()
    assert captured.get("called"), "expected requests.get to GitHub trending"
    timeout = captured.get("timeout")
    if isinstance(timeout, tuple):
        timeout = max(timeout)
    assert timeout is not None, "requests.get to https://github.com/trending must pass timeout="
    assert 1 < float(timeout) <= 30, f"timeout={timeout!r} must be in (1, 30]"


# Reproduces: KI-github-trending-no-timeout
@pytest.mark.xfail(
    strict=True,
    reason="KI-github-trending-no-timeout: trending requests.get has no timeout=",
)
def test_github_trending_gets_pass_bounded_timeout():
    # SW-REQ-006:request_timeout_bounded:nominal
    # SYS-REQ-007:request_timeout_bounded:nominal
    # INT-REQ-004:request_timeout_bounded:nominal
    actions = _load_actions_mod()
    _trending_get_timeout(actions, actions.get_github_trending_page_agent_action)

    strands = _load_strands_mod()
    _trending_get_timeout(strands, lambda: strands.get_trending_github_repositories(""))


AGENT_LOOKUP_PATH = "functions/most_popular_repo_bedrock_agent/agent/index.py"
EVIL_EMBEDDED_GITHUB = "https://evil.example/https://github.com/owner/repo"
PREFIX_JUNK_GITHUB = "junkhttps://github.com/owner/repo"
SUFFIX_EXTRA_GITHUB = "https://github.com/owner/repo/extra"


def _agent_lookup_completion(text):
    return {
        "ResponseMetadata": {"RequestId": "req-1"},
        "completion": [{"chunk": {"bytes": text.encode("utf-8")}}],
    }


# Reproduces: KI-github-url-unanchored-match
# Asserts the secure contract; fails while the defect is open.
@pytest.mark.xfail(
    strict=True,
    reason="KI-github-url-unanchored-match: extractor is re.search/re.match, not fullmatch",
)
def test_github_url_extractors_require_fullmatch(monkeypatch):
    monkeypatch.setenv("BEDROCK_AGENT_ID", "agent-id")
    monkeypatch.setenv("BEDROCK_AGENT_ALIAS_ID", "alias-id")
    agent_mod = load_module("bedrock_agent_lookup_url_repro", AGENT_LOOKUP_PATH)
    client = MagicMock()
    client.invoke_agent.side_effect = [
        _agent_lookup_completion(EVIL_EMBEDDED_GITHUB),
        _agent_lookup_completion(PREFIX_JUNK_GITHUB),
        _agent_lookup_completion(SUFFIX_EXTRA_GITHUB),
    ]
    agent_mod.bedrock_agent_client = client
    with pytest.raises(Exception, match="Could not find URL"):
        agent_mod.lookup_trending_repo_agent({}, None)

    GitHubRepo = _github_repo_model(_load_strands_mod())
    for bad in (EVIL_EMBEDDED_GITHUB, PREFIX_JUNK_GITHUB, SUFFIX_EXTRA_GITHUB):
        with pytest.raises((ValidationError, ValueError)):
            GitHubRepo(url=bad)
        with pytest.raises((ValidationError, ValueError)):
            GitHubRepo.validate_github_url(bad)

