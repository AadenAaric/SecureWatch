import cv2
import numpy as np
from .face_detector import FaceDetector
from .face_identifier import FaceIdentifier
from .landmarks_detector import LandmarksDetector
from .faces_database import FacesDatabase
import logging as log

class FaceRecognitionSystem:
    def __init__(self, face_detector, face_identifier, landmarks_detector, faces_database):
        self.face_detector = face_detector
        self.face_identifier = face_identifier
        self.landmarks_detector = landmarks_detector
        self.faces_database = faces_database
        self.tracker = cv2.TrackerKCF_create()
        self.tracked_faces = []

    def process_frame(self, frame):
        if len(self.tracked_faces) == 0:
            # Detect and recognize faces
            detected_faces = self.face_detector.infer(frame)
            for face in detected_faces:
                roi = [face]
                landmarks = self.landmarks_detector.infer((frame, roi))
                self.face_identifier.start_async(frame, roi, landmarks)
                descriptors = self.face_identifier.get_descriptors()
                matches = self.faces_database.match_faces(descriptors)
                
                for i, (identity, distance) in enumerate(matches):
                    if distance < self.face_identifier.get_threshold():
                        label = self.faces_database[identity].label
                    else:
                        label = "Unknown"
                    x, y, w, h = face.position[0], face.position[1], face.size[0], face.size[1]
                    self.tracked_faces.append((label, (x, y, w, h)))
                    self.tracker.init(frame, (x, y, w, h))
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        else:
            # Track faces
            success, boxes = self.tracker.update(frame)
            for i, (label, box) in enumerate(self.tracked_faces):
                if success:
                    x, y, w, h = [int(v) for v in box]
                    self.tracked_faces[i] = (label, (x, y, w, h))
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                else:
                    self.tracked_faces.pop(i)

        return frame

def main():
    # Initialize models
    model_path = "path/to/models"  # Update with the correct path to models
    face_detector = FaceDetector(f"{model_path}/face-detection-adas-0001.xml")
    face_identifier = FaceIdentifier(f"{model_path}/face-reidentification-retail-0095.xml")
    landmarks_detector = LandmarksDetector(f"{model_path}/landmarks-regression-retail-0009.xml")
    faces_database = FacesDatabase('path/to/faces_database', face_identifier, landmarks_detector, face_detector)

    face_recognition_system = FaceRecognitionSystem(face_detector, face_identifier, landmarks_detector, faces_database)

    cap = cv2.VideoCapture(0)  # Use 0 for webcam input

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = face_recognition_system.process_frame(frame)
        
        cv2.imshow('Face Recognition and Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()
