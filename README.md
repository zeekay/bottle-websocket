This project adds websocket capabilities to [bottle](http://bottlepy.org), leveraging [Websocket-for-Python](https://github.com/Lawouach/WebSocket-for-Python) and [gevent](http://www.gevent.org/).

Usage is pretty straight-forward, just import the server and plugin:

    from bottle_websocket.server import GeventWebSocketServer
    from bottle_websocket.plugin import websocket

You can use the websocket plugin to turn routes websocket handlers, the websocket is passed to the route as the first argument:

    @get('/websocket', apply=[websocket])
    def echo(ws):
        while True:
            msg = ws.receive()
            if msg is not None:
                ws.send(msg)
            else: break
        ws.close()

And then use the provided server:

    run(host='127.0.0.1', port=8080, server=GeventWebSocketServer, monkey=True)
