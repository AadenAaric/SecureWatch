# shared_middlewares/authentication.py
from General.models import ActiveUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from asgiref.sync import sync_to_async

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        return self.auth_without_camera_id(request, *args, **kwargs)

    async def auth_with_camera_id(self, request, *args, **kwargs):
        hashed_id = request.headers.get("id")
        camera_id = kwargs.get("camera_id")

        if hashed_id:
            try:
                user = await sync_to_async(ActiveUser.objects.get)(hashed_id=hashed_id)
                if user:
                    request.user = user
                    return await self.get_response(request, camera_id=camera_id)
            except ActiveUser.DoesNotExist:
                response = Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
    def auth_without_camera_id(self, request, *args, **kwargs):
        hashed_id = request.headers.get("id")

        if hashed_id:
            try:
                user = ActiveUser.objects.get(hashed_id=hashed_id)
                if user:
                    # Assign the user object to the request for later use if needed
                    request.user = user
                    # Return response without camera_id
                    return self.get_response(request)
            except ActiveUser.DoesNotExist:
                response = Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response

        # Return an unauthorized response if no valid user is found
        response = Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response
