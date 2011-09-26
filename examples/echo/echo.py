from bottle import route, run, template
from bottle_websocket.server import GeventWebSocketServer
from bottle_websocket.plugin import websocket

@route('/')
def index():
    return template('index')

@route('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive(msg_obj=True)
        if msg is not None:
            print 'WebSocket message recieved:', msg
            ws.send(msg.data)
        else:
            break
    ws.close()

run(host='127.0.0.1', port=8080, server=GeventWebSocketServer, monkey=True)
