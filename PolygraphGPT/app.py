from flask import Flask, request, jsonify, render_template
import os
import re
import threading
import requests
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file into environment
app = Flask(__name__)

API_KEY = os.getenv('PERPLEXITY_API_KEY')

from modules import deception, attribution, linguistic, deepfake



from flask_sqlalchemy import SQLAlchemy

# Setup SQLite DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polygraphgpt.db'  # SQLite file in your project folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import os
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # max 16MB upload

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


db = SQLAlchemy(app)

class ThreatActor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


@app.route('/add_threat_actor', methods=['POST'])
def add_threat_actor():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    existing = ThreatActor.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Threat actor already exists"}), 409

    actor = ThreatActor(name=name, description=description)
    db.session.add(actor)
    db.session.commit()

    return jsonify(actor.to_dict()), 201


@app.route('/threat_actors', methods=['GET'])
def get_threat_actors():
    actors = ThreatActor.query.all()
    return jsonify([actor.to_dict() for actor in actors])


@app.route('/')
def home():
    return render_template('home.html')
#---------------------------------------------------------------------------------------------
#deception

from modules import deception


@app.route('/deception-detection', methods=['GET', 'POST'])
def deception_detection():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            text = data.get('text') if data else None
        else:
            text = request.form.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        llm_result = {}

        def get_llm():
            nonlocal llm_result
            llm_result = deception.call_perplexity_deception_api(text, timeout=30)

        thread = threading.Thread(target=get_llm)
        thread.start()
        thread.join(timeout=30)  # 30 seconds max wait for LLM

        # Handle very short/trivial input
        if len(text.strip()) < 10:
            merged = {
                'risk_score': 10,
                'risk_color': "green",
                'risk_label': "Low Risk",
                'cues': ["Input is very short or incomplete, risk estimation is uncertain."],
                'recommended_action': [
                    "This input is too short for accurate analysis. Please provide more context.",
                    "Be cautious with unknown or incomplete messages."
                ],
                'why_flagged': ["Too little content to analyze for deception."],
                'summary': "The provided input is too short or lacks context for a reliable deception analysis. Please submit the full message for a more accurate assessment.",
                'classification': "None",
                'message_analyzed': text
            }
            return jsonify(merged)

        if llm_result:
            # Risk color mapping
            score = int(llm_result.get('risk_score', 0))
            if score >= 75:
                llm_result['risk_color'] = "red"
            elif score >= 50:
                llm_result['risk_color'] = "orange"
            elif score >= 25:
                llm_result['risk_color'] = "yellow"
            else:
                llm_result['risk_color'] = "green"
            return jsonify(llm_result)
        else:
            # Fallback error
            return jsonify({
                'risk_score': 0,
                'risk_color': "green",
                'risk_label': "Low Risk",
                'cues': [],
                'recommended_action': [],
                'why_flagged': ["Deception analysis failed. Please try again."],
                'summary': "Deception analysis failed. Please try again.",
                'classification': "None",
                'message_analyzed': text
            })
    return render_template('deception.html')




#------------------------------------------------------------------------------
#lingustic

from modules import linguistic

def call_perplexity_api(text, timeout=30):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
You are an expert cybersecurity analyst. Analyze the following email (headers and body) for phishing risk.

- Provide a risk score from 0 to 100.
- Provide a risk label: "Low Risk", "Moderate Risk", "Moderate-High Risk", or "Critical Risk".
- Tailor your recommendations based on the risk level:
  - For low risk: reassure the user and give cautious advice.
  - For moderate risk: advise caution and verification.
  - For high risk: advise quarantine, reporting, and no interaction.
- If the input is very short or lacks context (e.g., just a name or a few words), explain that risk estimation is uncertain and advise caution accordingly.
- Output a JSON with keys: risk_score, risk_label, why_flagged (list), recommended_action (list), summary (string).

