from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("receive_audio/", views.receive_audio, name="audio_receiver"),
    path("receive_text/", views.receive_text, name="text_receiver"),
]
