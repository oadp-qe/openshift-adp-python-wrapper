import logging
import time
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger(__name__)


def wait_for(condition_function, description="Something", wait_timeout=200, sleep=5, **func_kwargs):
    """
    Providing a way to wait for any function to return true.

    Example: wait_for(condition_function=dpa.reconciled, description="Wait For Data Protection Application
    Resource.", timeout=200, sleep=5):

    :param condition_function: to sample.
    :param description:  describe what we are waiting for.
    :param wait_timeout: before throwing timeoutExpiredError.
    :param sleep: between samples.
    :return:
    """
    logger.info(f"Waiting For {description}, any status information should be logged by your condition_function! ")
    timeout = datetime.now() + timedelta(seconds=wait_timeout)
    while datetime.now() < timeout and not condition_function(**func_kwargs):
        time.sleep(sleep)

    if not condition_function(**func_kwargs):
        logger.info(f"Waiting For {description}-TIMEOUT")
        raise TimeoutError
    logger.info(f"Waiting For {description}-OK")
    return True
