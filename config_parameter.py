import time
from pymavlink import mavutil
from pymavlink.mavutil import mavfile
from enum import Enum


class GPS_AUTO_SWITCH(Enum):
    USE_PRIMARY = 0
    USE_BEST = 1
    BLEND = 2
    USE_PRIMARY_IF_3D_FIX_OR_BETTER = 4


def wait_for_ack_that_parameter_has_been_configured_successfuly(
    parameter_name: str,
    expected_parameter_value: int,
    sock: mavfile,
    timeout_seconds: int,
):
    now = time.time()
    while True:
        if time.time() > now + timeout_seconds:
            raise TimeoutError("something went wrong, please try again")
        message = sock.recv_match(
            type="PARAM_VALUE", blocking=True, timeout=timeout_seconds
        )
        if not message:
            raise TimeoutError("something went wrong, please try again")
        parsed_message = message.to_dict()
        if (
            parsed_message.get("param_id") != parameter_name
            or parsed_message.get("param_value") != expected_parameter_value
        ):
            continue
        break

    print(
        f'parameter name: {parsed_message["param_id"]} was set successfuly with value: {parsed_message["param_value"]}'
    )


def set_a_parameter_at_on_board_computer(
    parameter_name: str, parameter_value: int, sock: mavfile, timeout_seconds: int
):
    sock.mav.param_set_send(
        sock.target_system,
        sock.target_component,
        bytes(parameter_name, "utf-8"),
        parameter_value,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32,
    )
    print(
        f"request sent to configure param name: {parameter_name} with value: {parameter_value}. waiting for acknowledgement"
    )
    wait_for_ack_that_parameter_has_been_configured_successfuly(
        parameter_name, parameter_value, sock, timeout_seconds
    )


def main():
    TIMEOUT_SECOND = 3
    PARAMETER_NAME = "GPS_AUTO_SWITCH"
    connection: mavfile = mavutil.mavlink_connection("udpin:0.0.0.0:14550")
    heartbeat = connection.wait_heartbeat(timeout=TIMEOUT_SECOND)
    if not heartbeat:
        raise TimeoutError("cannot get heartbeat, please check the connection")
    set_a_parameter_at_on_board_computer(
        PARAMETER_NAME,
        GPS_AUTO_SWITCH.USE_PRIMARY_IF_3D_FIX_OR_BETTER.value,
        connection,
        TIMEOUT_SECOND,
    )


if __name__ == "__main__":
    main()
