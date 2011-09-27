from bottle import get, run, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

users = set()

@get('/')
def index():
    return template('index')

@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in users:
                u.send(msg)
        else: break
    users.remove(ws)

run(host='127.0.0.1', port=8080, server=GeventWebSocketServer)
