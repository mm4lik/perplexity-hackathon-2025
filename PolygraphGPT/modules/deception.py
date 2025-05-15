def detect_deception(text):
    suspicious_words = ['lie', 'false', 'fake', 'deceive']
    for word in suspicious_words:
        if word in text.lower():
            return "Deception suspected"
    return "No deception detected"
