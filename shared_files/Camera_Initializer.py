from General.models import Devices
from AI.CAMERA import VideoCamera
camera_instances = {}

print("camera initialized!")

def initialize_cameras():
    global camera_instances
    dev = Devices()
    cameras = dev.get_Devices()  # Assuming this returns a dictionary

    # Convert values with a single character to int
    for key, value in cameras.items():
        if len(str(value)) == 1:
            cameras[key] = int(value)

    # Create new camera instances
    try:
        camera_instances = {key: VideoCamera(cameras[key], key) for key in cameras}
        print("cameras initialized!")
        print(camera_instances)
    except Exception as e:
        print(f"Error initializing cameras: {e}")


def addCam(key,value):
    global camera_instances
    if value.isdigit():
        value = int(value)
    camera_instances[key] = VideoCamera(value,key)

    
def get_instances():
    global camera_instances
    return camera_instances

def rel(camera_id):
    if camera_id in camera_instances:
        camera_instances[camera_id].release()  # Release the camera resource
        del camera_instances[camera_id]  # Delete the instance from the dictionary
       
    else:
        print(f"Camera ID {camera_id} not found.")
    

initialize_cameras()