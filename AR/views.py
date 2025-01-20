import os
import requests
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

class MeshyAIResultIDView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    AUTHORIZATION_KEY = os.getenv("MESHY_API_KEY")  

    def post(self, request):
        image_file = request.FILES.get("image") 
        enable_pbr = request.data.get("enable_pbr", "true").lower() == "true"
        should_remesh = request.data.get("should_remesh", "true").lower() == "true"
        should_texture = request.data.get("should_texture", "true").lower() == "true"

        if not image_file:
            return Response({"error": "Image file is required."}, status=status.HTTP_400_BAD_REQUEST)

        file_content = image_file.read()
        encoded_image = base64.b64encode(file_content).decode("utf-8")
        data_uri = f"data:{image_file.content_type};base64,{encoded_image}"

        payload = {
            "image_url": data_uri,
            "enable_pbr": enable_pbr,
            "should_remesh": should_remesh,
            "should_texture": should_texture,
        }

        headers = {
            "Authorization": f"Bearer {self.AUTHORIZATION_KEY}",
        }

        try:
            response = requests.post(
                "https://api.meshy.ai/openapi/v1/image-to-3d",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()  
            result_id = response.json().get("result")

            if not result_id:
                return Response({"error": "Result ID not found in response."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"result_id": result_id}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeshyAIDownloadView(APIView):
    """Handles downloading the .glb file using the result_id."""
    AUTHORIZATION_KEY = os.getenv("MESHY_API_KEY")  

    def get(self, request, result_id):
        headers = {
            "Authorization": f"Bearer {self.AUTHORIZATION_KEY}",
        }

        try:
            download_url = f"https://api.meshy.ai/openapi/v1/image-to-3d/{result_id}"

            response = requests.get(download_url, headers=headers)
            response.raise_for_status()

            data = response.json()

            model_url = data.get("model_urls", {}).get("glb")
            if not model_url:
                return Response({"error": "GLB model URL not found."}, status=status.HTTP_404_NOT_FOUND)

            file_response = requests.get(model_url, stream=True)
            file_response.raise_for_status()

            file_name = f"{result_id}.glb"  
            save_path = os.path.join(settings.MEDIA_ROOT, "3DModel", file_name)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)  

            with open(save_path, "wb") as file:
                for chunk in file_response.iter_content(chunk_size=8192):
                    file.write(chunk)

            return Response({"message": "File downloaded successfully.", "file_path": save_path}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)