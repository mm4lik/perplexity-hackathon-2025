import os
import requests
import json

def analyze_text(text, timeout=30):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
You are an expert in deception detection. Analyze the following text for signs of deception, manipulation, or psychological persuasion.

- Give a deception risk score (0–100).
- List the specific linguistic or psychological cues found (e.g., urgent language, vagueness, emotional manipulation).
- Provide a plain-language summary for a non-technical user.

Output as JSON with keys: risk_score, cues, summary.

TEXT:
{text}
"""
    data = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are a deception detection expert."},
            {"role": "user", "content": prompt}
        ]
    }
    url = "https://api.perplexity.ai/chat/completions"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        if response.status_code == 200:
            llm_content = response.json()['choices'][0]['message']['content']
            return json.loads(llm_content)
    except Exception as e:
        print("Deception API error:", e)
    return None
