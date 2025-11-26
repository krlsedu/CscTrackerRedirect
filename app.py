import logging
import platform
import subprocess
import time

import requests
from csctracker_py_core.starter import Starter
from csctracker_py_core.utils.configs import Configs

from enums.config_redirect import ConfigRedirect

starter = Starter(
    save_request=Configs.get_env_variable(ConfigRedirect.SAVE_REQUESTS, default='False').lower() == 'true'
)
app = starter.get_app()
http_repository = starter.get_http_repository()

remote_on = False

def monitor_connectivity(interval=30):
    """
    Roda em background a cada 'interval' segundos.
    Pinga o IP definido na ENV 'TARGET_IP_PING'.
    Se responder, remote_on = True. Caso contrário, False.
    """
    global remote_on
    target_ip = Configs.get_env_variable(ConfigRedirect.TARGET_IP_PING)

    if not target_ip:
        logging.getLogger().warning("Variável de ambiente 'TARGET_IP_PING' não definida. Monitoramento cancelado.")
        return

    # Define o parâmetro do ping (-n para Windows, -c para Linux/Mac)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Monta o comando: ping -n 1 <ip>
    command = ['ping', param, '1', target_ip]

    while True:
        try:
            # Executa o ping ocultando a saída (stdout/stderr)
            # subprocess.call retorna 0 se houve sucesso (resposta do ping)
            response = subprocess.call(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            remote_on = (response == 0)

        except Exception as e:
            logging.getLogger().error(f"Erro ao executar ping: {e}")
            remote_on = False

        time.sleep(interval)


@app.route('/<service>/<port>/<path:parts>', methods=['POST'])
def redirect_post(service, port, parts):  # put application's code here
    global remote_on
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    body = http_repository.get_json_body()
    if remote_on:
        target_ip = Configs.get_env_variable(ConfigRedirect.TARGET_IP_PING)
        try:
            response = http_repository.post(f"http://{target_ip}:5000/{service}/{port}/{parts}",
                                        headers=headers,
                                        body=body,
                                        args=args)
        except requests.exceptions.Timeout:
            logging.getLogger().error(f"Timeout ao executar POST")
            remote_on = False
            response = http_repository.post(f"http://{service}:{port}/{parts}",
                                        headers=headers,
                                        body=body,
                                        args=args)
    else:
        response = http_repository.post(f"http://{service}:{port}/{parts}",
                                        headers=headers,
                                        body=body,
                                        args=args)

    logging.getLogger().info(response.text)
    return response.text, response.status_code, {'Content-Type': 'application/json'}


@app.route('/<service>/<port>/<path:parts>', methods=['GET'])
def redirect_get(service, port, parts):
    global remote_on
    args = http_repository.get_args()
    headers = http_repository.get_headers()
    if remote_on:
        target_ip = Configs.get_env_variable(ConfigRedirect.TARGET_IP_PING)
        try:
            response = http_repository.get(f"http://{target_ip}:5000/{service}/{port}/{parts}", headers=headers, params=args)
        except requests.exceptions.Timeout:
            logging.getLogger().error(f"Timeout ao executar GET")
            remote_on = False
            response = http_repository.get(f"http://{service}:{port}/{parts}", headers=headers, params=args)
    else:
        response = http_repository.get(f"http://{service}:{port}/{parts}", headers=headers, params=args)
    return response.text


starter.start()
