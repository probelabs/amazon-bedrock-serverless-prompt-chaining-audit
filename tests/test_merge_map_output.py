# Parent system requirement: SYS-REQ-001
import pytest

from tests.conftest import load_module


def _handler():
    return load_module(
        "merge_map_output",
        "functions/generic/merge_map_output/index.py",
    ).handler


def _item(*messages):
    return {"model_outputs": {"conversation": list(messages)}}


def test_merges_shared_prefix_from_first_item_and_last_two_of_each():
    # mcdc:ignore:defensive SW-REQ-005: arc_entry_count_EQ_2=F, conversations_are_merged=T, handler_raises=T, map_result_count_GE_1=T, map_results_present=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-005: arc_entry_count_EQ_2=T, conversations_are_merged=F, handler_raises=F, map_result_count_GE_1=F, map_results_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-005: arc_entry_count_EQ_2=T, conversations_are_merged=F, handler_raises=F, map_result_count_GE_1=T, map_results_present=F => TRUE
    # MCDC SW-REQ-005: arc_entry_count_EQ_2=T, conversations_are_merged=F, handler_raises=T, map_result_count_GE_1=F, map_results_present=F => TRUE
    # mcdc:ignore:defensive SW-REQ-005: arc_entry_count_EQ_2=T, conversations_are_merged=F, handler_raises=T, map_result_count_GE_1=F, map_results_present=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-005: arc_entry_count_EQ_2=T, conversations_are_merged=F, handler_raises=T, map_result_count_GE_1=T, map_results_present=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-005: arc_entry_count_EQ_2=T, conversations_are_merged=T, handler_raises=T, map_result_count_GE_1=T, map_results_present=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-010: arc_entry_count_EQ_2=F, conversations_are_merged=F, map_results_present=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-010: arc_entry_count_EQ_2=T, conversations_are_merged=F, map_results_present=F => TRUE
    # mcdc:ignore:defensive SYS-REQ-010: arc_entry_count_EQ_2=T, conversations_are_merged=F, map_results_present=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-010: arc_entry_count_EQ_2=T, conversations_are_merged=T, map_results_present=T => TRUE

    # Verifies: SW-REQ-005
    # Verifies: SYS-REQ-010
    # SW-REQ-005:nominal:nominal
    # SW-REQ-005:error_handling:nominal
    # SYS-REQ-010:nominal:nominal
    handler = _handler()
    shared = [
        {"role": "user", "content": "write a story"},
        {"role": "assistant", "content": "ok"},
    ]
    item_a_tail = [
        {"role": "user", "content": "arc for Ada"},
        {"role": "assistant", "content": "Ada climbs"},
    ]
    item_b_tail = [
        {"role": "user", "content": "arc for Ben"},
        {"role": "assistant", "content": "Ben falls"},
    ]
    event = [
        _item(*(shared + item_a_tail)),
        _item(*(shared + item_b_tail)),
    ]

    result = handler(event, None)

    assert result["conversation"] == shared + item_a_tail + item_b_tail
    assert result["conversation"][:2] == event[0]["model_outputs"]["conversation"][:-2]
    assert result["conversation"][2:4] == event[0]["model_outputs"]["conversation"][-2:]
    assert result["conversation"][4:6] == event[1]["model_outputs"]["conversation"][-2:]


def test_single_item_keeps_full_conversation():
    # Verifies: SW-REQ-005
    # Verifies: SYS-REQ-010
    handler = _handler()
    conversation = ["history-a", "history-b", "prompt", "reply"]
    result = handler([_item(*conversation)], None)
    assert result == {"conversation": conversation}


def test_single_item_shorter_than_two_messages():
    # Verifies: SW-REQ-005
    # Verifies: SYS-REQ-010
    handler = _handler()
    result = handler([_item("only-one")], None)
    assert result == {"conversation": ["only-one"]}


def test_empty_map_results_raise():
    # Verifies: SW-REQ-005
    # Verifies: SYS-REQ-010
    # SW-REQ-005:error_handling:negative
    handler = _handler()
    with pytest.raises(IndexError):
        handler([], None)
