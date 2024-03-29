import logging
logger = logging.getLogger(__name__)


def check_phase(resource, expected_phase):
    try:
        current_phase = resource.instance.status.phase
        logger.info(f"Current phase status of the resource {resource.kind}/{resource.name} is: {current_phase}")
        return current_phase == expected_phase
    except AttributeError:
        return False


def log_status(resource):
    logger.info(f"The status of {resource.kind}/{resource.name} is:"
                f"\n{resource.instance.status}\n")

