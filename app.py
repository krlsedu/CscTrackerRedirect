import json
import os

from flask import request

import requests as requests
from flask import Flask

app = Flask(__name__)

url_repository = 'https://backend.csctracker.com/'


@app.route('/api/v1/consumo', methods=['POST'])
def consumo():  # put application's code here

    headers = {
        'Authorization': "Bearer " + os.environ['TOKEN_INTEGRACAO']
    }

    args = request.args
    body = {}
    response = requests.post(f"{url_repository}monitor-consumo/consumo", headers=headers, json=body, params=args)
    return "ok", 200, {'Content-Type': 'application/x-www-form-urlencoded'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
