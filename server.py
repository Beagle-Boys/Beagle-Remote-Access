from flask import Flask, render_template, jsonify, Response
from src.recorder.Recorder import VideoStream
from src.utils.utils import timed_call, genVideoFeed

app = Flask(__name__)
stream = VideoStream()

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

if __name__ == "__main__":
    app.run(debug=True)