"""Reproducers for MoviePitch Choice pitch-index glob."""
import ast
from pathlib import Path

import pytest

MOVIE_PITCH = Path("/workspace/stacks/movie_pitch_stack.py")
ALLOWED_PITCH_SELECTORS = {"1", "2", "3"}


def _literal_or_joined(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                parts.append(_index_placeholder(value.value))
            else:
                parts.append("{dyn}")
        return "".join(parts)
    return ast.unparse(node)


def _index_placeholder(expr):
    if (
        isinstance(expr, ast.BinOp)
        and isinstance(expr.op, ast.Add)
        and isinstance(expr.left, ast.Name)
        and expr.left.id == "i"
        and isinstance(expr.right, ast.Constant)
        and expr.right.value == 1
    ):
        return "{i+1}"
    return "{dyn}"


def pitch_choice_match_patterns(source: str):
    """Return Condition.string_matches pattern templates from the stack source."""
    tree = ast.parse(source)
    patterns = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "string_matches":
                if len(node.args) >= 2:
                    patterns.append(_literal_or_joined(node.args[1]))
                else:
                    for kw in node.keywords:
                        if kw.arg in {"value", "pattern"}:
                            patterns.append(_literal_or_joined(kw.value))
            self.generic_visit(node)

    Visitor().visit(tree)
    return patterns


def pitch_choice_equals_values(source: str):
    """Return string_equals / string_equals_path literals that look like pitch indexes."""
    tree = ast.parse(source)
    values = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in {
                "string_equals",
                "string_equals_path",
            }:
                args = list(node.args)
                if len(args) >= 2:
                    text = _literal_or_joined(args[1])
                    if text in ALLOWED_PITCH_SELECTORS or "{i+1}" in text:
                        values.append(text)
            self.generic_visit(node)

    Visitor().visit(tree)
    return values


def expand_index_patterns(patterns):
    expanded = []
    for pattern in patterns:
        if "{i+1}" in pattern:
            for i in range(3):
                expanded.append(pattern.replace("{i+1}", str(i + 1)))
        else:
            expanded.append(pattern)
    return expanded


# Reproduces: KI-moviepitch-pitch-glob-1star
@pytest.mark.xfail(
    strict=True,
    reason="KI-moviepitch-pitch-glob-1star: Choice string_matches uses {i+1}* suffix wildcard",
)
def test_movie_pitch_choice_selector_is_exact_digit():
    source = MOVIE_PITCH.read_text()
    match_patterns = expand_index_patterns(pitch_choice_match_patterns(source))
    equals_values = expand_index_patterns(pitch_choice_equals_values(source))

    wildcards = [pattern for pattern in match_patterns if "*" in pattern]
    assert wildcards == [], (
        "Select Model's Pitch Choice must use exact digit / enum {1,2,3}, "
        f"not suffix wildcard {wildcards!r} (1* matches 10/1foo and selects Red)"
    )

    exact = {
        value
        for value in match_patterns + equals_values
        if value in ALLOWED_PITCH_SELECTORS
    }
    assert exact == ALLOWED_PITCH_SELECTORS, (
        "pitch selector must be exact enum {1,2,3}; "
        f"got matches={match_patterns!r} equals={equals_values!r}"
    )
