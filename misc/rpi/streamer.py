import base64
import time
import threading
from threading import Timer
import cv2
import numpy as np
import requests
import json


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class State:
    # Device ID (typically 0)
    video_device_id = 0
    # can alternatively be a RTSP endpoint
    # video_device_id = 'http://192.168.0.1:8080/video/mjpeg'

    # GAN endpoint for inference
    gan_endpoint = 'http://api.selfie2anime.com/process'

    # Local render scale factor.
    display_scale = 1

    # Current frame.
    frame = None
    gan_frame = None

    # When changed to false, program will be terminated.
    running = True


# Init state for camera
state = State()


def read_frame_thread():
    """read frame from camera"""
    try:
        capture = cv2.VideoCapture(state.video_device_id)
        while state.running:
            _, frame = capture.read()
            state.frame = frame
            time.sleep(0.01)

    except Exception as e:
        print(e)
        state.running = False


def send_frame_thread():
    """send frame from camera"""
    try:
        if state.running:
            # Get recent frame
            frame = state.frame

            _, buffer = cv2.imencode('.jpg', frame)
            frame_as_text = base64.b64encode(buffer)

            data = {
                "image": "data:image/jpeg;base64,{}".format(str(frame_as_text)[2:])
            }

            headers = {
                "Content-Type": "application/json",
            }

            response = requests.request(
                "POST",
                state.gan_endpoint,
                data=json.dumps(data),
                headers=headers
            )

            selfie_response = response.json()
            selfie_data = selfie_response['selfie']
            selfie_gan_encoded = base64.b64decode(selfie_data[2:])
            selfie_gan_np_data = np.fromstring(selfie_gan_encoded, np.uint8)

            state.gan_frame = cv2.imdecode(
                selfie_gan_np_data, cv2.IMREAD_UNCHANGED)

    except Exception as e:
        print(e)
        state.running = False


def process_events():
    """process any key presses"""
    if cv2.waitKey(1) & 0xFF == ord('q'):
        state.running = False


def stream():
    """video stream"""
    # Run frame thread
    threading.Thread(target=read_frame_thread).start()

    # Send frame every 10 seconds
    rt = RepeatedTimer(10, send_frame_thread)

    while state.running:
        if state.frame is None:
            time.sleep(0.01)
            continue

        if state.gan_frame is not None:
            # display frame
            cv2.imshow('frame', cv2.resize(state.gan_frame, None,
                                           fx=state.display_scale, fy=state.display_scale))

        # handle key press events
        process_events()


if __name__ == '__main__':
    stream()
