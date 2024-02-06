import logging

from csctracker_py_core.models.emuns.config import Config
from csctracker_py_core.starter import Starter
from csctracker_py_core.utils.configs import Configs
from csctracker_py_core.utils.interceptor import g

starter = Starter()
app = starter.get_app()
http_repository = starter.get_http_repository()


@app.route('/api/v1/consumo', methods=['POST'])
def consumo():  # put application's code here
    try:
        headers = {
            'Authorization': "Bearer " + Configs.get_env_variable(Config.API_TOKEN),
            'x-correlation-id': g.correlation_id
        }
    except:
        headers = {
            'Authorization': "Bearer " + Configs.get_env_variable(Config.API_TOKEN),
        }

    args = http_repository.get_args()
    body = {}
    response = http_repository.post(f"{Configs.get_env_variable(Config.URL_BFF)}monitor-consumo/consumo",
                                    headers=headers,
                                    body=body,
                                    args=args)
    return "ok", 200, {'Content-Type': 'application/x-www-form-urlencoded'}


@app.route('/<service>/<port>/<path:parts>', methods=['POST'])
def redirect_post(service, port, parts):  # put application's code here

    args = http_repository.get_args()
    headers = http_repository.get_headers()
    body = http_repository.get_json_body()
    response = http_repository.post(f"http://{service}:{port}/{parts}",
                                    headers=headers,
                                    body=body,
                                    args=args)
    logging.getLogger().info(response.text)
    return response.text, response.status_code, {'Content-Type': 'application/json'}


@app.route('/<service>/<port>/<path:parts>', methods=['GET'])
def redirect_get(service, port, parts):
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    response = http_repository.get(f"http://{service}:{port}/{parts}", headers=headers, params=args)
    return response.text


starter.start()
