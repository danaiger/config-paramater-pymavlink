import time


def assert_not_exceeding_timeout_limit(time_now: int, timeout_seconds: int):
    if time.time() > time_now + timeout_seconds:
        raise TimeoutError("something went wrong, please try again")
