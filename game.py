from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    player_id = str(uuid.uuid4())
    players[player_id] = {"x": 400, "y": 300}
    emit("init", {"id": player_id, "players": players}, broadcast=False)
    emit("update", players, broadcast=True)
    print(f"玩家连接：{player_id}")

@socketio.on("disconnect")
def on_disconnect():
    for pid in list(players.keys()):
        if players[pid].get("sid") == request.sid:
            del players[pid]
            emit("remove", pid, broadcast=True)
            print(f"玩家离开：{pid}")
            break

@socketio.on("move")
def on_move(data):
    sid = request.sid
    for pid, p in players.items():
        if p.get("sid") == sid:
            p["x"] = data["x"]
            p["y"] = data["y"]
            break
    emit("update", players, broadcast=True)

@socketio.on("register")
def on_register():
    sid = request.sid
    for pid in players:
        if "sid" not in players[pid]:
            players[pid]["sid"] = sid
            break

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
