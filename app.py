import os

import requests as requests
from flask import Flask
from flask import request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app, group_by='endpoint', default_labels={'application': 'CscTrackerRedirect'})
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


@app.route('/<service>/<port>/<part1>', methods=['POST'])
def redirect1(service, port, part1):  # put application's code here

    args = request.args
    headers = request.headers
    body = request.json
    response = requests.post(f"http://{service}:{port}/{part1}", headers=headers, json=body, params=args)
    print(response.text)
    return response, response.status_code, {'Content-Type': 'application/json'}


@app.route('/<service>/<port>/<part1>', methods=['GET'])
def redirectGet1(service, port, part1):
    args = request.args
    headers = request.headers
    body = {}
    response = requests.get(f"http://{service}:{port}/{part1}", headers=headers, json=body)
    ##print if url contains federated
    if part1.find("federate") != -1:
        print(response.text)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>', methods=['POST'])
def redirect2(service, port, part1, part2):  # put application's code here

    args = request.args
    headers = request.headers
    body = request.get_json()
    response = requests.post(f"http://{service}:{port}/{part1}/{part2}", headers=headers, json=body, params=args)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>', methods=['GET'])
def redirectGet2(service, port, part1, part2):
    args = request.args
    headers = request.headers
    body = {}
    response = requests.get(f"http://{service}:{port}/{part1}/{part2}", headers=headers, json=body)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>/<part3>', methods=['POST'])
def redirect3(service, port, part1, part2, part3):  # put application's code here

    args = request.args
    headers = request.headers
    body = request.get_json()
    response = requests.post(f"http://{service}:{port}/{part1}/{part2}/{part3}", headers=headers, json=body,
                             params=args)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>/<part3>', methods=['GET'])
def redirectGet3(service, port, part1, part2, part3):
    args = request.args
    headers = request.headers
    body = {}
    url = f"http://{service}:{port}/{part1}/{part2}/{part3}"
    response = requests.get(url, headers=headers, json=body)
    return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
