import pytest
from pymavlink import mavutil
from pymavlink.dialects.v10.ardupilotmega import (
    MAVLink_param_value_message,
    MAVLink_heartbeat_message,
)


@pytest.fixture
def heartbeat_message_example():
    return MAVLink_heartbeat_message(
        type=2,
        autopilot=3,
        base_mode=81,
        custom_mode=0,
        system_status=3,
        mavlink_version=3,
    )


@pytest.fixture
def loit_speed_mavlink_message_example():
    return MAVLink_param_value_message(
        param_id=b"LOIT_SPEED",
        param_value=300.0,
        param_type=9,
        param_count=1386,
        param_index=65535,
    )


@pytest.fixture
def gps_auto_switch_mavlink_message_example():
    return MAVLink_param_value_message(
        param_id=b"GPS_AUTO_SWITCH",
        param_value=4.0,
        param_type=2,
        param_count=1386,
        param_index=65535,
    )


@pytest.fixture
def connection():
    return mavutil.mavlink_connection("udpin:0.0.0.0:14550")

