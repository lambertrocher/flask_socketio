from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from flask_socketio import send
from flask_socketio import emit
import socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app=app)

x = 0

@app.route('/home')
def home():
    global x
    return render_template('index.j2', x=x)


@socketio.on('my event')
def handle_message(message):
    global x
    print('received event: ', message)
    x += 1
    emit('my event', x)

if __name__ == "__main__":
    socketio.run(app)