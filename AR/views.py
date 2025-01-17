from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from .helpers import process_video, create_named_folders
import os

class UploadAndProcessVideoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided in the request"}, status=400)

        video_folder = create_named_folders("Assets/temp_videos", file.name)
        frames_folder = create_named_folders("Assets/frames", file.name)
        models_folder = create_named_folders("Assets/models", file.name)

        video_path = os.path.join(video_folder, file.name)
        with open(video_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        model_path = process_video(video_path, frames_folder, models_folder)

        if os.path.exists(model_path):
            return FileResponse(open(model_path, 'rb'), content_type='application/octet-stream')

        return Response({"error": "3D model generation failed"}, status=500)
