import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

WORKSPACE = Path("/workspace")

# Keep unit tests off real AWS even if a default credential chain exists.
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
os.environ.setdefault("AWS_SESSION_TOKEN", "testing")

if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))


class DummyCdkStack:
    """Minimal Stack stand-in so CDK stack __init__ bodies run under mocks."""

    def __init__(self, scope=None, construct_id=None, **kwargs):
        self.scope = scope
        self.construct_id = construct_id

    @classmethod
    def of(cls, scope):
        owner = MagicMock()
        owner.region = "us-east-1"
        owner.account = "123456789012"
        owner.format_arn.return_value = (
            "arn:aws:sns:us-east-1:123456789012:"
            "bedrock-serverless-prompt-chaining-notifications"
        )
        return owner

    def format_arn(self, **kwargs):
        return (
            "arn:aws:sns:us-east-1:123456789012:"
            "bedrock-serverless-prompt-chaining-notifications"
        )


# Documents: SW-REQ-001
# KnownIssue: KI-untraced-test-harness
def install_cdk_stubs(extra_modules=None):
    """Stub aws_cdk before importing stack modules. Stack is a real class."""
    modules = [
        "aws_cdk",
        "aws_cdk.aws_bedrock",
        "aws_cdk.aws_iam",
        "aws_cdk.aws_lambda",
        "aws_cdk.aws_lambda_python_alpha",
        "aws_cdk.aws_stepfunctions",
        "aws_cdk.aws_stepfunctions_tasks",
        "aws_cdk.aws_cloudwatch",
        "aws_cdk.aws_cloudwatch_actions",
        "aws_cdk.aws_sns",
        "constructs",
        "jsii",
    ]
    if extra_modules:
        modules.extend(extra_modules)
    for name in modules:
        sys.modules.setdefault(name, MagicMock())
    sys.modules["aws_cdk"].Stack = DummyCdkStack
    return sys.modules["aws_cdk"]


# Documents: SW-REQ-001
# KnownIssue: KI-untraced-test-harness
def load_module(module_name, relative_path, extra_sys_modules=None):
    """Import a production file under a unique module name."""
    if extra_sys_modules:
        for name, module in extra_sys_modules.items():
            sys.modules.setdefault(name, module)

    path = WORKSPACE / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
# KnownIssue: KI-untraced-test-harness
def identity_tool():
    """A @tool stand-in that leaves the wrapped function intact."""
    return lambda fn: fn


# KnownIssue: KI-untraced-test-harness
def strands_import_stubs():
    strands = MagicMock()
    strands.tool = lambda fn: fn
    models = MagicMock()
    return {
        "strands": strands,
        "strands.models": models,
    }


# KnownIssue: KI-untraced-test-harness
def md2pdf_import_stubs(md2pdf_fn=None):
    core = MagicMock()
    core.md2pdf = md2pdf_fn if md2pdf_fn is not None else MagicMock()
    pkg = MagicMock()
    pkg.core = core
    return {
        "md2pdf": pkg,
        "md2pdf.core": core,
    }
