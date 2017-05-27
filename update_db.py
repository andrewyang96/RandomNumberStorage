from datetime import datetime
import logging
import psycopg2
import os
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DB_NAME = 'random_numbers'
HOST_URL = os.environ['HOST_URL']  # to be set in Lambda
TABLE_NAME = os.environ['TABLE_NAME']  # to be set in Lambda
USERNAME = os.environ['USERNAME']  # to be set in Lambda


def get_connection():
    """Get psycopg2 connection to RDS instance."""
    return psycopg2.connect(dbname=DB_NAME, user=USERNAME, host=HOST_URL)


def run(event, context):
    """Primary Lambda handler."""
    conn = get_connection()
    cur = conn.cursor()
    random_num = random.randint(-2 ** 31, 2 ** 31 + 1)
    current_dt = datetime.utcnow()
    cur.execute(
        'INSERT INTO %s (timestamp, random_num) VALUES (%s, %s)',
        (TABLE_NAME, current_dt, random_num))
    conn.commit()
    conn.close()
    logger.info(
        '{0}: Inserted random number {1}'.format(current_dt, random_num))
