from django.urls import path
from .views import MeshyAIResultIDView, MeshyAIDownloadView

urlpatterns = [
    path("convert/", MeshyAIResultIDView.as_view(), name="generate_result_id"),
    path("download/<str:result_id>/", MeshyAIDownloadView.as_view(), name="download_3d_model"),
]
