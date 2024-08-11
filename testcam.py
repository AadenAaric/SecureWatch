import cv2

# Set the video source (0 is typically the default webcam, or you can provide an RTSP stream URL)
video_source = "rtsp://192.168.8.101:554"  # You can also replace this with 'rtsp://your_ip_camera_address' or a video file path

# Open the video capture
cap = cv2.VideoCapture(video_source)

# Check if the video source is opened successfully
if not cap.isOpened():
    print("Error: Cannot open video source")
    exit()

# Loop to continuously get frames from the video source
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret will be True
    if not ret:
        print("Error: Cannot read frame")
        break

    # Display the resulting frame
    cv2.imshow('Video Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
