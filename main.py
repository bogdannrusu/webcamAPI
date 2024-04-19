import os
import cv2
import logging
from flask import Flask, render_template, Response

app = Flask(__name__, template_folder='src')

# Configure logging
app.logger.setLevel(logging.DEBUG)  # Set logging level

# Specify the directory where you want to save captured images
IMAGE_DIR = 'captured_images'

# Create the directory if it doesn't exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    app.logger.info(f"Created directory: {IMAGE_DIR}")

camera = cv2.VideoCapture(0)


def capture_image():
    success, frame = camera.read()  # Capture frame from camera
    if success:
        app.logger.debug("Successfully captured frame from camera")
        return frame
    else:
        app.logger.error("Failed to capture frame from camera")
        return None


def save_image(image):
    # Generate a unique filename
    filename = os.path.join(IMAGE_DIR, 'captured_image.jpg')

    # Save the image to disk
    cv2.imwrite(filename, image)
    app.logger.info(f"Image saved at: {filename}")
    return filename


def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            app.logger.error("Failed to read frame from camera")
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


@app.route('/capture_image')
def capture_image_route():
    frame = capture_image()  # Capture image from camera
    if frame is not None:
        image_path = save_image(frame)  # Save image to disk
        app.logger.info(f"Image captured and saved as {image_path}")
        return f"Image captured and saved as {image_path}"
    else:
        app.logger.error("Failed to capture image")
        return "Failed to capture image."


if __name__ == "__main__":
    app.run(debug=True)
