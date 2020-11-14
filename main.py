import socketio
import time
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user
from flask_socketio import SocketIO, send, emit
from threading import Thread

from user import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app=app, async_mode="threading")


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(id=request.form["pseudo"], app=app)
        login_user(user)
        # TODO validate flask.request.args.get('next') to prevent vulnerability to open redirect
        return render_template("index.j2", mining_speed=0, gold=0)
    return render_template("index.j2", mining_speed=0, gold=0)


@socketio.on("upgrade")
def handle_message(message):
    current_user.set_mining_speed(current_user.get_mining_speed() + 1)
    emit("gold", current_user.get_gold())
    emit("mining_speed", current_user.get_mining_speed())


@socketio.on("connect")
def connect():
    emit("my response", {"data": "Connected"})
    current_user.client = request.sid


def update_gold_amount():
    sleep_time = 0.5
    for _ in range(6000):
        time.sleep(sleep_time)
        print("running")
        for user in User.users().values():
            user.set_gold(user.get_gold() + user.get_mining_speed() * sleep_time)
            user_gold = user.get_gold()
            print(user_gold)
            print("emitting gold", user_gold)
            socketio.emit("gold", user_gold, room=user.client)


if __name__ == "__main__":
    print("started with main")
    thread = Thread(target=update_gold_amount, args=())
    thread.start()
    socketio.run(app)