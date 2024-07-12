
import logging as log
from time import perf_counter, time
import cv2
from openvino.runtime import Core, get_version
import dlib
from .landmarks_detector import LandmarksDetector
from .face_detector import FaceDetector
from .faces_database import FacesDatabase
from .face_identifier import FaceIdentifier
from .model_api.performance_metrics import PerformanceMetrics
import requests

source = (0)
device = "CPU"

faceDETECT = "model_2022_3/face-detection-retail-0005.xml"
faceLANDMARK = "model_2022_3/landmarks-regression-retail-0009.xml"
faceIDENTIFY = "model_2022_3/face-reidentification-retail-0095.xml"
alert_url = "http://your.api/alert"  # Replace with your actual API endpoint

class FrameProcessor:
    QUEUE_SIZE = 16

    def __init__(self):
        log.info('OpenVINO Runtime')
        log.info('build: {}'.format(get_version()))
        core = Core()

        self.face_detector = FaceDetector(core, faceDETECT, input_size=(0, 0), confidence_threshold=0.6)
        self.landmarks_detector = LandmarksDetector(core, faceLANDMARK)
        self.face_identifier = FaceIdentifier(core, faceIDENTIFY, match_threshold=0.7, match_algo='HUNGARIAN')
        self.face_detector.deploy(device)
        self.landmarks_detector.deploy(device, self.QUEUE_SIZE)
        self.face_identifier.deploy(device, self.QUEUE_SIZE)
        self.faces_database = FacesDatabase('../../face_img', self.face_identifier, self.landmarks_detector)
        self.face_identifier.set_faces_database(self.faces_database)
        log.info('Database is built, registered {} identities.'.format(len(self.faces_database)))

    def face_process(self, frame):
        rois = self.face_detector.infer((frame,))
        if self.QUEUE_SIZE > len(rois):
            rois = rois[:self.QUEUE_SIZE]
        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))
        return [rois, landmarks, face_identities]

def draw_face_detections(frame, frame_processor, detections, face_trackers, face_names, unknown_times):
    size = frame.shape[:2]
    current_trackers = {}
    current_time = time()

    for roi, landmarks, identity in zip(*detections):
        text = frame_processor.face_identifier.get_identity_label(identity.id)
        xmin = max(int(roi.position[0]), 0)
        ymin = max(int(roi.position[1]), 0)
        xmax = min(int(roi.position[0] + roi.size[0]), size[1])
        ymax = min(int(roi.position[1] + roi.size[1]), size[0])

        # Draw rectangle and landmarks
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 220, 0), 2)
        for point in landmarks:
            x = int(xmin + roi.size[0] * point[0])
            y = int(ymin + roi.size[1] * point[1])
            cv2.circle(frame, (x, y), 1, (0, 255, 255), 2)

        # Create or update tracker
        tracker = dlib.correlation_tracker()
        tracker.start_track(frame, dlib.rectangle(xmin, ymin, xmax, ymax))
        current_trackers[identity.id] = tracker

        # Set face name and track unknown durations
        if identity.id != FaceIdentifier.UNKNOWN_ID and (1 - identity.distance) > 0.75:
            face_names[identity.id] = text
            if identity.id in unknown_times:
                del unknown_times[identity.id]
        else:
            face_names[identity.id] = "Unknown"
            if identity.id not in unknown_times:
                unknown_times[identity.id] = current_time
            elif current_time - unknown_times[identity.id] > 10:  # 10 seconds threshold
                send_alert(identity.id, frame)
                unknown_times[identity.id] = current_time  # Reset the timer after sending an alert



    # Update face trackers and names
    face_trackers.clear()
    face_trackers.update(current_trackers)

    # Draw tracked faces
    for fid, tracker in face_trackers.items():
        tracked_position = tracker.get_position()
        t_x = int(tracked_position.left())
        t_y = int(tracked_position.top())
        t_w = int(tracked_position.width())
        t_h = int(tracked_position.height())

        cv2.rectangle(frame, (t_x, t_y), (t_x + t_w, t_y + t_h), (0, 0, 255), 2)
        if fid in face_names:
            cv2.putText(frame, face_names[fid], (t_x, t_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame

def draw_face_label(frame, text, identity, face_point, threshold):
    xmin, ymin = face_point
    if identity.id != FaceIdentifier.UNKNOWN_ID:
        if (1 - identity.distance) > threshold:
            pass
        else:
            textsize = cv2.getTextSize("Unknown", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
            cv2.rectangle(frame, (xmin, ymin), (xmin + textsize[0], ymin - textsize[1]), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, "Unknown", (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)

def send_alert(identity_id, frame):
    alert_data = {
        "identity_id": identity_id,
        "timestamp": time()
    }
    #response = requests.post(alert_url, json=alert_data)
    if True:
        print(f"There is Someone Unknown Outside")
    else:
        print(f"Failed to send alert for identity {identity_id}.")

def yield_predictions():
    cap = cv2.VideoCapture(source)
    metrics = PerformanceMetrics()
    frame_processor = FrameProcessor()
    face_trackers = {}
    face_names = {}
    unknown_times = {}

    while True:
        start_time = perf_counter()
        ret, frame = cap.read()
        if not ret:
            break

        detections = frame_processor.face_process(frame)
        frame = draw_face_detections(frame, frame_processor, detections, face_trackers, face_names, unknown_times)
        metrics.update(start_time, frame)
        cv2.imshow("face recognition demo", frame)
        key = cv2.waitKey(1)
        if key in (ord('q'), ord('Q'), 27):
            break

    cap.release()
    cv2.destroyAllWindows()


