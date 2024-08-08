import os
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from detector import frame_processor
import numpy as np
import cv2

# Load images and their corresponding true identities
def load_images_and_labels(folder_path):
    images = []
    labels = []
    for identity_name in os.listdir(folder_path):
        identity_folder = os.path.join(folder_path, identity_name)
        if os.path.isdir(identity_folder):
            for image_name in os.listdir(identity_folder):
                image_path = os.path.join(identity_folder, image_name)
                image = cv2.imread(image_path)
                if image is not None:
                    images.append(image)
                    labels.append(identity_name)
    return images, labels

def evaluate_faces(frame_processor, images, true_labels):
    predicted_labels = []
    for image, true_label in zip(images, true_labels):
        detections = frame_processor.face_process(image)
        if detections[2]:  # Ensure there's at least one detection
            predicted_label = frame_processor.face_identifier.get_identity_label(detections[2][0].id)
            predicted_labels.append(predicted_label)
        else:
            predicted_labels.append('Unknown')
    return predicted_labels

# Load images and true labels
folder_path = 'face_img'
images, true_labels = load_images_and_labels(folder_path)

# Evaluate predictions
predicted_labels = evaluate_faces(frame_processor, images, true_labels)

# Generate confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=np.unique(true_labels + predicted_labels))
cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(true_labels + predicted_labels))
cm_display.plot()
cv2.waitKey(0)