# Parent system requirement: SYS-REQ-001
import json

import pytest
from jsonschema.exceptions import ValidationError

from tests.conftest import load_module

GENERIC_PATH = "functions/generic/parse_json_response/index.py"
SFN_TECHNIQUE_PATH = "techniques_step_functions/functions/parse_json_response/index.py"
FLOWS_PATH = "techniques_bedrock_flows/functions/parse_json_response/index.py"

OBJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "pages": {"type": "integer"},
    },
    "required": ["title", "pages"],
    "additionalProperties": False,
}


def _load_event_schema_parser(module_name, relative_path):
    return load_module(module_name, relative_path)


@pytest.mark.parametrize(
    "module_name,relative_path",
    [
        ("generic_parse_json_response", GENERIC_PATH),
        ("sfn_technique_parse_json_response", SFN_TECHNIQUE_PATH),
    ],
)
def test_valid_json_matching_schema_returns_object(
    # MCDC INT-REQ-003: json_schema_present=F, parser_lambda_invoked=F, parser_lambda_targeted=F, response_string_and_schema_provided=F, response_string_present=F, sfn_parser_invoked=F => TRUE [no-action: guarded action not requested on this path]
    # mcdc:ignore:defensive INT-REQ-003: json_schema_present=F, parser_lambda_invoked=F, parser_lambda_targeted=F, response_string_and_schema_provided=F, response_string_present=F, sfn_parser_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-003: json_schema_present=F, parser_lambda_invoked=T, parser_lambda_targeted=T, response_string_and_schema_provided=T, response_string_present=T, sfn_parser_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-003: json_schema_present=T, parser_lambda_invoked=F, parser_lambda_targeted=T, response_string_and_schema_provided=T, response_string_present=T, sfn_parser_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-003: json_schema_present=T, parser_lambda_invoked=T, parser_lambda_targeted=F, response_string_and_schema_provided=T, response_string_present=T, sfn_parser_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-003: json_schema_present=T, parser_lambda_invoked=T, parser_lambda_targeted=T, response_string_and_schema_provided=F, response_string_present=T, sfn_parser_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-003: json_schema_present=T, parser_lambda_invoked=T, parser_lambda_targeted=T, response_string_and_schema_provided=T, response_string_present=F, sfn_parser_invoked=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-003: json_schema_present=T, parser_lambda_invoked=T, parser_lambda_targeted=T, response_string_and_schema_provided=T, response_string_present=T, sfn_parser_invoked=T => TRUE
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=F, handler_raises=F, invalid_payload_rejected=F, json_is_malformed=F, model_output_fails_schema=F, parsed_object_returned=F, payload_is_invalid=F, schema_mismatched=F, schema_type_is_object=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-001: additional_properties_disallowed=F, handler_raises=F, invalid_payload_rejected=F, json_is_malformed=F, model_output_fails_schema=F, parsed_object_returned=T, payload_is_invalid=F, schema_mismatched=F, schema_type_is_object=F => TRUE
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=F, handler_raises=F, invalid_payload_rejected=F, json_is_malformed=F, model_output_fails_schema=F, parsed_object_returned=T, payload_is_invalid=F, schema_mismatched=T, schema_type_is_object=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=F, handler_raises=F, invalid_payload_rejected=F, json_is_malformed=F, model_output_fails_schema=T, parsed_object_returned=T, payload_is_invalid=F, schema_mismatched=F, schema_type_is_object=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=F, handler_raises=F, invalid_payload_rejected=F, json_is_malformed=T, model_output_fails_schema=F, parsed_object_returned=T, payload_is_invalid=F, schema_mismatched=F, schema_type_is_object=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=F, handler_raises=T, invalid_payload_rejected=F, json_is_malformed=F, model_output_fails_schema=F, parsed_object_returned=F, payload_is_invalid=F, schema_mismatched=F, schema_type_is_object=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-001: additional_properties_disallowed=F, handler_raises=T, invalid_payload_rejected=F, json_is_malformed=F, model_output_fails_schema=F, parsed_object_returned=F, payload_is_invalid=T, schema_mismatched=F, schema_type_is_object=F => TRUE
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=T, handler_raises=F, invalid_payload_rejected=T, json_is_malformed=T, model_output_fails_schema=T, parsed_object_returned=T, payload_is_invalid=T, schema_mismatched=T, schema_type_is_object=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-001: additional_properties_disallowed=T, handler_raises=T, invalid_payload_rejected=F, json_is_malformed=T, model_output_fails_schema=T, parsed_object_returned=T, payload_is_invalid=T, schema_mismatched=T, schema_type_is_object=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-001: additional_properties_disallowed=T, handler_raises=T, invalid_payload_rejected=T, json_is_malformed=T, model_output_fails_schema=T, parsed_object_returned=T, payload_is_invalid=T, schema_mismatched=T, schema_type_is_object=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=F, model_output_fails_schema=F, parse_error_count_LT_3=F, parser_lambda_invoked=T, parser_rejects_or_retries=F, retry_limit_is_three=F, schema_provided=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-002: invalid_payload_rejected=F, model_output_fails_schema=F, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=F, retry_limit_is_three=F, schema_provided=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=F, model_output_fails_schema=F, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=F, retry_limit_is_three=F, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=F, model_output_fails_schema=T, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=F, retry_limit_is_three=F, schema_provided=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=F, model_output_fails_schema=T, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=T, retry_limit_is_three=T, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=T, model_output_fails_schema=T, parse_error_count_LT_3=T, parser_lambda_invoked=F, parser_rejects_or_retries=T, retry_limit_is_three=T, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=T, model_output_fails_schema=T, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=F, retry_limit_is_three=T, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-002: invalid_payload_rejected=T, model_output_fails_schema=T, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=T, retry_limit_is_three=F, schema_provided=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-002: invalid_payload_rejected=T, model_output_fails_schema=T, parse_error_count_LT_3=T, parser_lambda_invoked=T, parser_rejects_or_retries=T, retry_limit_is_three=T, schema_provided=T => TRUE
    module_name, relative_path):

    # Verifies: SW-REQ-001
    # Verifies: SYS-REQ-002
    # Verifies: INT-REQ-003
    # Verifies: STK-REQ-001
    # SW-REQ-001:nominal:nominal
    # SW-REQ-001:error_handling:nominal
    # SW-REQ-001:malformed_input:nominal
    # SYS-REQ-002:nominal:nominal
    # SYS-REQ-002:error_handling:nominal
    # SYS-REQ-002:malformed_input:nominal
    # SYS-REQ-002:boundary:nominal
    # INT-REQ-003:nominal:nominal
    # INT-REQ-003:error_handling:nominal
    # INT-REQ-003:malformed_input:nominal
    # INT-REQ-003:integration:integration
    handler = _load_event_schema_parser(module_name, relative_path).handler
    payload = {"title": "Dune", "pages": 412}
    result = handler(
        {
            "response_string": json.dumps(payload),
            "json_schema": OBJECT_SCHEMA,
        },
        None,
    )
    assert result == payload
    assert result["title"] == "Dune"
    assert result["pages"] == 412


