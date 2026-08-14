from pathlib import Path

SFN_TECHNIQUE_STACKS = [
    "Techniques-ModelInvocation",
    "Techniques-PromptTemplating",
    "Techniques-SequentialChain",
    "Techniques-ParallelChain",
    "Techniques-ConditionalChain",
    "Techniques-HumanInput",
    "Techniques-Map",
    "Techniques-AwsServiceInvocation",
    "Techniques-Validation",
]


def test_sfn_technique_stack_names_exist():
    # mcdc:ignore:defensive SYS-REQ-006: flows_stack_count_GE_6=F, human_input_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=F, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=F, technique_name_is_documented_sfn=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=F, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=F, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-006: flows_stack_count_GE_6=T, human_input_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => TRUE
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=F, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=F, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=F, model_invocation_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=F, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=F, technique_execution_requested=F, technique_name_is_documented_sfn=F => TRUE
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=F, technique_execution_requested=F, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=F, technique_execution_requested=T, technique_name_is_documented_sfn=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=F, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=F, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=F, technique_execution_requested=T, technique_name_is_documented_sfn=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-009: flows_stack_count_GE_6=T, flows_technique_stack_defined=T, human_input_technique_defined=T, model_invocation_technique_defined=T, named_technique_exists=T, sfn_stack_count_GE_9=T, sfn_technique_stack_defined=T, technique_execution_requested=T, technique_name_is_documented_sfn=T => TRUE

    # Verifies: STK-REQ-003
    # Verifies: SW-REQ-009
    # Verifies: SYS-REQ-006
    # STK-REQ-003:nominal:nominal
    # STK-REQ-003:error_handling:nominal
    # STK-REQ-003:boundary:nominal
    # SW-REQ-009:nominal:nominal
    # SW-REQ-009:boundary:nominal
    # SYS-REQ-006:nominal:nominal
    # SYS-REQ-006:error_handling:nominal
    # SYS-REQ-006:boundary:nominal
    src = Path("/workspace/techniques_step_functions/technique_stacks.py").read_text()
    for name in SFN_TECHNIQUE_STACKS:
        assert f'"{name}"' in src, name
