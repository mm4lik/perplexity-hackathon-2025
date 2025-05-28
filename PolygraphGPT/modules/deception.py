import os
import requests

def call_perplexity_deception_api(text, timeout=30):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Prompt for detailed, attribution-focused Markdown report
    prompt = f"""
You are an expert deception detection analyst and threat intelligence profiler. Given the following suspicious message, produce a detailed, attribution-focused Markdown report for a security analyst and a non-technical user.

Your report MUST include:
- A clear classification (e.g., High-Risk Phishing Attempt).
- A summary of the suspicious message (subject, sender, recipient, link, timestamp).
- A table of social engineering tactics used, with explanations.
- Technical analysis (e.g., domain age, hosting, simulated WHOIS, link analysis, sender IP, TLS cert).
- Attribution: Based on language, infrastructure, and tactics, suggest a likely threat actor or campaign (simulate if needed).
- Clear recommended actions for the recipient.
- An analyst note explaining the multi-layered deception.
- End with: "Would you like this exported as a JSON threat report, PDF brief, or live alert to your dashboard?"

Format your answer in Markdown with sections, tables, and bullet points as appropriate.

MESSAGE TO ANALYZE:
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
            # The LLM returns Markdown text
            return llm_content
        else:
            print("API call failed:", response.status_code, response.text)
    except Exception as e:
        print("Exception while calling API:", e)
    return None
