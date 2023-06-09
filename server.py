from flask import Flask, render_template, request
import socketio

sio = socketio.Server(async_mode="threading")
app = Flask(__name__, static_folder="static")
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
grid = []


@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("index.html")


@sio.event
def connect(sid, env, auth):
    sio.emit("status", "connected", to=sid)


@sio.event
def color(sid, data):
    global grid
    grid = data
    sio.emit("sendGrid", grid)


@sio.event
def getGrid(sid):
    sio.emit("sendGrid", grid)


@sio.event
def disconnect(sid):
    print("disconnected", sid)


app.run(host="0.0.0.0", port=80)
