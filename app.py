from datetime import datetime
from flask import Flask
import json
import psycopg2
import logging
import random

with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_db_connection():
    """Get psycopg2 connection to RDS instance."""
    db_config = config['database']
    logger.info('Connecting to database at {0}'.format(db_config['host_url']))
    return psycopg2.connect(
        host=db_config['host_url'],
        dbname=db_config['db_name'],
        user=db_config['username'],
        password=db_config['password'])

@app.route('/', methods=['GET'])
def main_handler(event=None, context=None):
    logger.info('Handler called!')
    conn = get_db_connection()
    cur = conn.cursor()

    random_num = random.randint(0, config['max_number'])
    current_dt = datetime.utcnow()

    cur.execute(
        'INSERT INTO history (timestamp, random_num) VALUES (%s, %s)',
        (current_dt, random_num))
    conn.commit()
    cur.close()
    conn.close()

    logger.info(
        '{0}: Inserted random number {1}'.format(current_dt, random_num))
    return str(random_num)

if __name__ == '__main__':
    app.run(debug=True)
