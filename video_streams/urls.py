from django.urls import path
from . import views

urlpatterns = [
    path('<str:camera_id>', views.video_feed, name='video_feed'),
]
