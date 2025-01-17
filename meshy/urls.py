from django.urls import path
from .views import ImageTo3DView, Download3DModelView

urlpatterns = [
    path("image-to-3d/", ImageTo3DView.as_view(), name="image-to-3d"),
    path("download/<str:model_id>/", Download3DModelView.as_view(), name="download-3d-model"),
]
