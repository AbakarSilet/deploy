from django.urls import path
from .views import upload_media,home

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_media, name='upload_media'),
]