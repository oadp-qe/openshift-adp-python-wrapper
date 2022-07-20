import logging
import os

logger = logging.getLogger(__name__)


def run_shell_cmd(cmd):
    logger.info(f"shell: {cmd}")
    err = os.system(cmd)
    if err != 0:
        logger.error("Shell Command return none zero.")
    return err
