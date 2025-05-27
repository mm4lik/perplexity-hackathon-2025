import os
import requests
import json as pyjson

def call_perplexity_deception_api(text, timeout=30):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
You are an expert deception detection analyst. Analyze the following message for signs of deception, manipulation, or fraud.

- Assign a risk score from 0 to 100.
- Assign a risk label: "Low Risk", "Moderate Risk", "Moderate-High Risk", or "Critical Risk".
- Classify the type of deception (e.g., Phishing, Advance-fee Fraud, Social Engineering, or None).
- List the specific suspicious cues found (e.g., too-good-to-be-true claim, urgent call to action, request for sensitive info, manipulative trust phrase, false secrecy, suspicious reassurance), and quote the relevant text.
- Provide a plain-language summary for a non-technical user.
- Give clear recommendations for the recipient based on risk level.
- Explain briefly why the message was flagged.
- Output a JSON object with keys: risk_score, risk_label, classification, cues (list), recommended_action (list), why_flagged (list), summary, message_analyzed.
- Respond ONLY with valid JSON and nothing else.

MESSAGE:
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
            try:
                return pyjson.loads(llm_content)
            except Exception as e:
                # Print the LLM output for debugging if not valid JSON
                print("LLM returned non-JSON:", llm_content)
        else:
            print("API call failed:", response.status_code, response.text)
    except Exception as e:
        print("Exception while calling API:", e)
    return None
