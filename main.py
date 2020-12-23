from flask_login.utils import logout_user
import socketio
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
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
            "resources.j2", mining_speed=0, food=0, wood=0, coal=0, metal=0
        )
    return render_template("login.j2")


@app.route("/logout", methods=["GET"])
def logout():
    print("logging out")
    logout_user()
    return redirect(url_for("login"))


@socketio.on("upgrade")
def upgrade(message):
    message = message['data']
    if message == 'upgrade_hunting':
        current_user.food.set_speed(current_user.food.get_speed() + 1)
        emit("hunting_speed", current_user.food.get_speed())
    elif message == 'upgrade_chopping':
        current_user.wood.set_speed(current_user.wood.get_speed() + 1)
        emit("chopping_speed", current_user.wood.get_speed())
    elif message == 'upgrade_coal_mining':
        current_user.coal.set_speed(current_user.coal.get_speed() + 1)
        emit("coal_mining_speed", current_user.coal.get_speed())
    elif message == 'upgrade_metal_mining':
        current_user.metal.set_speed(current_user.metal.get_speed() + 1)
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
                resource_amount = resource.get_amount()
                print(resource_amount)
                print(f"emitting resource {resource.name}", resource_amount)
                socketio.emit(resource.name, resource_amount, room=user.client)


if __name__ == "__main__":
    thread = Thread(target=update_resources, args=())
    thread.start()
    socketio.run(app)