from flask import Flask, render_template, jsonify, Response, make_response, redirect, request
from src.recorder.Recorder import VideoStream
from src.utils.utils import timed_call, genVideoFeed
from flask_socketio import SocketIO, emit
from engineio.payload import Payload
from src.controls.Controller import Controller
from src.authentication.Auth import Auth
from config import MAX_DECODE_PACKETS , COOKIE_MAX_AGE , FPS


Payload.max_decode_packets = MAX_DECODE_PACKETS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
auth = Auth()

stream = VideoStream()
controller = Controller()

authenticated = False

@app.before_request
def hook():
    global authenticated
    print('endpoint: %s, url: %s, path: %s' % (
        request.endpoint,
        request.url,
        request.path))
    cookie = request.cookies.get('auth')
    print('cookie recieved',cookie)
    if cookie == None:
        authenticated = False
    else:
        authenticated = auth.isAuthenticated(cookie)

@app.route("/", methods=['GET'])
def home():
    global authenticated
    if not authenticated:
        return redirect('/login')
    return render_template('index.html')

@app.route("/wrong", methods=['GET'])
def wrong():
    return render_template('unauth.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/video_feed')
def video_feed():
    if not authenticated:
        return redirect('/login')
    return Response(timed_call(genVideoFeed,FPS,stream),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/res',methods=['GET'])
def get_res():
    if not authenticated:
        return redirect('/login')
    res = stream.getRes()
    return jsonify({'x' : res[0], 'y' : res[1] })

@app.route('/login',methods=['POST'])
def login():
    global authenticated
    if authenticated:
        auth.generateRandomPasscode()
        authenticated = False
    data = request.get_json()
    key = data['key']
    match = auth.matchesPasscode(key)
    if match:
        resp = make_response(redirect('/'))
        resp.set_cookie('auth',auth.gen_cookie(),max_age=COOKIE_MAX_AGE)
        return resp
    else:
        resp = make_response(redirect('/wrong'))
        resp.delete_cookie('auth')
        return resp

@app.route('/login',methods=['GET'])
def loginView():
    global authenticated
    resp = make_response(render_template('login.html'))
    resp.delete_cookie("auth")
    if authenticated:
        auth.generateRandomPasscode()
        authenticated = False
    return resp

@app.route('/logout',methods=['GET'])
def logout():
    global authenticated
    resp = make_response(redirect('/login'))
    resp.delete_cookie("auth")
    authenticated = False
    auth.generateRandomPasscode()
    return resp

@socketio.on('mouse_move')
def handle_mouse_move(data):
    if not authenticated:
        return redirect('/login')
    r = stream.getRes()
    controller.mouse_move(r,data)

@socketio.on('mouse_click')
def handle_mouse_click(data):
    r = stream.getRes()
    if(data['press'] == 'd'):
        controller.mouse_click_down(r, data)
    else:
        controller.mouse_click_up(r, data)


@socketio.on('keyboard')
def handle_key_press(data):
    if(data['press'] == 'd'):
        controller.press_key_down(data)
    else:
        controller.press_key_up(data)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')