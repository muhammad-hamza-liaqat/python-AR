import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()


def convert_uploaded_file_to_data_uri(file):
    mime_type = "image/png" if file.name.lower().endswith(".png") else "image/jpeg"
    file_content = file.read()
    encoded_string = base64.b64encode(file_content).decode("utf-8")
    file.seek(0)

    return f"data:{mime_type};base64,{encoded_string}"


def convert_image_to_3d(image_url_or_data_uri):
    url = os.getenv("MESHY_AI_IMAGE_TO_3D_URL")
    api_key = os.getenv("MESHY_AI_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "image_url": image_url_or_data_uri,
        "enable_pbr": True,
        "should_remesh": True,
        "should_texture": True,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        error_message = response.text if response else str(http_err)
        raise Exception(f"Error communicating with Meshy.ai: {error_message}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Network error occurred: {req_err}")


def fetch_3d_model(model_id):
    url = f"{os.getenv('MESHY_AI_IMAGE_TO_3D_URL')}/{model_id}"
    api_key = os.getenv("MESHY_AI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching 3D model details: {str(e)}")