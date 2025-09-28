from flask import Flask, render_template , request
from flask_socketio import SocketIO, emit
import uuid
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

participants = {}  # { sid: {"id": str, "name": str, "mic": bool, "avatar": str} }

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join(data):
    name = data.get("name", "Guest")
    avatar = f"https://i.pravatar.cc/150?u={uuid.uuid4()}"  # unique avatar
    participants[request.sid] = {"id": request.sid, "name": name, "mic": True, "avatar": avatar}
    emit("participantsUpdate", participants, broadcast=True)

@socketio.on("toggleMic")
def handle_toggle(data):
    status = data.get("status", True)
    if request.sid in participants:
        participants[request.sid]["mic"] = status
        emit("participantsUpdate", participants, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    if request.sid in participants:
        del participants[request.sid]
        emit("participantsUpdate", participants, broadcast=True)

@socketio.on("signal")
def handle_signal(message):
    # Relay WebRTC offer/answer/ice candidates
    emit("signal", message, broadcast=True, include_self=False)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

