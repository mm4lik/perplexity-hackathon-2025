from flask import Flask, request, jsonify, render_template

from modules import deception, attribution, linguistic, deepfake

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/deception-detection', methods=['GET', 'POST'])
def deception_detection():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        result = deception.detect_deception(text)
        return jsonify({'result': result})
    return render_template('deception.html')

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

@app.route('/deepfake-detection', methods=['GET', 'POST'])
def deepfake_detection():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        result = deepfake.detect_deepfake(file)
        return jsonify({'result': result})
    return render_template('deepfake.html')

if __name__ == '__main__':
    app.run(debug=True)
