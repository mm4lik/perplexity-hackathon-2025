from transformers import pipeline

# Load fake news detection model
deception_model = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")

# Label mapping: adjust depending on the model's labels
label_map = {
    "LABEL_0": "REAL",
    "LABEL_1": "FAKE"
}

def detect_deception(text):
    result = deception_model(text)[0]
    return {
        "label": label_map.get(result['label'], result['label']),
        "confidence": round(result['score'], 3)
    }
