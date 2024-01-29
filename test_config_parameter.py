import pytest
from config_parameter import (
    wait_for_heartbeat,
    _assert_not_exceeding_timeout_limit,
    _is_received_message_is_the_relevant_ack,
)
from unittest.mock import Mock
from pymavlink import mavutil
import time

GPS_AUTO_SWITCH_MESSAGE_EXAMPLE = {
    "mavpackettype": "PARAM_VALUE",
    "param_id": "GPS_AUTO_SWITCH",
    "param_value": 4.0,
    "param_type": 2,
    "param_count": 1386,
    "param_index": 65535,
}


@pytest.fixture
def connection():
    return mavutil.mavlink_connection("udpin:0.0.0.0:14550")


def test_heartbeat_raises_timeout_error(connection):
    connection.wait_heartbeat = Mock(return_value=None)
    with pytest.raises(TimeoutError):
        wait_for_heartbeat(connection, timeout_seconds=3)


def test_assert_exceeding_timeout_limits_raises():
    with pytest.raises(TimeoutError):
        _assert_not_exceeding_timeout_limit(time_now=time.time() - 4, timeout_seconds=3)


def test_is_received_message_is_the_relevant_ack_returns_true_for_correct_ack():
    assert _is_received_message_is_the_relevant_ack(
        GPS_AUTO_SWITCH_MESSAGE_EXAMPLE, "GPS_AUTO_SWITCH", 4
    )


def test_is_received_message_is_the_relevant_ack_returns_false_for_incorrect_value_ack():
    assert not _is_received_message_is_the_relevant_ack(
        GPS_AUTO_SWITCH_MESSAGE_EXAMPLE, "GPS_AUTO_SWITCH", 3
    )

def test_is_received_message_is_the_relevant_ack_returns_false_for_incorrect_param_ack():
    assert not _is_received_message_is_the_relevant_ack(
        GPS_AUTO_SWITCH_MESSAGE_EXAMPLE, "GPS_AUTO_CONFIG", 1
    )