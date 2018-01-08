from datetime import datetime
import logging
import psycopg2
import os
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DB_NAME = 'random_numbers'

# Lambda environment variables
HOST_URL = os.environ.get('HOST_URL')
TABLE_NAME = os.environ.get('TABLE_NAME')
USERNAME = os.environ.get('USERNAME')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')

def get_db_connection():
    """Get psycopg2 connection to RDS instance."""
    return psycopg2.connect(dbname=DB_NAME, user=USERNAME, host=HOST_URL)

def run(event, context):
    """Primary Lambda handler."""
    conn = get_db_connection()
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
    if EMAIL_ADDRESS:
        # TODO: send email
        logger.info('Sent email to {0}'.format(EMAIL_ADDRESS))
