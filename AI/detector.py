import logging as log
from time import perf_counter
import cv2
from openvino.runtime import Core, get_version
from .landmarks_detector import LandmarksDetector
from .face_detector import FaceDetector
from .faces_database import FacesDatabase
from .face_identifier import FaceIdentifier
from .model_api.performance_metrics import PerformanceMetrics
from queue import Queue
from threading import Lock
from multipledispatch import dispatch
import numpy as np

device = "CPU"

import os

# Get the base directory (you can also import it from settings)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_dir = os.path.join(BASE_DIR, 'AI', 'model_2022_3')
faceDETECT = os.path.join(model_dir, 'face-detection-retail-0005.xml')
faceLANDMARK = os.path.join(model_dir, 'landmarks-regression-retail-0009.xml')
faceIDENTIFY = os.path.join(model_dir, 'face-reidentification-retail-0095.xml')

class FrameProcessor:
    QUEUE_SIZE = 16

    def __init__(self):
        log.info('OpenVINO Runtime')
        log.info('build: {}'.format(get_version()))
        core = Core()

        self.face_detector = FaceDetector(core, faceDETECT, input_size=(0, 0), confidence_threshold=0.6,)
        self.landmarks_detector = LandmarksDetector(core, faceLANDMARK)
        self.face_identifier = FaceIdentifier(core, faceIDENTIFY, match_threshold=0.7, match_algo='HUNGARIAN')
        self.face_detector.deploy(device)
        self.landmarks_detector.deploy(device, self.QUEUE_SIZE)
        self.face_identifier.deploy(device, self.QUEUE_SIZE)
        self.faces_database = FacesDatabase(os.path.join(BASE_DIR,'media','MiniApp_Images'), self.face_identifier, self.landmarks_detector)
        self.face_identifier.set_faces_database(self.faces_database)
        log.info('Database is built, registered {} identities.'.format(len(self.faces_database)))

        self.prediction_queue = Queue()
        self.lock = Lock()
    
    @dispatch(np.ndarray)
    def face_process(self, frame):
        rois = self.face_detector.infer((frame,))
        if self.QUEUE_SIZE > len(rois):
            rois = rois[:self.QUEUE_SIZE]
        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))
        return [rois, landmarks, face_identities]
    @dispatch(np.ndarray,int)
    def face_process(self, frame, camera_id):
        rois = self.face_detector.infer((frame,))
        if self.QUEUE_SIZE > len(rois):
            rois = rois[:self.QUEUE_SIZE]
        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))
        
        # Collect predictions and push them to the queue
        with self.lock:
            for roi, identity in zip(rois, face_identities):
                if identity.id != FaceIdentifier.UNKNOWN_ID:
                    if (1 - identity.distance) > 0.75:
                        prediction = {
                            'camera_id': camera_id,
                            'identity': self.face_identifier.get_identity_label(identity.id),
                            'confidence': 1 - identity.distance
                        }
                    else:
                         prediction = {
                            'camera_id': camera_id,
                            'identity': "Unknown",
                            'confidence': 1 - identity.distance
                        }      
                self.prediction_queue.put(prediction)

        return [rois, landmarks, face_identities]
    
    @dispatch(np.ndarray,str)
    def face_process(self, frame, camera_id):
        rois = self.face_detector.infer((frame,))
        if self.QUEUE_SIZE > len(rois):
            rois = rois[:self.QUEUE_SIZE]
        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))
        
        # Collect predictions and push them to the queue
        with self.lock:
            for roi, identity in zip(rois, face_identities):
                if identity.id != FaceIdentifier.UNKNOWN_ID:
                    if (1 - identity.distance) > 0.75:
                        prediction = {
                            'camera_id': camera_id,
                            'identity': self.face_identifier.get_identity_label(identity.id),
                            'confidence': 1 - identity.distance
                        }
                    else:
                         prediction = {
                            'camera_id': camera_id,
                            'identity': "Unknown",
                            'confidence': 1 - identity.distance
                        }      
                self.prediction_queue.put(prediction)

        return [rois, landmarks, face_identities]

    def get_predictions(self):
        predictions = []
        with self.lock:
            while not self.prediction_queue.empty():
                predictions.append(self.prediction_queue.get())
        return predictions

def draw_face_detections(frame, frame_processor, detections):
    size = frame.shape[:2]
    for roi, landmarks, identity in zip(*detections):
        if identity.id != FaceIdentifier.UNKNOWN_ID:
            text = frame_processor.face_identifier.get_identity_label(identity.id)
            xmin = max(int(roi.position[0]), 0)
            ymin = max(int(roi.position[1]), 0)
            xmax = min(int(roi.position[0] + roi.size[0]), size[1])
            ymax = min(int(roi.position[1] + roi.size[1]), size[0])
            face_point = (xmin, ymin)
            image_recognizer(frame, text, identity, face_point, 0.75)
    return frame

def image_recognizer(frame, text, identity, face_point, threshold):
    xmin, ymin = face_point
    if identity.id != FaceIdentifier.UNKNOWN_ID:
        if (1 - identity.distance) > threshold:
            textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
            cv2.putText(frame, text, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        else:
            textsize = cv2.getTextSize("Unknown", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
            cv2.putText(frame, "Unknown", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