EMAIL:
{text}
"""

    data = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are an advanced cybersecurity email analyzer."},
            {"role": "user", "content": prompt}
        ]
    }
    url = "https://api.perplexity.ai/chat/completions"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        if response.status_code == 200:
            import json as pyjson
            llm_content = response.json()['choices'][0]['message']['content']
            return pyjson.loads(llm_content)
    except Exception:
        pass
    return None

@app.route('/linguistic-forensics', methods=['GET', 'POST'])
def linguistic_forensics():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            text = data.get('text') if data else None
        else:
            text = request.form.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        local_result = linguistic.analyze_text(text)
        llm_result = {}

        # Run LLM in a thread for speed, with a timeout
        def get_llm():
            nonlocal llm_result
            llm_result = call_perplexity_api(text, timeout=30)

        thread = threading.Thread(target=get_llm)
        thread.start()
        thread.join(timeout=30)  # 30 seconds max wait for LLM

        merged = local_result.copy()

        # Handle very short/trivial input
        if len(text.strip()) < 10:
            merged['phishing_likelihood_percent'] = 20
            merged['risk_color'] = "green"
            merged['risk_label'] = "Low Risk"
            merged['why_flagged'] = [
                "Input is very short or incomplete, risk estimation is uncertain."
            ]
            merged['recommended_action'] = [
                "This input is too short for accurate analysis. Please provide the full email.",
                "Be cautious with unknown or incomplete messages."
            ]
            merged['summary'] = "The provided input is too short or lacks context for a reliable phishing analysis. Please submit the full email content for a more accurate assessment."
            return jsonify(merged)

        if llm_result:
            merged.update(llm_result)
            # Harmonize risk score/risk_label if present in LLM output
            if 'risk_score' in llm_result:
                merged['phishing_likelihood_percent'] = llm_result['risk_score']
            # Risk color mapping
            score = int(merged.get('phishing_likelihood_percent', 0))
            if score >= 75:
                merged['risk_color'] = "red"
                merged['risk_label'] = "Critical Risk"
            elif score >= 50:
                merged['risk_color'] = "orange"
                merged['risk_label'] = "Moderate-High Risk"
            elif score >= 25:
                merged['risk_color'] = "yellow"
                merged['risk_label'] = "Moderate Risk"
            else:
                merged['risk_color'] = "green"
                merged['risk_label'] = "Low Risk"
        else:
            # Always ensure a risk score is present (fallback)
            if not merged.get('phishing_likelihood_percent'):
                merged['phishing_likelihood_percent'] = local_result['phishing_likelihood_percent']
            score = int(merged.get('phishing_likelihood_percent', 0))
            if score >= 75:
                merged['risk_color'] = "red"
                merged['risk_label'] = "Critical Risk"
            elif score >= 50:
                merged['risk_color'] = "orange"
                merged['risk_label'] = "Moderate-High Risk"
            elif score >= 25:
                merged['risk_color'] = "yellow"
                merged['risk_label'] = "Moderate Risk"
            else:
                merged['risk_color'] = "green"
                merged['risk_label'] = "Low Risk"

        return jsonify(merged)
    return render_template('linguistic.html')

#---------------------------------------------------------------------------------------------------------
# testing perlexity 

import requests

import requests
from flask import jsonify

@app.route('/test-perplexity')
def test_perplexity():
    API_KEY = os.getenv('PERPLEXITY_API_KEY')

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "sonar-pro",  # 🔁 use this valid model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is cyber attribution?"}
        ]
    }

    url = "https://api.perplexity.ai/chat/completions"

    try:
        response = requests.post(url, headers=headers, json=data)

        print("API response status:", response.status_code)
        print("API response text:", response.text)

        if response.status_code == 200:
            return jsonify({"success": True, "response": response.json()}), 200
        else:
            return jsonify({"success": False, "error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#----------------------------------------------------------------------------------------------------
# chat bot 


# Helper to extract all markdown links ([text](url)) as URLs
def extract_markdown_links(markdown_text):
    return re.findall(r'\[.*?\]\((https?://[^\s)]+)\)', markdown_text)

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_issue = request.json.get('issue')

    if not user_issue:
        return jsonify({"error": "No issue provided"}), 400

    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        return jsonify({"error": "API key not found"}), 500

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Prompt instructs the model to give detailed, structured, sourced answers
    data = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": """
You are a cybersecurity troubleshooter who helps users solve technical issues step-by-step.
Provide detailed, structured responses with clear headings, bullet points, and a summary table.
Use recent discussions from Reddit, Microsoft forums, and official Apple support pages.
Include relevant links as markdown hyperlinks ([title](url)) when they’d help the user directly.
At the end, include a '### Citations' section with a bullet list of all sources used (as markdown links).
Talk like a person helping a friend fix their device.
Format responses exactly as shown below:

### Example Output Format

#### Introduction
Briefly describe the issue.

### Key Vulnerabilities
- Use bullet points for each vulnerability:
  - **Vulnerability Name (CVE-ID)**
    - Affected devices
    - Description
    - Impact

### Summary Table
| Vulnerability | Impact/Description | Patched in iOS |
|---------------|---------------------|---------------|
| CVE-1234      | Short description   | Version       |

### Recommendations
- Step-by-step instructions or advice.

### Citations
- Include sources like Reddit, Microsoft, or official Apple pages as markdown links.

Now, provide this format for: '{user_issue}'?
                """.replace("{user_issue}", user_issue)
            },
            {
                "role": "user",
                "content": f"What are common fixes for: '{user_issue}'?"
            }
        ]
    }

    url = "https://api.perplexity.ai/chat/completions"

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            citations = extract_markdown_links(answer)

            return jsonify({
                "success": True,
                "answer": answer,
                "citations": citations,
                "follow_up": "Did that help? If not, describe what's still happening."
            })
        else:
            return jsonify({
                "success": False,
                "error": f"API Error ({response.status_code}): {response.text}"
            }), response.status_code

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


#---------------------------------------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("Loaded API Key:", API_KEY)  # <-- move here
    
    app.run(debug=True)

