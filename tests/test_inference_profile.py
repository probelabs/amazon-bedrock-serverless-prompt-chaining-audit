"""Drive the inference-profile foundation-model id split (`.` present vs absent)."""

import sys

from tests.conftest import DummyCdkStack, install_cdk_stubs, load_module

install_cdk_stubs()


def _identity_implements(*_args, **_kwargs):
    def deco(cls):
        return cls

    return deco


def _load_profile(module_name, relative_path):
    jsii = sys.modules["jsii"]
    jsii.implements = _identity_implements
    jsii.member = _identity_implements
    extra = {"aws_cdk": sys.modules["aws_cdk"], "jsii": jsii}
    extra["aws_cdk"].Stack = DummyCdkStack
    return load_module(module_name, relative_path, extra_sys_modules=extra)


PROFILE_PATHS = [
    ("stacks_inference_profile", "stacks/inference_profile.py"),
    (
        "sfn_inference_profile",
        "techniques_step_functions/stacks/inference_profile.py",
    ),
    (
        "flows_inference_profile",
        "techniques_bedrock_flows/stacks/inference_profile.py",
    ),
]


def test_inference_profile_splits_dotted_id():
    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-006
    # SW-REQ-010:nominal:nominal
    # SYS-REQ-006:nominal:nominal
    dotted = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
    for name, path in PROFILE_PATHS:
        mod = _load_profile(name + "_dotted", path)
        profile = mod.InferenceProfile(object(), "Profile", dotted)
        assert profile._foundation_model_id == "anthropic.claude-haiku-4-5-20251001-v1:0"
        assert "foundation-model/anthropic.claude-haiku-4-5-20251001-v1:0" in (
            profile.get_foundation_model_arn_pattern()
        )


def test_inference_profile_keeps_undotted_id():
    # Verifies: SW-REQ-010
    # Verifies: SYS-REQ-006
    # SW-REQ-010:error_handling:nominal
    # SYS-REQ-006:error_handling:nominal
    # The undotted case is the `"." not in inference_profile_id` polarity.
    undotted = "anthropic-claude-haiku"
    for name, path in PROFILE_PATHS:
        mod = _load_profile(name + "_plain", path)
        profile = mod.InferenceProfile(object(), "Profile", undotted)
        assert profile._foundation_model_id == undotted
        assert profile.get_foundation_model_arn_pattern().endswith(
            f"foundation-model/{undotted}"
        )
