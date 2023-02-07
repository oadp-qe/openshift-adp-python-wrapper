import logging
import unittest

from src.oadp_utils.wait import wait_for

logger = print


def func1(**kwargs):
    logger(kwargs)
    return True


class TestWait(unittest.TestCase):

    def test_wait(self):
        result = wait_for(condition_function=func1, description="חכה לי פינוקיו", wait_timeout=200, sleep=5, x=1, y=2)

        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
