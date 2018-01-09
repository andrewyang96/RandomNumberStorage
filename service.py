import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import json
import os
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

def send_email(timestamp, random_num):
    """Send email via Amazon SES."""
    email_config = config['email']
    subject = 'Random Number Storage Test Update'
    message = 'The random number is {0}. Generated at {1} UTC'.format(
        random_num, timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    body_html = '''<html>
        <head></head><body>
            <p>{0}</p>
            <img src="https://www.python.org/static/community_logos/python-logo.png">
        </body>
    </html>'''.format(message)
    client = boto3.client('ses', region_name='us-east-1')
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email_config['recipient'],
                ],
            }, Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': message,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=email_config['sender']
        )
    except ClientError as e:
        print('Error sending email: {0}'.format(e.response['Error']['Message']))
    else:
        print('Email sent! Message ID: {0}'.format(response['ResponseMetadata']['RequestId']))

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
    if os.environ.get('ENABLE_EMAIL'):
        print('Email enabled, sending email')
        send_email(current_dt, random_num)
    else:
        print('Email disabled')
    return random_num
