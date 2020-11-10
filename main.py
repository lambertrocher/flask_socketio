import socketio
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user
from flask_socketio import SocketIO, send, emit

from user import User

app = Flask(__name__)
app.secret_key = 'my secret key'
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app=app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(request.form['pseudo']) 
        login_user(user)
        #TODO validate flask.request.args.get('next') to prevent vulnerability to open redirect
    return render_template('index.j2')

@app.route('/home')
def home():
    return render_template('index.j2', x=0)


@socketio.on('my event')
def handle_message(message):
    print(current_user)
    print('received event: ', message)
    current_user.gold += 1
    emit('my event', current_user.gold)

@socketio.on('connect')
def connect():
    emit('my response', {'data': 'Connected'})

if __name__ == "__main__":
    socketio.run(app)