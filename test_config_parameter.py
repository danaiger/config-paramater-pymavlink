import pytest
from config_parameter import wait_for_heartbeat, _assert_not_exceeding_timeout_limit
from unittest.mock import Mock
from pymavlink import mavutil
import time


@pytest.fixture
def connection():
    return mavutil.mavlink_connection("udpin:0.0.0.0:14550")


def test_heartbeat_raises_timeout_error(connection):
    connection.wait_heartbeat = Mock(return_value=None)
    with pytest.raises(TimeoutError):
        wait_for_heartbeat(connection, timeout_seconds=3)


def test_assert_exceeding_timeout_limits_raises():
    with pytest.raises(TimeoutError):
        _assert_not_exceeding_timeout_limit(time_now=time.time()-4,timeout_seconds=3)
