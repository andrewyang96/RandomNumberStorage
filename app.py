from flask import Flask
import logging
import random

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET'])
def main_handler(event=None, context=None):
    random_num = random.randint(0, 9)
    logger.info('Random number is {0}'.format(random_num))
    return str(random_num)

if __name__ == '__main__':
    app.run(debug=True)
