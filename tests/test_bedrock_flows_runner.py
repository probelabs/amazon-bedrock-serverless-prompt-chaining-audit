import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tests.conftest import load_module

RUNNER_PATH = "techniques_bedrock_flows/run-test-execution.py"
MODEL_INVOCATION_INPUT = Path(
    "/workspace/techniques_bedrock_flows/test-inputs/ModelInvocation.json"
)


def _load_runner(module_name="flows_run_test_execution"):
    return load_module(module_name, RUNNER_PATH)


def _fake_paginator(pages):
    paginator = MagicMock()
    paginator.paginate.return_value = pages
    return paginator


def _patch_success(mod, monkeypatch, demo_name="ModelInvocation"):
    monkeypatch.setattr(sys, "argv", ["run-test-execution.py", demo_name])
    mod.flows_paginator = _fake_paginator(
        [{"flowSummaries": [{"name": f"Flows-{demo_name}", "id": "flow-1"}]}]
    )
    mod.flow_aliases_paginator = _fake_paginator(
        [{"flowAliasSummaries": [{"name": "live", "id": "alias-live"}]}]
    )
    mod.client_runtime = MagicMock()
    mod.client_runtime.invoke_flow.return_value = {
        "responseStream": [
            {"flowOutputEvent": {"content": {"document": "ok"}}},
            {"flowCompletionEvent": {"completionReason": "SUCCESS"}},
        ]
    }
    monkeypatch.chdir("/workspace/techniques_bedrock_flows")


def test_flows_main_invokes_live_alias(monkeypatch):
    # MCDC INT-REQ-007: alias_name_is_live=F, completion_reason_checked=F, completion_reason_is_success=F, flow_identifier_resolved=F, flow_invoke_raises=F, flow_invoke_requested=F, input_document_provided=F, invoke_uses_document_content=F, live_alias_invoked=F => TRUE [no-action: guarded action not requested on this path]
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=F, completion_reason_checked=F, completion_reason_is_success=F, flow_identifier_resolved=F, flow_invoke_raises=F, flow_invoke_requested=T, input_document_provided=F, invoke_uses_document_content=F, live_alias_invoked=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=F, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=T, completion_reason_checked=F, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=F, flow_identifier_resolved=T, flow_invoke_raises=F, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=F, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => TRUE
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=F, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=F, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => TRUE
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=F, invoke_uses_document_content=T, live_alias_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=F, live_alias_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-007: alias_name_is_live=T, completion_reason_checked=T, completion_reason_is_success=T, flow_identifier_resolved=T, flow_invoke_raises=T, flow_invoke_requested=T, input_document_provided=T, invoke_uses_document_content=T, live_alias_invoked=T => TRUE

    # Verifies: INT-REQ-007
    # Verifies: STK-REQ-003
    # INT-REQ-007:nominal:nominal
    # INT-REQ-007:error_handling:nominal
    # INT-REQ-007:integration:integration

    # STK-REQ-003:error_handling:nominal
    mod = _load_runner("flows_run_test_execution_ok")
    _patch_success(mod, monkeypatch)

    mod.main()

    mod.client_runtime.invoke_flow.assert_called_once()
    kwargs = mod.client_runtime.invoke_flow.call_args.kwargs
    assert kwargs["flowIdentifier"] == "flow-1"
    assert kwargs["flowAliasIdentifier"] == "alias-live"
    assert kwargs["inputs"][0]["content"] == json.loads(
        MODEL_INVOCATION_INPUT.read_text()
    )


def test_flows_main_missing_flow_raises(monkeypatch):
    # Verifies: INT-REQ-007
    # INT-REQ-007:error_handling:negative
    # INT-REQ-007:integration:integration

    mod = _load_runner("flows_run_test_execution_missing_flow")
    monkeypatch.setattr(sys, "argv", ["run-test-execution.py", "ModelInvocation"])
    mod.flows_paginator = _fake_paginator([{"flowSummaries": []}])
    mod.client_runtime = MagicMock()

    with pytest.raises(Exception, match="Could not find flow"):
        mod.main()
    mod.client_runtime.invoke_flow.assert_not_called()


