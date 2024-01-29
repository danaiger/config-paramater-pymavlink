import pytest
from config_parameter import (
    wait_for_heartbeat,
    _assert_not_exceeding_timeout_limit,
    _is_received_message_is_the_relevant_ack,
    _get_next_message_of_type_parameter_value,
    _wait_for_ack_that_parameter_has_been_configured_successfuly,
)
from unittest.mock import Mock
from pymavlink import mavutil
from pymavlink.dialects.v20.ardupilotmega import MAVLink_param_value_message
import time

GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE = MAVLink_param_value_message(**{
    "param_id": b"GPS_AUTO_SWITCH",
    "param_value": 4.0,
    "param_type": 2,
    "param_count": 1386,
    "param_index": 65535,
})


@pytest.fixture
def connection():
    return mavutil.mavlink_connection("udpin:0.0.0.0:14550")


def test_wait_for_heartbeat_raises_timeout_error(connection):
    connection.wait_heartbeat = Mock(return_value=None)
    with pytest.raises(TimeoutError):
        wait_for_heartbeat(connection, timeout_seconds=3)


def test_assert_not_exceeding_timeout_limit_raises_when_exceeding_limit():
    with pytest.raises(TimeoutError):
        _assert_not_exceeding_timeout_limit(time_now=time.time() - 4, timeout_seconds=3)


def test_is_received_message_is_the_relevant_ack_returns_true_for_correct_ack():
    assert _is_received_message_is_the_relevant_ack(
        GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE.to_dict(), "GPS_AUTO_SWITCH", 4
    )


def test_is_received_message_is_the_relevant_ack_returns_false_for_incorrect_value_ack():
    assert not _is_received_message_is_the_relevant_ack(
        GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE.to_dict(), "GPS_AUTO_SWITCH", 3
    )


def test_is_received_message_is_the_relevant_ack_returns_false_for_incorrect_param_ack():
    assert not _is_received_message_is_the_relevant_ack(
        GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE.to_dict(), "GPS_AUTO_CONFIG", 1
    )


def test_get_next_message_of_type_parameter_value_returns_correct_message(connection):
    connection.recv_match = Mock(return_value=GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE)
    assert (
        _get_next_message_of_type_parameter_value(connection, 3)
        == GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE
    )


def test_get_next_message_of_type_parameter_value_raises_when_no_message_is_received(
    connection,
):
    connection.recv_match = Mock(return_value=None)
    with pytest.raises(TimeoutError):
        _get_next_message_of_type_parameter_value(connection, 3)


def test_wait_for_ack_that_parameter_has_been_configured_successfuly_returns_correct_parsed_message(
    connection,
):
    connection.recv_match = Mock(return_value=GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE)
    assert (
        _wait_for_ack_that_parameter_has_been_configured_successfuly(
            "GPS_AUTO_SWITCH", 4, connection, 3
        )
        == GPS_AUTO_SWITCH_EXPECTED_MESSAGE_EXAMPLE.to_dict()
    )
