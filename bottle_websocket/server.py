from bottle import ServerAdapter
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

class GeventWebSocketServer(ServerAdapter):
    def run(self, handler):
        pywsgi.WSGIServer((self.host, self.port), handler, handler_class=WebSocketHandler).serve_forever()
