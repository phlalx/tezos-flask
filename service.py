# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

import flask
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for, session
from tools import paths
from flask import g
from flask import jsonify
from flask import abort
import json
from client.client import Client
from tools import constants

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# tasks = [
#     {
#         'id': 1,
#         'title': u'tezos-client',
#         'description': u'call the tezos client',
#         'done': False
#     },
# ]

# @app.route('/tezos/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


# @app.route('/tezos/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})

ZERONET = False

if ZERONET:
    CLIENT = './tezos-client.zeronet'
    CLIENT_ADMIN = './tezos-admin-client.zeronet'
    HOST = '35.180.138.28'
    PORT = '8732'
else:
    CLIENT = './tezos-client'
    CLIENT_ADMIN = './tezos-admin-client'
    HOST = '127.0.0.1'
    PORT = '18731'


def tezos_client():
    # TODO use one client per session, clean-up client resources
    client = Client(CLIENT,
                    CLIENT_ADMIN,
                    host=HOST,
                    rpc_port=PORT,
                    use_tls=False)

    identities = constants.IDENTITIES
    client.import_secret_key('bootstrap1', identities['bootstrap1']['secret'])
    return client

# TODO  don't use global variable for client
CLIENT = tezos_client()


@app.route('/tezosclient', methods=['POST'])
def tezosclient():
    params = request.json['params']
    print(params)
    if not params or not params[0] in {'tezos-client', 'tezos-client-admin'}:
        return
    admin = params[0] == 'tezos-client-admin'
    res = CLIENT.run(params[1:], admin=admin)
    res = jsonify({ 'client_output': res })
    return res

@app.route('/')
def index(msg=None):
    return render_template('index.html', msg = msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # default port = 5000
