import os
import requests

def call_perplexity_attribution_api(text, timeout=30):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
You are a cyber threat intelligence analyst. Given the suspicious message below, generate a detailed, Markdown-formatted attribution report for a security team.

**Your report MUST include:**
- Title: "🎯 Attribution Report"
- Message Subject, Sender, Timestamp
- Section 1: 🧩 Infrastructure Fingerprinting (domain, registrar, SSL, IP/geo, DNS)
- Section 2: 🧠 TTP Matching (language, tactics, phishing kit, campaign links)
- Section 3: 🧬 Attribution Signature (actor profile, motivation, historical links, codebase similarity)
- Section 4: 📍 Attribution Summary (as a Markdown table: Threat Actor, Region, Objective, Confidence, IoCs)
- Write in clear, professional Markdown with headings, bullet points, and tables.
- End with: "If you'd like, I can provide Indicators of Compromise (IoCs) from this sample and suggest countermeasures or integration points for threat feeds."

MESSAGE TO ATTRIBUTE:
{text}
"""

    data = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are a cyber threat attribution expert."},
            {"role": "user", "content": prompt}
        ]
    }
    url = "https://api.perplexity.ai/chat/completions"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        if response.status_code == 200:
            llm_content = response.json()['choices'][0]['message']['content']
            return llm_content
        else:
            print("API call failed:", response.status_code, response.text)
    except Exception as e:
        print("Exception while calling API:", e)
    return None
