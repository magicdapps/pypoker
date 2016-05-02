import os
import gevent
from flask import Flask, render_template, session
from flask_sockets import Sockets
import random
import uuid
import time
from poker import ServerWebSocket, WebSocketChannel, PlayerServer

app = Flask(__name__)
app.config['SECRET_KEY'] = '!!_-pyp0k3r-_!!'
app.debug = True

sockets = Sockets(app)

server = ServerWebSocket(app.logger)
gevent.spawn(server.start)

names = [
    "Leonard",
    "Michael",
    "Fab",
    "Charles",
    "Jim",
    "Jimy",
    "John",
    "Paul",
    "George",]

surnames = [
    "Morrison",
    "Hendrix",
    "Lennon",
    "McCartney",
    "Harrison",]


players = {}


@app.route('/')
def hello():
    global names, surnames
    if 'player-id' not in session:
        session['player-id'] = str(uuid.uuid4())
        session['player-name'] = random.choice(names) + " " + random.choice(surnames)
        session['player-money'] = 1000.00
    return render_template('index.html',
                           id=session['player-id'],
                           name=session['player-name'],
                           money=session['player-money'])


@sockets.route('/poker5')
def poker5(ws):
    player = PlayerServer(
        channel=WebSocketChannel(ws),
        id=session['player-id'],
        name=session['player-name'],
        money=session['player-money'])

    server.register(player)

    last_ping = time.time()
    while not ws.closed:
        # Keep the websocket alive
        gevent.sleep(0.1)
        if time.time() > last_ping + 20:
            # Ping the client every 20 secs to prevent idle connections
            player.ping()
            last_ping = time.time()


# if __name__ == '__main__':
#     app.run()
