# import cv2
# from threading import Thread, Lock
# from detector import FrameProcessor, draw_face_detections
# import asyncio
# import json
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import time

# class VideoCamera:
#     def __init__(self, src, camera_id):
#         self.cap = cv2.VideoCapture(src)
#         self.lock = Lock()
#         self.frame = None
#         self.running = True
#         self.frame_processor = FrameProcessor()
#         self.camera_id = camera_id

#         # Start the frame update thread
#         self.thread = Thread(target=self.update_frame, args=())
#         self.thread.start()

#         # Start the prediction sending thread
#         # self.prediction_thread = Thread(target=self.send_predictions, args=())
#         # self.prediction_thread.start()

#     def release(self):
#         if self.cap.isOpened():
#             self.thread.join()
#             self.prediction_thread.join()
#             self.cap.release()
#             cv2.destroyAllWindows()

#     def __del__(self):
#         self.running = False
#         self.thread.join()
#         self.prediction_thread.join()
#         self.cap.release()

#     def update_frame(self):
#         while self.running:
#             ret, frame = self.cap.read()
#             with self.lock:
#                 if ret:
#                     self.frame = frame
#                 else:
#                     self.frame = None

#     async def get_frame(self):
#         with self.lock:
#             if self.frame is None:
#                 return None  # Return early if frame is None

#             frame_copy = self.frame.copy()

#         # Apply face detection and recognition
#         detections = self.frame_processor.face_process(frame_copy, self.camera_id)
#         frame_copy = draw_face_detections(frame_copy, self.frame_processor, detections)

#         # Encode frame as JPEG
#         encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]  # Adjust quality value (0-100) as needed
#         _, buffer = cv2.imencode('.jpg', frame_copy, encode_param)
#         frame_bytes = buffer.tobytes()
#         return frame_bytes

#     # def send_predictions(self):
#     #     channel_layer = get_channel_layer()
#     #     while self.running:
#     #         predictions = self.frame_processor.get_predictions()
#     #         for prediction in predictions:
#     #             async_to_sync(channel_layer.group_send)(
#     #                 'notifications',
#     #                 {
#     #                     'type': 'send_notification',
#     #                     'message': prediction
#     #                   }
#     #             )
#     #         time.sleep(1)
import cv2
from threading import Thread, Lock
from .detector import FrameProcessor, draw_face_detections
import asyncio
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

class VideoCamera:
    def __init__(self, src, camera_id):
        self.cap = cv2.VideoCapture(src)
        self.lock = Lock()
        self.frame = None
        self.running = True
        self.frame_processor = FrameProcessor()
        self.camera_id = camera_id

        # Start the frame update thread
        self.thread = Thread(target=self.update_frame, args=())
        self.thread.start()

        # Start the prediction sending thread
        self.prediction_thread = Thread(target=self.send_predictions, args=())
        self.prediction_thread.start()

    def release(self):
        self.running = False
        if self.cap.isOpened():
            self.thread.join()
            self.prediction_thread.join()
            self.cap.release()
            cv2.destroyAllWindows()

    def __del__(self):
        self.release()

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                if ret:
                    self.frame = frame
                else:
                    self.frame = None

    async def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None  # Return early if frame is None

            frame_copy = self.frame.copy()

        # Apply face detection and recognition
        detections = self.frame_processor.face_process(frame_copy, self.camera_id)
        frame_copy = draw_face_detections(frame_copy, self.frame_processor, detections)

        # Encode frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]  # Adjust quality value (0-100) as needed
        _, buffer = cv2.imencode('.jpg', frame_copy, encode_param)
        frame_bytes = buffer.tobytes()
        return frame_bytes

    def send_predictions(self):
        channel_layer = get_channel_layer()
        while self.running:
            predictions = self.frame_processor.get_predictions()
            for prediction in predictions:
                async_to_sync(channel_layer.group_send)(
                    'notifications',
                    {
                        'type': 'send_notification',
                        'message': prediction
                    }
                )
            time.sleep(1)

