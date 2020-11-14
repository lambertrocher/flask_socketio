import socketio
import time
import pymongo
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user
from flask_socketio import SocketIO, send, emit
from threading import Thread

from user import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app=app, async_mode='threading')

client = pymongo.MongoClient(f"mongodb+srv://admin:{app.config['MONGO_PASSWD']}@cluster0.soder.mongodb.net/admin?retryWrites=true&w=majority")
db = client.sample_airbnb
listing_and_review = db.listingsAndReviews
review = listing_and_review.find_one()
print("review", review)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(id=request.form['pseudo']) 
        login_user(user)
        #TODO validate flask.request.args.get('next') to prevent vulnerability to open redirect
    return render_template('index.j2', mining_speed=0, gold=0)

@socketio.on('upgrade')
def handle_message(message):
    current_user.mining_speed += 1
    emit('gold', current_user.gold)
    emit('mining_speed', current_user.mining_speed)

@socketio.on('connect')
def connect():
    emit('my response', {'data': 'Connected'})
    current_user.client = request.sid

def update_gold_amount():
    for _ in range(600):
        time.sleep(0.2)
        print("running")
        for user in User.users():
            User.get(user).gold += (User.get(user).mining_speed)/5
            print("emitting gold", User.get(user).gold)
            socketio.emit('gold', User.get(user).gold, room=User.get(user).client)

if __name__ == "__main__":
    print("started with main")
    thread = Thread(target=update_gold_amount, args=())
    thread.start()
    socketio.run(app)