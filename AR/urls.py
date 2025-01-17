from django.urls import path
from .views import UploadAndProcessVideoView

urlpatterns = [
    path('upload-and-process/', UploadAndProcessVideoView.as_view(), name='upload-and-process'),
]
