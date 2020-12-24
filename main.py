from flask_login.utils import logout_user
import socketio
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_socketio import SocketIO, emit
from threading import Thread
import flask.json
from flask.json import JSONEncoder

from user import User


class MyJsonEncoder(JSONEncoder):
    def default(self, object):
        try:
            return getattr(object, "to_json")()
        except AttributeError:
            return JSONEncoder.default(self, object)

app = Flask(__name__, instance_relative_config=True)
app.json_encoder = MyJsonEncoder
app.config.from_pyfile("config.py")
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app=app, async_mode="threading", json=flask.json)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@socketio.on("connect")
def connect():
    emit("my response", {"data": "Connected"})
    current_user.client = request.sid


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(id=request.form["pseudo"], app=app)
        login_user(user)
        # TODO validate flask.request.args.get('next') to prevent vulnerability to open redirect
        return render_template(
            "resources.j2", resources = user.resources
        )
    return render_template("login.j2")


@app.route("/logout", methods=["GET"])
def logout():
    print("logging out")
    logout_user()
    return redirect(url_for("login"))


@socketio.on("upgrade")
def upgrade(message):
    message = message["data"]
    if message == "upgrade_hunting":
        current_user.food.set_speed(current_user.food.get_speed() + 1)
        current_user.food.set_level(current_user.food.get_level() + 1)
        emit("hunting_speed", current_user.food.get_speed())
    elif message == "upgrade_chopping":
        current_user.wood.set_speed(current_user.wood.get_speed() + 1)
        current_user.wood.set_level(current_user.wood.get_level() + 1)
        emit("chopping_speed", current_user.wood.get_speed())
    elif message == "upgrade_coal_mining":
        current_user.coal.set_speed(current_user.coal.get_speed() + 1)
        current_user.coal.set_level(current_user.coal.get_level() + 1)
        emit("coal_mining_speed", current_user.coal.get_speed())
    elif message == "upgrade_metal_mining":
        current_user.metal.set_speed(current_user.metal.get_speed() + 1)
        current_user.metal.set_level(current_user.metal.get_level() + 1)
        emit("metal_mining_speed", current_user.metal.get_speed())

def update_resources():
    sleep_time = 0.5
    while True:
        time.sleep(sleep_time)
        for user in User.users().values():
            for resource in user.resources:
                resource.set_amount(
                    resource.get_amount() + resource.get_speed() * sleep_time
                )
            socketio.emit("resources", user.resources, room=user.client)


if __name__ == "__main__":
    thread = Thread(target=update_resources, args=())
    thread.start()
    socketio.run(app)