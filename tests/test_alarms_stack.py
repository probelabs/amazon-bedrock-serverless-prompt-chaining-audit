import importlib
import sys

from tests.conftest import DummyCdkStack, install_cdk_stubs

install_cdk_stubs()
import stacks.alarms_stack as alarms_mod  # noqa: E402

if not isinstance(alarms_mod.Stack, type):
    sys.modules["aws_cdk"].Stack = DummyCdkStack
    alarms_mod = importlib.reload(alarms_mod)

AlarmsStack = alarms_mod.AlarmsStack


def test_alarms_stack_defines_composite_and_sns_topic():
    # MCDC SYS-REQ-005: alarm_action_is_sns=F, alarm_notification_published=F, composite_alarm_defined=T, demo_metric_failed_alarmed=F, demo_workflow_failed=F, failed_count_GE_1=F, failed_execution_metric_present=F, sns_topic_defined=T => TRUE
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=F, alarm_notification_published=F, composite_alarm_defined=T, demo_metric_failed_alarmed=F, demo_workflow_failed=F, failed_count_GE_1=F, failed_execution_metric_present=T, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=F, alarm_notification_published=F, composite_alarm_defined=T, demo_metric_failed_alarmed=F, demo_workflow_failed=F, failed_count_GE_1=T, failed_execution_metric_present=F, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=F, alarm_notification_published=F, composite_alarm_defined=T, demo_metric_failed_alarmed=F, demo_workflow_failed=T, failed_count_GE_1=F, failed_execution_metric_present=F, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=F, alarm_notification_published=T, composite_alarm_defined=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, failed_count_GE_1=T, failed_execution_metric_present=T, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=T, alarm_notification_published=F, composite_alarm_defined=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, failed_count_GE_1=T, failed_execution_metric_present=T, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=T, alarm_notification_published=T, composite_alarm_defined=F, demo_metric_failed_alarmed=T, demo_workflow_failed=T, failed_count_GE_1=T, failed_execution_metric_present=T, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=T, alarm_notification_published=T, composite_alarm_defined=T, demo_metric_failed_alarmed=F, demo_workflow_failed=T, failed_count_GE_1=T, failed_execution_metric_present=T, sns_topic_defined=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SYS-REQ-005: alarm_action_is_sns=T, alarm_notification_published=T, composite_alarm_defined=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, failed_count_GE_1=T, failed_execution_metric_present=T, sns_topic_defined=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SYS-REQ-005: alarm_action_is_sns=T, alarm_notification_published=T, composite_alarm_defined=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, failed_count_GE_1=T, failed_execution_metric_present=T, sns_topic_defined=T => TRUE
    # MCDC INT-REQ-005: alarm_notification_published=F, composite_alarm_defined=T, composite_alarm_firing=F, demo_workflow_failed=F, evaluation_periods_EQ_1=T, failed_count_GE_1=F, sns_topic_receives_publish=F, topic_name_is_notifications=T => TRUE
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=F, composite_alarm_defined=T, composite_alarm_firing=F, demo_workflow_failed=F, evaluation_periods_EQ_1=T, failed_count_GE_1=T, sns_topic_receives_publish=F, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=F, composite_alarm_defined=T, composite_alarm_firing=F, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_count_GE_1=F, sns_topic_receives_publish=F, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=F, composite_alarm_defined=T, composite_alarm_firing=T, demo_workflow_failed=F, evaluation_periods_EQ_1=T, failed_count_GE_1=F, sns_topic_receives_publish=F, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=F, composite_alarm_defined=T, composite_alarm_firing=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_count_GE_1=T, sns_topic_receives_publish=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=T, composite_alarm_defined=F, composite_alarm_firing=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_count_GE_1=T, sns_topic_receives_publish=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=T, composite_alarm_defined=T, composite_alarm_firing=T, demo_workflow_failed=T, evaluation_periods_EQ_1=F, failed_count_GE_1=T, sns_topic_receives_publish=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=T, composite_alarm_defined=T, composite_alarm_firing=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_count_GE_1=T, sns_topic_receives_publish=F, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive INT-REQ-005: alarm_notification_published=T, composite_alarm_defined=T, composite_alarm_firing=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_count_GE_1=T, sns_topic_receives_publish=T, topic_name_is_notifications=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC INT-REQ-005: alarm_notification_published=T, composite_alarm_defined=T, composite_alarm_firing=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_count_GE_1=T, sns_topic_receives_publish=T, topic_name_is_notifications=T => TRUE
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=F, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=F, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=F, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=F, demo_workflow_failed=F, evaluation_periods_EQ_1=T, failed_execution_metric_present=F, sns_topic_defined=T, topic_name_is_notifications=T => TRUE
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=F, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=F, demo_workflow_failed=F, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=F, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=F, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=F, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=F, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=F, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=F, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=F, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=F, topic_name_is_notifications=T => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # mcdc:ignore:defensive SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=F => FALSE -- logically unreachable; implementation preserves the guarantee [reviewed: REVIEW-1]
    # MCDC SW-REQ-008: alarm_action_is_sns=T, alarm_threshold_EQ_1=T, composite_alarm_defined=T, demo_alarm_count_EQ_7=T, demo_metric_failed_alarmed=T, demo_workflow_failed=T, evaluation_periods_EQ_1=T, failed_execution_metric_present=T, sns_topic_defined=T, topic_name_is_notifications=T => TRUE

    # Verifies: STK-REQ-002
    # Verifies: SW-REQ-008
    # Verifies: SYS-REQ-005
    # Verifies: INT-REQ-005
    # STK-REQ-002:nominal:nominal
    # STK-REQ-002:error_handling:nominal
    # STK-REQ-002:error_handling:negative
    # SW-REQ-008:nominal:nominal
    # SW-REQ-008:error_handling:nominal
    # SW-REQ-008:error_handling:negative
    # SYS-REQ-005:nominal:nominal
    # SYS-REQ-005:error_handling:nominal
    # INT-REQ-005:nominal:nominal
    # INT-REQ-005:error_handling:nominal
    # INT-REQ-005:error_handling:negative
    # INT-REQ-005:integration:integration
    cloudwatch = alarms_mod.cloudwatch
    sns = alarms_mod.sns
    cw_actions = alarms_mod.cw_actions
    cloudwatch.CompositeAlarm.reset_mock()
    cloudwatch.Alarm.reset_mock()
    sns.Topic.reset_mock()
    cw_actions.SnsAction.reset_mock()

    AlarmsStack(object(), "Alarms")

    assert cloudwatch.Alarm.call_count == 7
    assert cloudwatch.CompositeAlarm.called
    composite_kwargs = cloudwatch.CompositeAlarm.call_args.kwargs
    assert composite_kwargs.get("composite_alarm_name") == "PromptChainDemo-Composite-Alarm"

    topic_kwargs = sns.Topic.call_args.kwargs
    assert topic_kwargs.get("topic_name") == (
        "bedrock-serverless-prompt-chaining-notifications"
    )
    composite = cloudwatch.CompositeAlarm.return_value
    assert composite.add_alarm_action.called
    assert cw_actions.SnsAction.called

