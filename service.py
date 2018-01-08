from datetime import datetime
import json
import psycopg2
import random

with open('config.json', 'r') as f:
    config = json.load(f)

def get_db_connection():
    """Get psycopg2 connection to RDS instance."""
    db_config = config['database']
    print('Connecting to database at {0}'.format(db_config['host_url']))
    return psycopg2.connect(
        host=db_config['host_url'],
        dbname=db_config['db_name'],
        user=db_config['username'],
        password=db_config['password'])

def handler(event, context):
    conn = get_db_connection()
    cur = conn.cursor()

    print('Generating number')
    random_num = random.randint(0, config['max_number'])
    current_dt = datetime.utcnow()

    cur.execute(
        'INSERT INTO history (timestamp, random_num) VALUES (%s, %s)',
        (current_dt, random_num))
    conn.commit()
    cur.close()
    conn.close()

    print('{0}: Inserted random number {1}'.format(current_dt, random_num))
    return random_num
