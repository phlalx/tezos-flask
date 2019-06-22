import flask
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for, session
from tools import paths
from flask import g
import json
from client.client import Client

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


ZERONET = True

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
    if 'tezos_client' not in g:
        g.tezos_client = Client(CLIENT,
                                CLIENT_ADMIN,
                                host=HOST,
                                rpc_port=PORT,
                                use_tls=False)
    return g.tezos_client


@app.route('/checkdoc')
def checkdoc():
    _val = flask.request.args.get('val', default = '', type = str)
    client = tezos_client()
    res = client.p2p_stat()
    return res

@app.route('/checkrpc')
def checkrpc():
    val = flask.request.args.get('val', default = '', type = str)
    client = tezos_client()
    res = client.rpc('get', val)
    return json.dumps(res, indent=4, sort_keys=True)

@app.route('/')
def index(msg = None):
    return render_template('index.html', msg = msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # default port = 5000
