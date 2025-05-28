import os
os.environ["CURL_CA_BUNDLE"] = ""  # SSL workaround

import requests

def test_huggingface_api():
    """Check if Hugging Face API is reachable."""
    api_url = "https://api-inference.huggingface.co/models/gpt2"
    api_key = os.getenv("HF_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        r = requests.get(api_url, headers=headers, timeout=10)
        return r.status_code in [200, 400, 403, 404]
    except Exception as e:
        return False

def analyze_image_huggingface(image_path):
    api_key = os.getenv("HF_API_KEY")
    model_id = "prithivMLmods/deepfake-detector-model-v1"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(image_path, "rb") as img_file:
        response = requests.post(api_url, headers=headers, files={"file": img_file}, timeout=60)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
