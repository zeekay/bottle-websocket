from bottle import ServerAdapter
from gevent import pywsgi, monkey, local
from ws4py.server.geventserver import UpgradableWSGIHandler
import threading

class GeventWebSocketServer(ServerAdapter):
    def run(self, handler):
        if not threading.local is local.local: monkey.patch_all()
        pywsgi.WSGIServer((self.host, self.port), handler, handler_class=UpgradableWSGIHandler).serve_forever()
