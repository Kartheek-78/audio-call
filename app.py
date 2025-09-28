from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on("signal")
def handle_signal(message):
    # Broadcast signaling messages between peers
    emit("signal", message, broadcast=True, include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)


