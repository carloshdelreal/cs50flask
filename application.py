import os

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {}
idgen = 0

@app.route("/")
def index():
    return render_template("index.html", channels=channels.keys())

@socketio.on("new channel")
def newchannel(data):
    if data['channel'] in channels.keys():
        pass
    else:
        channels[data['channel']] = []
        emit("newChannel", { 'channel': data['channel'] }, broadcast=True)

@app.route("/chatmsgs", methods=["POST"])
def channeldata():
    # Query for chat room
    channel = request.form.get("channel")
    if channel in channels.keys():
        return jsonify( {"channel": channel, "msgs": channels[channel], 'success': True })
    else:
        return jsonify( { "channel": channel, 'success': False})


@socketio.on("new msg")
def chatmsg(data):
    channel = data['channel']
    chaterName = data["chaterName"]
    msg = data["msg"]
    timestamp = data["timestamp"]
    if len(channels[channel])>99:
        channels[channel].pop()
    global idgen
    msgIndex = idgen
    idgen += 1
    channels[channel].append([chaterName,msg,timestamp,msgIndex])
    emit("msg", {"msgIndex":msgIndex,
                'chaterName':chaterName,
                'msg': msg, 
                "timestamp": timestamp}, broadcast=True)

@socketio.on("msg delete")
def msgdelete(data):
    channel = data["channel"]
    msgid = data["msgid"]
    channels[channel][:] = [ msg for msg in channels[channel] if msg[3] != int(msgid) ]
