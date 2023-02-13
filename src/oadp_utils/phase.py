import logging
logger = logging.getLogger(__name__)


def check_phase(resource, expected_phase):
    try:
        current_phase = resource.instance.status.phase
        logger.info(f"Current phase status is: {current_phase}")
        return current_phase == expected_phase
    except AttributeError:
        return False


def log_status(resource):
    logger.info(f"The status of {resource.kind}/{resource.name} is:")
    logger.info(f"\n{resource.instance.status}\n")
