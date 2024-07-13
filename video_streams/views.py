from django.http import StreamingHttpResponse
from django.utils.decorators import async_only_middleware
from AI.CAMERA import VideoCamera
import asyncio
from django.utils.decorators import method_decorator
from shared_middlewares.authentication import AuthenticationMiddleware
from General.models import ActiveUser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from asgiref.sync import sync_to_async

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
async def video_feed(request, camera_id):
    hashed_id = request.headers.get("id")
    if hashed_id:
        try:
            user = await sync_to_async(ActiveUser.objects.get)(hashed_id=hashed_id)
            if user:
                cam = camera_instances[int(camera_id)]
                response =  AsyncStreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace; boundary=frame')
                response.streaming = True
                return response
        except ActiveUser.DoesNotExist:
            return JsonResponse({"error": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"error": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)