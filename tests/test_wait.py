import unittest

import pytest

from src.oadp_utils.wait import wait_for, ExitConditionFoundError

logger = print


def f_condition_met(**kwargs):
    logger(kwargs)
    return True


def f_exit_condition_found(**kwargs):
    logger(kwargs)
    return False, True


def f_time_out(**kwargs):
    logger(kwargs)
    return False, False


class TestWait(unittest.TestCase):

    def test_wait_condition_found(self):
        assert wait_for(condition_function=f_condition_met,
                        description="Some Condition.",
                        wait_timeout=10, sleep=1, x=1, y=2)

    def test_wait_timeout(self):

        try:
            wait_for(condition_function=f_condition_met,
                     description="Some Condition.and expect it to Timeout",
                     wait_timeout=10, sleep=1, x=1, y=2)
        except TimeoutError:
            pass
        pytest.xfail("TimeoutError was not raised.")

    def test_wait_exit_condition_found(self):
        try:
            wait_for(condition_function=f_exit_condition_found,
                     description="Exit Condition and expect ExitConditionFoundError",
                     wait_timeout=200, sleep=5, x=1, y=2)

        except ExitConditionFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
