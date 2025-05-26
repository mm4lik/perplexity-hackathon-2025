import os
import requests
import re
from urllib.parse import urlparse
from linguistic_analyzer import analyze_text  # your previously created module

PPLX_API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = os.getenv("PERPLEXITY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def preprocess_for_attribution(text):
    analysis = analyze_text(text)
    return {
        "summary": analysis["body_summary"],
        "tone": analysis["tone"],
        "phishing_score": analysis["phishing_likelihood_percent"],
        "keywords": ", ".join(analysis["key_triggers"]),
        "spoof_indicators": ", ".join(analysis["spoof_indicators"]),
        "domains": ", ".join([urlparse(link).netloc for link in analysis["links"]])
    }

def build_prompt(text, features):
    return f"""
You are a cybersecurity threat intelligence expert. A suspicious message has been detected.
Analyze and attribute it to a known threat actor (e.g. APT28, Lazarus, FIN7) based on linguistic and behavioral patterns.

🧾 Raw Message:
\"\"\"{text}\"\"\"

🔍 Extracted Features:
- Summary: {features['summary']}
- Tone: {features['tone']}
- Phishing Likelihood: {features['phishing_score']}%
- Keywords: {features['keywords']}
- Spoof Indicators: {features['spoof_indicators']}
- Domains Found: {features['domains']}

If attribution is not possible, provide reasoning and list relevant TTPs.
"""

def attribute_text(text):
    features = preprocess_for_attribution(text)
    prompt = build_prompt(text, features)

    payload = {
        "model": "pplx-70b-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "stream": False
    }

    response = requests.post(PPLX_API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        content = response.json()
        return {
            "success": True,
            "attribution_analysis": content["choices"][0]["message"]["content"],
            "features_used": features
        }
    else:
        return {
            "success": False,
            "error": response.text
        }