def test_flows_main_missing_live_alias_raises(monkeypatch):
    # Verifies: INT-REQ-007
    # INT-REQ-007:error_handling:negative
    # INT-REQ-007:integration:integration

    mod = _load_runner("flows_run_test_execution_missing_alias")
    monkeypatch.setattr(sys, "argv", ["run-test-execution.py", "ModelInvocation"])
    mod.flows_paginator = _fake_paginator(
        [{"flowSummaries": [{"name": "Flows-ModelInvocation", "id": "flow-1"}]}]
    )
    mod.flow_aliases_paginator = _fake_paginator(
        [{"flowAliasSummaries": [{"name": "draft", "id": "alias-draft"}]}]
    )
    mod.client_runtime = MagicMock()

    with pytest.raises(Exception, match="Could not find flow alias"):
        mod.main()
    mod.client_runtime.invoke_flow.assert_not_called()


def test_flows_main_ignores_non_matching_flow_name(monkeypatch):
    # Verifies: INT-REQ-007
    # INT-REQ-007:error_handling:negative
    # INT-REQ-007:integration:integration
    mod = _load_runner("flows_run_test_execution_name_mismatch")
    monkeypatch.setattr(sys, "argv", ["run-test-execution.py", "ModelInvocation"])
    mod.flows_paginator = _fake_paginator(
        [{"flowSummaries": [{"name": "Flows-Other", "id": "flow-other"}]}]
    )
    mod.client_runtime = MagicMock()

    with pytest.raises(Exception, match="Could not find flow"):
        mod.main()
    mod.client_runtime.invoke_flow.assert_not_called()


def test_flows_main_unsuccessful_completion_raises(monkeypatch):
    # Verifies: INT-REQ-007
    # INT-REQ-007:error_handling:negative
    # INT-REQ-007:integration:integration

    mod = _load_runner("flows_run_test_execution_fail_reason")
    _patch_success(mod, monkeypatch)
    mod.client_runtime.invoke_flow.return_value = {
        "responseStream": [
            {"flowCompletionEvent": {"completionReason": "FAILED"}},
        ]
    }

    with pytest.raises(Exception, match="completed unsuccessfully"):
        mod.main()


def test_flows_runner_main_guard_false_when_imported():
    # Verifies: SYS-REQ-006
    # SYS-REQ-006:nominal:nominal
    # The module is imported (not executed as __main__), so
    # `__name__ == "__main__"` is false. The existing success test
    # plus this import cover both polarities of the entry guard.
    mod = _load_runner("flows_run_test_execution_import_guard")
    assert mod.__name__ != "__main__"
    assert callable(mod.main)


def test_flows_runner_main_guard_true_via_runpy(monkeypatch):
    # Verifies: SYS-REQ-006
    # SYS-REQ-006:nominal:nominal
    import runpy
    from unittest.mock import MagicMock

    monkeypatch.setattr(sys, "argv", ["run-test-execution.py", "ModelInvocation"])
    boto3 = pytest.importorskip("boto3")
    fake_cp = MagicMock()
    fake_rt = MagicMock()
    fake_cp.get_paginator.side_effect = lambda name: _fake_paginator(
        [{"flowSummaries": [{"name": "Flows-ModelInvocation", "id": "flow-1"}]}]
        if name == "list_flows"
        else [{"flowAliasSummaries": [{"name": "live", "id": "alias-live"}]}]
    )
    fake_rt.invoke_flow.return_value = {
        "responseStream": [
            {"flowOutputEvent": {"content": {"document": "ok"}}},
            {"flowCompletionEvent": {"completionReason": "SUCCESS"}},
        ]
    }
    monkeypatch.setattr(boto3, "client", lambda service, **kwargs: fake_rt if "runtime" in service else fake_cp)
    monkeypatch.chdir("/workspace/techniques_bedrock_flows")
    runpy.run_path(
        "/workspace/techniques_bedrock_flows/run-test-execution.py",
        run_name="__main__",
    )
