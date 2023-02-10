import logging
import time
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger(__name__)


class ExitConditionFoundError(Exception):
    pass


def wait_for(condition_function, description="Something", wait_timeout=200, sleep=5, **func_kwargs):
    """
    Providing a way to wait for any function to return true.
    If the function should return a tuple,
    the second item is considered a break criteria and ExitConditionFoundError is raised.

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
    condition_met = False
    exit_condition_found = False
    while datetime.now() < timeout and not condition_met \
            and not exit_condition_found:
        conditions = condition_function(**func_kwargs)
        if type(conditions) == tuple:
            condition_met = conditions[0]
            exit_condition_found = conditions[1]
        else:
            condition_met = conditions
        time.sleep(sleep)

    if exit_condition_found:
        logger.warning("Waiting For {description}-BRAKE")
        raise ExitConditionFoundError

    if condition_met:
        logger.info(f"Waiting For {description}-OK")

    return condition_met

