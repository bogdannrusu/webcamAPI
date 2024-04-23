import io
import logging
import time
from flask import Flask, render_template, Response
from picamera import PiCamera

app = Flask(__name__, template_folder='src')


app.logger.setLevel(logging.DEBUG)

camera = PiCamera()
camera.resolution = (640, 480)


def gen_frames():
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
        stream.seek(0)
        stream.truncate()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
