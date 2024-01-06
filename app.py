import os

from csctracker_py_core.starter import Starter

starter = Starter()
app = starter.get_app()
http_repository = starter.get_http_repository()

backend_url = 'https://backend.csctracker.com/'


@app.route('/api/v1/consumo', methods=['POST'])
def consumo():  # put application's code here

    headers = {
        'Authorization': "Bearer " + os.environ['TOKEN_INTEGRACAO']
    }

    args = http_repository.get_args()
    body = {}
    response = http_repository.post(f"{backend_url}monitor-consumo/consumo",
                                    headers=headers,
                                    body=body,
                                    args=args)
    return "ok", 200, {'Content-Type': 'application/x-www-form-urlencoded'}


@app.route('/<service>/<port>/<part1>', methods=['POST'])
def redirect1(service, port, part1):  # put application's code here

    args = http_repository.get_args()
    headers = http_repository.get_headers()
    body = http_repository.get_json_body()
    response = http_repository.post(f"http://{service}:{port}/{part1}",
                                    headers=headers,
                                    body=body,
                                    args=args)
    print(response.text)
    return response, response.status_code, {'Content-Type': 'application/json'}


@app.route('/<service>/<port>/<part1>', methods=['GET'])
def redirectGet1(service, port, part1):
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    response = http_repository.get(f"http://{service}:{port}/{part1}", headers=headers, params=args)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>', methods=['POST'])
def redirect2(service, port, part1, part2):
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    body = http_repository.get_json_body()
    response = http_repository.post(f"http://{service}:{port}/{part1}/{part2}",
                                    headers=headers,
                                    body=body,
                                    args=args)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>', methods=['GET'])
def redirectGet2(service, port, part1, part2):
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    response = http_repository.get(f"http://{service}:{port}/{part1}/{part2}", headers=headers, params=args)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>/<part3>', methods=['POST'])
def redirect3(service, port, part1, part2, part3):
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    body = http_repository.get_json_body()
    response = http_repository.post(f"http://{service}:{port}/{part1}/{part2}/{part3}",
                                    headers=headers,
                                    body=body,
                                    args=args)
    return response.text


@app.route('/<service>/<port>/<part1>/<part2>/<part3>', methods=['GET'])
def redirectGet3(service, port, part1, part2, part3):
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    url = f"http://{service}:{port}/{part1}/{part2}/{part3}"
    response = http_repository.get(url, headers=headers, params=args)
    return response.text


starter.start()
