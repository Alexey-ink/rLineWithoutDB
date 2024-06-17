from django.urls import path
from . import views

urlpatterns = [
    path('<str:text>/', views.generate_video, name='generate_video'),
]
