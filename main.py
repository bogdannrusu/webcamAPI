import cv2
import logging
from flask import Flask, render_template, Response

app = Flask(__name__, template_folder='src')

# Configure logging
app.logger.setLevel(logging.DEBUG)  # Set logging level

# Initialize the webcam capture object
webcam_camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = webcam_camera.read()  # read the camera frame
        if not success:
            app.logger.error("Failed to read frame from webcam")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                app.logger.error("Failed to encode frame")
                break
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
