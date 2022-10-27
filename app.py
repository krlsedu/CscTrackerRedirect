import json

import pika as pika
from flask import request

import requests as requests
from flask import Flask

app = Flask(__name__)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='redirect', durable=True)


@app.route('/notify-sync/message', methods=['POST'])
def redirect_notify():  # put application's code here
    jsn = request.get_json()
    msg = {
        'body': json.dumps(jsn, ensure_ascii=False),
        'token': request.headers.get('Authorization'),
        'url': '/notify-sync/message'
    }
    print(msg)
    channel.basic_publish(exchange='', routing_key='redirect', body=json.dumps(msg, ensure_ascii=False))
    return "{}", 201, {'Content-Type': 'application/json'}


@app.route('/backend/usage-info', methods=['POST'])
def redirect_usage_info():  # put application's code here
    jsn = request.get_json()
    msg = {
        'body': json.dumps(jsn, ensure_ascii=False),
        'token': request.headers.get('Authorization'),
        'url': '/backend/usage-info'
    }
    print(msg)
    channel.basic_publish(exchange='', routing_key='redirect', body=json.dumps(msg, ensure_ascii=False))
    return "{}", 201, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run()
