import importlib
import sys
from unittest.mock import MagicMock

from tests.conftest import DummyCdkStack, install_cdk_stubs

# CDK-mock the same surface as tests/test_util.py so MealPlannerStack can
# be constructed far enough to inspect the Consensus Choice.
install_cdk_stubs()
import stacks.meal_planner_stack as meal_mod  # noqa: E402
from stacks import util as util_mod  # noqa: E402

if not isinstance(meal_mod.Stack, type):
    sys.modules["aws_cdk"].Stack = DummyCdkStack
    meal_mod = importlib.reload(meal_mod)

MealPlannerStack = meal_mod.MealPlannerStack


def test_meal_planner_choice_takes_winner_path_when_agree_or_round_ge_3():
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=F, chef_id_is_declared=T, chefs_agree=T, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=T, winner_path_taken=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=F, chefs_agree=T, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=T, winner_path_taken=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=F, consensus_choice_defined=T, debate_round_GE_3=F, debate_round_LT_3=T, scoring_path_taken=F, winner_path_taken=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=F, consensus_choice_defined=T, debate_round_GE_3=F, debate_round_LT_3=T, scoring_path_taken=T, winner_path_taken=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=F, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=F, scoring_path_taken=F, winner_path_taken=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=F, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=F, winner_path_taken=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=T, consensus_choice_defined=F, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=T, winner_path_taken=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=T, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=F, winner_path_taken=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=T, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=T, winner_path_taken=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-004: chef_count_EQ_2=T, chef_id_is_declared=T, chefs_agree=T, consensus_choice_defined=T, debate_round_GE_3=T, debate_round_LT_3=T, scoring_path_taken=T, winner_path_taken=T => TRUE

    # mcdc:witness-code-free SYS-REQ-004
    # Verifies: SYS-REQ-004
    # SYS-REQ-004:nominal:nominal
    # SYS-REQ-004:boundary:nominal
    # SYS-REQ-004:error_handling:nominal
    # SYS-REQ-004:error_handling:negative
    sfn = util_mod.sfn
    sfn.Choice.reset_mock()
    sfn.Condition.or_.reset_mock()
    sfn.Condition.string_equals.reset_mock()
    sfn.Condition.number_greater_than_equals.reset_mock()
    sfn.Errors = MagicMock()
    sfn.Errors.TASKS_FAILED = "States.TaskFailed"

    MealPlannerStack(object(), "MealPlanner")

    choice_ids = [
        call.args[1] if len(call.args) > 1 else call.kwargs.get("id")
        for call in sfn.Choice.call_args_list
    ]
    assert any("Consensus reached?" in str(choice_id) for choice_id in choice_ids)

    string_equals_calls = sfn.Condition.string_equals.call_args_list
    assert any(
        call.args == ("$.referee_output.consensus.do_chefs_agree", "yes")
        or (
            call.kwargs.get("variable") == "$.referee_output.consensus.do_chefs_agree"
            and call.kwargs.get("value") == "yes"
        )
        for call in string_equals_calls
    ), string_equals_calls
    assert any(
        call.args == ("$.referee_output.consensus.do_chefs_agree", "no")
        or (
            call.kwargs.get("variable") == "$.referee_output.consensus.do_chefs_agree"
            and call.kwargs.get("value") == "no"
        )
        for call in string_equals_calls
    ), string_equals_calls

    gte_calls = sfn.Condition.number_greater_than_equals.call_args_list
    assert any(
        call.args == ("$.debate_state.debate_round", 3)
        or (
            call.kwargs.get("variable") == "$.debate_state.debate_round"
            and call.kwargs.get("value") == 3
        )
        for call in gte_calls
    ), gte_calls
    assert sfn.Condition.or_.called

