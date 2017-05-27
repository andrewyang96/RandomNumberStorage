from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    """Primary Lambda handler."""
    random_num = random.randint(-2 ** 31, 2 ** 31 + 1)
    current_dt = datetime.now()
    logger.info(
        '{0}: Inserted random number {1}'.format(current_dt, random_num))
