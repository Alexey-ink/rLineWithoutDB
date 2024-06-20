from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('generate_video/', generate_video, name='generate_video'),
    path('<str:text>/', generate_video, name='generate_video_with_text'),
]

