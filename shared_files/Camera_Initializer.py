from General.models import Devices
from AI.CAMERA import VideoCamera
import asyncio
import cv2
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import logging

camera_instances = {}

def initialize_cameras():
    global camera_instances
    dev = Devices()
    cameras = dev.get_Devices()  # Assuming this returns a dictionary

    try:
        # Initialize camera instances safely
        for key, value in cameras.items():
            if len(str(value)) == 1:
                cameras[key] = int(value)
            try:
                camera_instances[key] = VideoCamera(cameras[key], key)
                logging.info(f"Camera {key} initialized successfully.")
            except ValueError as ve:
                logging.warning(f"Skipping camera {key}: {ve}")
            except Exception as e:
                logging.error(f"Unexpected error initializing camera {key}: {e}")
    except Exception as e:
        logging.critical(f"Critical error initializing cameras: {e}")
        raise e  # Raise the exception after logging to avoid silent failures

async def fetch_frames():
    for camera_id, camera in camera_instances.items():
        frame = await camera.get_frame()
        # if frame is not None:
        #     np_frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
        #     cv2.imshow(f'Camera {camera_id}', np_frame)
        #     cv2.waitKey(1)

def start_background_task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: asyncio.run(fetch_frames()), trigger="interval", seconds=2)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())




def addCam(key, value):
    global camera_instances
    try:
        if value.isdigit():
            value = int(value)
        camera_instances[key] = VideoCamera(value, key)
    except Exception as e:
        print("error in adding camera")
        raise e

def get_instances():
    global camera_instances
    return camera_instances

def rel(camera_id):
    if camera_id in camera_instances:
        camera_instances[camera_id].release()  # Release the camera resource
        del camera_instances[camera_id]  # Delete the instance from the dictionary
    else:
        print(f"Camera ID {camera_id} not found.")

def reinitialize_cameras():
    global camera_instances

    # Release all existing camera instances
    for camera_id, camera in camera_instances.items():
        print("starting releasing camera")
        camera_instances[camera_id].release()
        print("cam released!")
    camera_instances.clear()

    # Reinitialize cameras
    initialize_cameras()
    print("Cameras reinitialized")

# Initialize cameras and start the background task

# from threading import Thread
# ini_cam = Thread(target=initialize_cameras, args=())
# ini_cam.start()

initialize_cameras()
