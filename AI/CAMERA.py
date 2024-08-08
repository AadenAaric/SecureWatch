import cv2
from threading import Thread, Lock
from .detector import FrameProcessor, draw_face_detections
import asyncio
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
import os
from datetime import datetime
import requests
from shared_files.FCM import get_access_token
from shared_files.globals import getDevToken , GetListofToken

class VideoCamera:
    def __init__(self, src, camera_id):
        self.cap = cv2.VideoCapture(src)
        self.lock = Lock()
        self.frame = None
        self.processed_frame = None
        self.running = True
        self.frame_processor = FrameProcessor()
        self.camera_id = camera_id

        # Get the video frame width and height
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # Fallback FPS if not available from the source
        if self.fps == 0:
            self.fps = 20.0

        # Define the video directory (independent of machine)
        self.video_dir = os.path.join(os.path.expanduser('~'), 'Videos', 'CameraRecordings')
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)

        # Initialize the recording time tracking
        self.start_time = datetime.now()

        # VideoWriter setup
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = self.create_video_writer()

        # Start the frame update thread
        self.thread = Thread(target=self.update_frame, args=())
        self.thread.start()

        # Start the prediction sending thread
        self.prediction_thread = Thread(target=self.send_predictions, args=())
        self.prediction_thread.start()

        # Start the old recordings management thread
        self.old_recordings_thread = Thread(target=self.manage_old_recordings, args=())
        self.old_recordings_thread.start()

    def create_video_writer(self):
        video_file = os.path.join(self.video_dir, f'output_{self.camera_id}_{self.start_time.strftime("%Y-%m-%d_%H-%M-%S")}.avi')
        return cv2.VideoWriter(video_file, self.fourcc, self.fps, (self.frame_width, self.frame_height))

    def manage_old_recordings(self):
        while self.running:
            now = datetime.now()
            if (now - self.start_time).days >= 1:
                with self.lock:
                    self.out.release()  # Close the current video file
                    self.delete_old_videos()  # Delete old videos
                    self.start_time = now
                    self.out = self.create_video_writer()  # Create a new video writer
              # Check once an hour

    def delete_old_videos(self):
        for filename in os.listdir(self.video_dir):
            file_path = os.path.join(self.video_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def release(self):
        self.running = False
        print("running is set to False")
        if self.cap.isOpened():
            print("cam is open")
            self.thread.join()
            print("thread ended")
            self.prediction_thread.join()
            print("prediction thread ended")
            self.old_recordings_thread.join()
            print("rec thred ended")
            self.cap.release()
            print("camera is released")
            
            cv2.destroyAllWindows()

    def __del__(self):
        self.release()

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                if ret:
                    self.frame = frame
                    self.out.write(frame)  # Write the frame to the video file

                    # Apply face detection and recognition
                    detections = self.frame_processor.face_process(self.frame, self.camera_id)
                    self.processed_frame = draw_face_detections(self.frame.copy(), self.frame_processor, detections)
                else:
                    self.frame = None
                    self.processed_frame = None

    async def get_frame(self):
        with self.lock:
            if self.processed_frame is None:
                return None  # Return early if frame is None

            # Encode frame as JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]  # Adjust quality value (0-100) as needed
            _, buffer = cv2.imencode('.jpg', self.processed_frame, encode_param)
            frame_bytes = buffer.tobytes()
            return frame_bytes

    # def send_predictions(self):
    #     channel_layer = get_channel_layer()
    #     token = get_access_token()
    #     print(token)
    #     predictions = 0

    #     url = "https://fcm.googleapis.com/v1/projects/watch-3e30d/messages:send"
    #     headers = {
    #         "Authorization": f"Bearer {token}",
    #     }
    #     data = {
    #         "message": {
    #             "token": "hereisToken",
    #             "notification": {
    #                 "body": "This is another FCM notification message!",
    #                 "title": "FCM Message"
    #             }
    #         }
    #     }
        
    #     while self.running:
    #         if self.frame_processor.get_predictions():
    #             predictions += 1
    #         if predictions >= 5:
    #             token = getDevToken()
    #             data["message"]["token"] = token
    #             response = requests.post(url, headers=headers, json=data)
    #             print("FCM: " + str(response.status_code))
    #             async_to_sync(channel_layer.group_send)(
    #                 'notifications',
    #                 {
    #                     'type': 'send_notification',
    #                     'message': "Ma Chudao!"
    #                 }
    #             )
    #             predictions = 0
    #         time.sleep(1)
    
    def send_predictions(self):
        channel_layer = get_channel_layer()
        token = get_access_token()
        print(token)
        predictions = 0

        url = "https://fcm.googleapis.com/v1/projects/watch-3e30d/messages:send"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        data = {
            "message": {
                "token": "hereisToken",
                "notification": {
                    "body": "This is another FCM notification message!",
                    "title": "FCM Message"
                }
            }
        }
        
        while self.running:
            if self.frame_processor.get_predictions():
                predictions += 1
            if predictions >= 5:
                for token in GetListofToken():
                    data["message"]["token"] = token
                    response = requests.post(url, headers=headers, json=data)
                    print("FCM: " + str(response.status_code))
                predictions = 0
            time.sleep(1)
