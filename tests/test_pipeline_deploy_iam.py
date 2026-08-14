"""Reproducers for unrestricted CodeBuild deploy roles in pipeline_stack.py."""
import ast
from pathlib import Path

import pytest

PIPELINE_STACK = Path("/workspace/pipeline/pipeline_stack.py")


def _const_str_list(node):
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values = []
    for elt in node.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
            values.append(elt.value)
        else:
            return None
    return values


def deploy_role_policies(source: str):
    """Map PipelineProject construct id -> [(actions, resources), ...]."""
    tree = ast.parse(source)
    policies = {}
    var_to_id = {}

    class Visitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                value = node.value
                if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute):
                    if value.func.attr == "PipelineProject":
                        cid = None
                        if len(value.args) >= 2 and isinstance(value.args[1], ast.Constant):
                            cid = value.args[1].value
                        if cid:
                            var_to_id[name] = cid
                            policies.setdefault(cid, [])
            self.generic_visit(node)

        def visit_Call(self, node):
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_to_role_policy"
                and isinstance(node.func.value, ast.Name)
            ):
                cid = var_to_id.get(node.func.value.id)
                if cid and node.args:
                    stmt = node.args[0]
                    if isinstance(stmt, ast.Call):
                        actions = resources = None
                        for kw in stmt.keywords:
                            if kw.arg == "actions":
                                actions = _const_str_list(kw.value)
                            elif kw.arg == "resources":
                                resources = _const_str_list(kw.value)
                        if actions is not None and resources is not None:
                            policies.setdefault(cid, []).append((actions, resources))
            self.generic_visit(node)

    Visitor().visit(tree)
    return policies


def _star_star(policies):
    return [p for p in policies if p == (["*"], ["*"])]


def test_deploy_roles_still_grant_star_star():
    # Verifies: SYS-REQ-011
    # SYS-REQ-011:error_handling:negative
    # Characterizes the live sample: both deploy roles still grant Action=* Resource=*.
    policies = deploy_role_policies(PIPELINE_STACK.read_text())
    assert _star_star(policies["DeployExamples"])
    assert _star_star(policies["DeployDemoApp"])


# Reproduces: KI-pipeline-deploy-examples-star-star
@pytest.mark.xfail(
    strict=True,
    reason="KI-pipeline-deploy-examples-star-star: DeployExamples still grants Action=* Resource=*",
)
def test_deploy_examples_role_has_no_star_star_policy():
    policies = deploy_role_policies(PIPELINE_STACK.read_text())
    assert "DeployExamples" in policies
    assert _star_star(policies["DeployExamples"]) == [], (
        "DeployExamples CodeBuild role must not attach PolicyStatement("
        "actions=['*'], resources=['*']) at pipeline/pipeline_stack.py:167-169"
    )


# Reproduces: KI-pipeline-deploy-demo-star-star
@pytest.mark.xfail(
    strict=True,
    reason="KI-pipeline-deploy-demo-star-star: DeployDemoApp still grants Action=* Resource=*",
)
def test_deploy_demo_app_role_has_no_star_star_policy():
    policies = deploy_role_policies(PIPELINE_STACK.read_text())
    assert "DeployDemoApp" in policies
    assert _star_star(policies["DeployDemoApp"]) == [], (
        "DeployDemoApp CodeBuild role must not attach PolicyStatement("
        "actions=['*'], resources=['*']) at pipeline/pipeline_stack.py:286-288"
    )
