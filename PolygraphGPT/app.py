from flask import Flask, request, jsonify, render_template
import os
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
@app.route('/deception-detection', methods=['GET', 'POST'])
def deception_detection():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        result = deception.detect_deception(text)
        return jsonify({'result': result})
    return render_template('deception.html')
#--------------------------------------------------------------------------------------------------------
@app.route('/attribution', methods=['GET', 'POST'])
def attribution_route():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            text = data.get('text')
        except Exception as e:
            return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        result = attribution.attribute_text(text)
        return jsonify(result)

    return render_template('attribution.html')

#------------------------------------------------------------------------------
from modules import linguistic  # make sure this import works

@app.route('/linguistic-forensics', methods=['GET', 'POST'])
def linguistic_forensics():
    if request.method == 'POST':
        # Use request.get_json() if frontend sends JSON, or request.form for form data
        if request.is_json:
            data = request.get_json()
            text = data.get('text') if data else None
        else:
            text = request.form.get('text')

        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = linguistic.analyze_text(text)
        return jsonify(result)  # return JSON result directly (not nested)

    # GET request - render the form page
    return render_template('linguistic.html')

#----------------------------------------------------------------------------------------------------------------------------
@app.route('/deepfake-detection', methods=['GET', 'POST'])
def deepfake_detection():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        result = deepfake.detect_deepfake(file)
        return jsonify({'result': result})
    return render_template('deepfake.html')


from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Save file metadata to DB
    uploaded_file = UploadedFile(filename=filename)
    db.session.add(uploaded_file)
    db.session.commit()

    return jsonify({'message': 'File uploaded', 'filename': filename}), 201

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

    data = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are a troubleshooting assistant."},
            {"role": "user", "content": f"What are common fixes for: '{user_issue}'?"}
        ]
    }

    url = "https://api.perplexity.ai/chat/completions"

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            return jsonify({
                "success": True,
                "answer": answer,
                "follow_up": "Did that fix it?"
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

