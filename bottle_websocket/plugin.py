import base64
from hashlib import sha1
from bottle import request, HTTPError

from ws4py.exc import HandshakeError
from ws4py import WS_KEY
from ws4py.server.wsgi.middleware import WebSocketHandler

WS_VERSION = 8

def websocket(callback):
    def wrapper(*args, **kwargs):
        try:
            if 'websocket' not in request.environ.get('upgrade.protocol', ''):
                raise HandshakeError("Upgrade protocol is not websocket")

            if request.environ.get('REQUEST_METHOD') != 'GET':
                raise HandshakeError('Method is not GET')

            key = request.environ.get('HTTP_SEC_WEBSOCKET_KEY')
            if key:
                ws_key = base64.b64decode(key)
                if len(ws_key) != 16:
                    raise HandshakeError("WebSocket key's length is invalid")
            else:
                raise HandshakeError("Not a valid HyBi WebSocket request")

            version = request.environ.get('HTTP_SEC_WEBSOCKET_VERSION')
            if version:
                if version != str(WS_VERSION):
                    raise HandshakeError('Unsupported WebSocket version')
                request.environ['websocket.version'] = str(WS_VERSION)
            else:
                raise HandshakeError('WebSocket version required')
        except HandshakeError, e:
            raise HTTPError(code=400, output=e)

        # Collect supported subprotocols
        protocols = []
        subprotocols = request.environ.get('HTTP_SEC_WEBSOCKET_PROTOCOL')
        ws_protocols = []
        if subprotocols:
            for s in subprotocols.split(','):
                s = s.strip()
                if s in protocols:
                    ws_protocols.append(s)

        # Collect supported extensions
        exts = []
        ws_extensions = []
        extensions = request.environ.get('HTTP_SEC_WEBSOCKET_EXTENSIONS')
        if extensions:
            for ext in extensions.split(','):
                ext = ext.strip()
                if ext in exts:
                    ws_extensions.append(ext)

        # Build and start the HTTP response
        headers = [
            ('Upgrade', 'websocket'),
            ('Connection', 'Upgrade'),
            ('Sec-WebSocket-Version', request.environ['websocket.version']),
            ('Sec-WebSocket-Accept', base64.b64encode(sha1(key + WS_KEY).digest())),
        ]
        if ws_protocols:
            headers.append(('Sec-WebSocket-Protocol', ', '.join(ws_protocols)))
        if ws_extensions:
            headers.append(('Sec-WebSocket-Extensions', ','.join(ws_extensions)))
        socket = request.environ.get('upgrade.socket')
        socket.send("HTTP/1.1 101 Switching Protocols\r\n")
        for k,v in headers:
            socket.send(': '.join([k,v]) + '\r\n')
        socket.send('\r\n')
        websocket = WebSocketHandler(socket, ws_protocols, ws_extensions, request.environ)
        callback(websocket, *args, **kwargs)
        websocket.close()
    return wrapper
