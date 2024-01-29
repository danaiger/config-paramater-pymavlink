import time
from pymavlink.mavutil import mavfile
from utils import assert_not_exceeding_timeout_limit

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


def wait_for_ack_that_parameter_has_been_configured_successfuly(
    parameter_name: str,
    expected_parameter_value: int,
    sock: mavfile,
    timeout_seconds: int,
) -> dict:
    now = time.time()
    while True:
        assert_not_exceeding_timeout_limit(now, timeout_seconds)
        message = _get_next_message_of_type_parameter_value(sock, timeout_seconds)
        parsed_message = message.to_dict()
        if _is_received_message_is_the_relevant_ack(
            parsed_message, parameter_name, expected_parameter_value
        ):
            return parsed_message

