import os
import uuid
import cv2
from openvino.runtime import Core, get_version
from face_detector import FaceDetector  # Assuming you have a FaceDetector class

# Global variables for paths and settings
source = 0
device = "CPU"
faceDETECT = "model_2022_3/face-detection-retail-0005.xml"
save_folder = "captured"

class FrameProcessor:
    QUEUE_SIZE = 16

    def __init__(self):
        core = Core()
        self.face_detector = FaceDetector(core, faceDETECT, input_size=(0, 0), confidence_threshold=0.6)
        self.face_detector.deploy(device)

    def detect_and_save_faces(self, frame, person_name):
        rois = self.face_detector.infer((frame,))
        size = frame.shape[:2]

        for idx, roi in enumerate(rois):
            xmin = max(int(roi.position[0]), 0)
            ymin = max(int(roi.position[1]), 0)
            xmax = min(int(roi.position[0] + roi.size[0]), size[1])
            ymax = min(int(roi.position[1] + roi.size[1]), size[0])

            # Extract and save face image
            face_img = frame[ymin:ymax, xmin:xmax]
            save_path = os.path.join(save_folder, f"{person_name}-{uuid.uuid4().hex}.jpg")
            cv2.imwrite(save_path, face_img)

            print(f"Saved face image for {person_name} at: {save_path}")

def yield_predictions():
    cap = cv2.VideoCapture(source)
    frame_processor = FrameProcessor()

    # Create save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Input person's name
    person_name = input("Enter the person's name: ")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame to detect faces and save them
        frame_processor.detect_and_save_faces(frame, person_name)

        # Display frame or perform other operations
        cv2.imshow("Face Detection and Capture", frame)
        key = cv2.waitKey(1)
        if key in (ord('q'), ord('Q'), 27):
            break

    cap.release()
    cv2.destroyAllWindows()


