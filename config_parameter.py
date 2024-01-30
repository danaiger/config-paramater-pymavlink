from pymavlink import mavutil
from pymavlink.mavutil import mavfile
from mavlink_message_filter import wait_for_ack_that_parameter_has_been_configured_successfuly
from parameter_models import GPS_Auto_Switch

TIMEOUT_SECOND = 3

def set_a_parameter_at_on_board_computer(
    parameter_name: str, parameter_value: int, sock: mavfile, timeout_seconds: int
):
    sock.mav.param_set_send(
        sock.target_system,
        sock.target_component,
        bytes(parameter_name, "utf-8"),
        parameter_value,
        mavutil.mavlink.MAV_PARAM_TYPE_INT8,
    )
    print(
        f"request sent to configure param name: {parameter_name} with value: {parameter_value}. waiting for acknowledgement"
    )
    ack_message = wait_for_ack_that_parameter_has_been_configured_successfuly(
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
