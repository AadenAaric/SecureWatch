from django.urls import path
from . import views
from shared_middlewares.authentication import AuthenticationMiddleware

urlpatterns = [
    path('<str:camera_id>', views.video_feed, name='video_feed'),
]