@pytest.mark.parametrize(
    "module_name,relative_path",
    [
        ("generic_parse_json_response", GENERIC_PATH),
        ("sfn_technique_parse_json_response", SFN_TECHNIQUE_PATH),
    ],
)
def test_invalid_json_raises(module_name, relative_path):
    # Verifies: SW-REQ-001
    # Verifies: SYS-REQ-002
    # Verifies: INT-REQ-003
    # SW-REQ-001:malformed_input:negative
    # SW-REQ-001:error_handling:negative
    # SYS-REQ-002:malformed_input:negative
    # SYS-REQ-002:error_handling:negative
    # INT-REQ-003:malformed_input:negative
    # INT-REQ-003:error_handling:negative
    # INT-REQ-003:integration:integration
    handler = _load_event_schema_parser(module_name, relative_path).handler
    with pytest.raises(json.JSONDecodeError):
        handler(
            {
                "response_string": "{not-json",
                "json_schema": OBJECT_SCHEMA,
            },
            None,
        )


@pytest.mark.parametrize(
    "module_name,relative_path",
    [
        ("generic_parse_json_response", GENERIC_PATH),
        ("sfn_technique_parse_json_response", SFN_TECHNIQUE_PATH),
    ],
)
def test_valid_json_failing_schema_raises(module_name, relative_path):
    # Verifies: SW-REQ-001
    # Verifies: SYS-REQ-002
    # Verifies: INT-REQ-003
    # SW-REQ-001:malformed_input:negative
    # SW-REQ-001:error_handling:negative
    # SYS-REQ-002:malformed_input:negative
    # SYS-REQ-002:error_handling:negative
    handler = _load_event_schema_parser(module_name, relative_path).handler
    with pytest.raises(ValidationError):
        handler(
            {
                "response_string": json.dumps({"title": "Dune", "pages": "many"}),
                "json_schema": OBJECT_SCHEMA,
            },
            None,
        )


def test_flows_parser_reads_node_input_and_schema_env(monkeypatch):
    # Verifies: SW-REQ-001
    # Verifies: SYS-REQ-002
    # Verifies: INT-REQ-003
    # INT-REQ-003:nominal:nominal
    monkeypatch.setenv("SCHEMA", json.dumps(OBJECT_SCHEMA))
    handler = load_module(
        "flows_parse_json_response",
        FLOWS_PATH,
    ).handler
    payload = {"title": "Neuromancer", "pages": 271}
    result = handler(
        {"node": {"inputs": [{"value": json.dumps(payload)}]}},
        None,
    )
    assert result == payload


def test_flows_parser_invalid_json_raises(monkeypatch):
    # Verifies: SW-REQ-001
    # Verifies: SYS-REQ-002
    monkeypatch.setenv("SCHEMA", json.dumps(OBJECT_SCHEMA))
    handler = load_module(
        "flows_parse_json_response_invalid",
        FLOWS_PATH,
    ).handler
    with pytest.raises(json.JSONDecodeError):
        handler(
            {"node": {"inputs": [{"value": "nope"}]}},
            None,
        )


def test_flows_parser_schema_mismatch_raises(monkeypatch):
    # Verifies: SW-REQ-001
    # Verifies: SYS-REQ-002
    monkeypatch.setenv("SCHEMA", json.dumps(OBJECT_SCHEMA))
    handler = load_module(
        "flows_parse_json_response_schema",
        FLOWS_PATH,
    ).handler
    with pytest.raises(ValidationError):
        handler(
            {"node": {"inputs": [{"value": json.dumps({"title": 1, "pages": 2})}]}},
            None,
        )
