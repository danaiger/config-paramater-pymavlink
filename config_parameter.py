import time
from pymavlink import mavutil
from pymavlink.mavutil import mavfile
from enum import Enum


class GPS_Auto_Switch(Enum):
    USE_PRIMARY = 0
    USE_BEST = 1
    BLEND = 2
    USE_PRIMARY_IF_3D_FIX_OR_BETTER = 4


def _assert_not_exceeding_timeout_limit(time_now: int, timeout_seconds: int):
    if time.time() > time_now + timeout_seconds:
        raise TimeoutError("something went wrong, please try again")


def _is_received_message_is_the_relevant_ack(
    parsed_message: dict, parameter_name: str, expected_parameter_value: int
) -> bool:
    return (
        parsed_message.get("param_id") == parameter_name
        and parsed_message.get("param_value") == expected_parameter_value
    )


def _get_next_message_of_type_parameter_value(sock, timeout_seconds):
    message = sock.recv_match(
        type="PARAM_VALUE", blocking=True, timeout=timeout_seconds
    )
    if not message:
        raise TimeoutError("something went wrong, please try again")
    return message


def _wait_for_ack_that_parameter_has_been_configured_successfuly(
    parameter_name: str,
    expected_parameter_value: int,
    sock: mavfile,
    timeout_seconds: int,
) -> dict:
    now = time.time()
    while True:
        _assert_not_exceeding_timeout_limit(now, timeout_seconds)
        message = _get_next_message_of_type_parameter_value(sock, timeout_seconds)
        print(type(message))
        parsed_message = message.to_dict()
        if _is_received_message_is_the_relevant_ack(
            parsed_message, parameter_name, expected_parameter_value
        ):
            return parsed_message


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
    ack_message = _wait_for_ack_that_parameter_has_been_configured_successfuly(
        parameter_name, parameter_value, sock, timeout_seconds
    )

    print(
        f'parameter name: {ack_message["param_id"]} was set successfuly with value: {ack_message["param_value"]}'
    )


def wait_for_heartbeat(sock: mavfile, timeout_seconds: int):
    heartbeat = sock.wait_heartbeat(timeout=timeout_seconds)
    if not heartbeat:
        raise TimeoutError("cannot get heartbeat, please check the connection")


def main():
    TIMEOUT_SECOND = 3
    PARAMETER_NAME = "GPS_AUTO_SWITCH"
    connection: mavfile = mavutil.mavlink_connection("udpin:0.0.0.0:14550")
    wait_for_heartbeat(connection, TIMEOUT_SECOND)
    set_a_parameter_at_on_board_computer(
        PARAMETER_NAME,
        GPS_Auto_Switch.USE_PRIMARY_IF_3D_FIX_OR_BETTER.value,
        connection,
        TIMEOUT_SECOND,
    )


if __name__ == "__main__":
    main()
