from flask import Flask, render_template, jsonify, Response
import pyautogui
from src.recorder.Recorder import VideoStream
from src.utils.utils import timed_call, genVideoFeed
from flask_socketio import SocketIO, emit
from engineio.payload import Payload
from src.controls.Controller import Controller

Payload.max_decode_packets = 500

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

stream = VideoStream()
controller = Controller()

FPS = 30

@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(timed_call(genVideoFeed,FPS,stream),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/res',methods=['GET'])
def get_res():
    res = stream.getRes()
    return jsonify({'x' : res[0], 'y' : res[1] })

@socketio.on('mouse_move')
def handle_mouse_move(data):
    r = stream.getRes()
    controller.mouse_move(r,data)

@socketio.on('mouse_click')
def handle_mouse_click(data):
    r = stream.getRes()
    controller.mouse_click(r,data)


@socketio.on('keyboard')
def handle_key_press(data):
    controller.press_key(data)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')