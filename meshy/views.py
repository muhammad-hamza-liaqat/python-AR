from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import convert_image_to_3d, convert_uploaded_file_to_data_uri, fetch_3d_model
import requests
from django.http import JsonResponse
import os
from rest_framework import status

class ImageTo3DView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            image_file = request.FILES.get("file")
            if not image_file:
                return Response({"error": "No image file provided"}, status=400)

            if not image_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
                return Response(
                    {"error": "Unsupported file format. Only JPEG and PNG are allowed."},
                    status=400,
                )

            data_uri = convert_uploaded_file_to_data_uri(image_file)

            response = convert_image_to_3d(data_uri)

            return Response(
                {
                    "message": "Image successfully converted to 3D",
                    "result": response,
                }
            )
        except Exception as e:
            return Response({"error": f"Internal Server Error: {str(e)}"}, status=500)
        


class Download3DModelView(APIView):
    def get(self, request, model_id, *args, **kwargs):
        try:
            file_format = "glb"
            model_response = fetch_3d_model(model_id)
            model_urls = model_response.get("model_urls", {})
            download_url = model_urls.get(file_format)

            if not download_url:
                return Response({"error": f"File format {file_format.upper()} not available for this model."}, status=status.HTTP_404_NOT_FOUND)

            with requests.get(download_url, stream=True) as file_response:
                file_response.raise_for_status()

                file_dir = os.path.join("media", "3d_models")
                os.makedirs(file_dir, exist_ok=True)
                file_path = os.path.join(file_dir, f"{model_id}.{file_format}")

                with open(file_path, "wb") as f:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        f.write(chunk)

                return JsonResponse({"status": 201 ,"message": "File downloaded successfully", "file_path": file_path}, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch the 3D model: {str(e)}"}, status=500)
        except Exception as e:
            return Response({"error": f"Internal Server Error: {str(e)}"}, status=500)