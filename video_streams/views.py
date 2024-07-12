from django.http import StreamingHttpResponse
from django.utils.decorators import async_only_middleware
from AI.CAMERA import VideoCamera
import asyncio
#Initialize a single VideoCamera instance

cameras = [0]
camera_instances = {}
camera_instances = {cameras.index(i): VideoCamera(i,cameras.index(i)) for i in cameras}


async  def gen(camera):
    while True:
        frame_bytes = await camera.get_frame()
        if frame_bytes is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        await asyncio.sleep(0.1)  # Adjust the delay for your needs



class AsyncStreamingHttpResponse(StreamingHttpResponse):
    async def __aiter__(self):
        async for item in self.streaming_content:
            yield item


@async_only_middleware
async def video_feed(request,camera_id):
    cam = camera_instances[int(camera_id)]
    response = AsyncStreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace; boundary=frame')
    response.streaming = True
    return response
    