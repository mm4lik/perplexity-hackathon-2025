import os
import requests

PPLX_API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = os.getenv("PERPLEXITY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def attribute_text(text):
    prompt = f"""You are a cybersecurity analyst. Based on the text below, analyze and attribute the cyber incident to a known threat actor if possible. 
    Provide rationale and known TTPs if applicable. 

    Incident:
    \"\"\"{text}\"\"\"
    """

    payload = {
    "model": "pplx-70b-chat",  # ✅ valid model
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7,
    "stream": False
}


    response = requests.post(PPLX_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        content = response.json()
        return {
            "response": content["choices"][0]["message"]["content"]
        }
    else:
        return {
            "error": response.text,
            "success": False
        }
