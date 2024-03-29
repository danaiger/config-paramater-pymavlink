import pytest
from config_parameter import (
    wait_for_heartbeat,
    TIMEOUT_SECOND,
)
from utils import (
    assert_not_exceeding_timeout_limit,
)
from mavlink_message_filter import (
    _is_received_message_is_the_relevant_ack,
    _get_next_message_of_type_parameter_value,
    wait_for_ack_that_parameter_has_been_configured_successfuly,
)
from unittest.mock import Mock
import time


def test_wait_for_heartbeat_raises_timeout_error(connection):
    connection.wait_heartbeat = Mock(return_value=None)
    with pytest.raises(TimeoutError):
        wait_for_heartbeat(connection, timeout_seconds=3)


def test_wait_for_heartbeat_not_raises(connection, heartbeat_message_example):
    connection.wait_heartbeat = Mock(return_value=heartbeat_message_example)
    wait_for_heartbeat(connection, timeout_seconds=3)


def test_assert_not_exceeding_timeout_limit_raises_when_exceeding_limit():
    with pytest.raises(TimeoutError):
        assert_not_exceeding_timeout_limit(time_now=time.time() - 4, timeout_seconds=3)


def test_is_received_message_is_the_relevant_ack_returns_true_for_correct_ack(
    gps_auto_switch_mavlink_message_example,
):
    assert _is_received_message_is_the_relevant_ack(
        gps_auto_switch_mavlink_message_example, "GPS_AUTO_SWITCH", 4
    )


def test_is_received_message_is_the_relevant_ack_returns_false_for_incorrect_value_ack(
    gps_auto_switch_mavlink_message_example,
):
    assert not _is_received_message_is_the_relevant_ack(
        gps_auto_switch_mavlink_message_example, "GPS_AUTO_SWITCH", 3
    )


def test_is_received_message_is_the_relevant_ack_returns_false_for_incorrect_param_ack(
    gps_auto_switch_mavlink_message_example,
):
    assert not _is_received_message_is_the_relevant_ack(
        gps_auto_switch_mavlink_message_example, "GPS_AUTO_CONFIG", 1
    )


def test_get_next_message_of_type_parameter_value_returns_correct_message(
    connection, gps_auto_switch_mavlink_message_example
):
    connection.recv_match = Mock(return_value=gps_auto_switch_mavlink_message_example)
    assert (
        _get_next_message_of_type_parameter_value(connection, 3)
        == gps_auto_switch_mavlink_message_example
    )


def test_get_next_message_of_type_parameter_value_raises_when_no_message_is_received(
    connection,
):
    connection.recv_match = Mock(return_value=None)
    with pytest.raises(TimeoutError):
        _get_next_message_of_type_parameter_value(connection, 3)


def test_wait_for_ack_that_parameter_has_been_configured_successfuly_returns_correct_parsed_message(
    connection, gps_auto_switch_mavlink_message_example
):
    connection.recv_match = Mock(return_value=gps_auto_switch_mavlink_message_example)
    assert (
        wait_for_ack_that_parameter_has_been_configured_successfuly(
            parameter_name="GPS_AUTO_SWITCH",
            expected_parameter_value=4,
            sock=connection,
            timeout_seconds=3,
        )
        == gps_auto_switch_mavlink_message_example.to_dict()
    )


def test_wait_for_ack_that_parameter_has_been_configured_successfuly_after_receiving_the_wrong_message_at_first(
    connection,
    gps_auto_switch_mavlink_message_example,
    loit_speed_mavlink_message_example,
):
    connection.recv_match = Mock(
        side_effect=(
            loit_speed_mavlink_message_example,
            gps_auto_switch_mavlink_message_example,
        )
    )
    assert (
        wait_for_ack_that_parameter_has_been_configured_successfuly(
            parameter_name="GPS_AUTO_SWITCH",
            expected_parameter_value=4,
            sock=connection,
            timeout_seconds=3,
        )
        == gps_auto_switch_mavlink_message_example.to_dict()
    )


def test_wait_for_ack_that_parameter_has_been_configured_successfuly_raises_if_time_is_too_big(
    connection,
):
    now = time.time()
    time.time = Mock(side_effect=(now, now + TIMEOUT_SECOND + 1))
    with pytest.raises(TimeoutError):
        wait_for_ack_that_parameter_has_been_configured_successfuly(
            parameter_name="GPS_AUTO_SWITCH",
            expected_parameter_value=4,
            sock=connection,
            timeout_seconds=3,
        )
