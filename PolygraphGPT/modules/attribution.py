import re

DECEPTIVE_PHRASES = [
    "trust me", "to be honest", "believe me", "confidential", "secret", "guarantee",
    "I assure you", "no lie", "I swear", "act now", "urgent", "immediately",
    "limited time", "exclusive offer", "don't tell anyone", "this is not a scam",
    "100% real", "winner", "selected", "prize", "reward", "send your details",
    "bank account", "password", "for your own good", "promise", "risk-free"
]

def extract_deceptive_phrases(text):
    lower_text = text.lower()
    return [phrase for phrase in DECEPTIVE_PHRASES if phrase in lower_text]

def analyze_text(text):
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    avg_word_length = round(sum(len(w) for w in words) / max(word_count, 1), 2)
    unique_words = len(set(w.lower() for w in words))
    sentence_count = len(re.findall(r'[.!?]', text))

    lower_text = text.lower()
    cues = extract_deceptive_phrases(text)

    # Tone & sentiment (simple heuristic)
    tone = []
    if any(w in lower_text for w in ["urgent", "immediately", "act now", "limited time"]):
        tone.append("Urgent")
    if any(w in lower_text for w in ["confidential", "secret", "don't tell anyone"]):
        tone.append("Secretive")
    if any(w in lower_text for w in ["promise", "guarantee", "trust me", "believe me"]):
        tone.append("Persuasive")
    if any(w in lower_text for w in ["winner", "prize", "reward", "selected"]):
        tone.append("Too-good-to-be-true")
    tone = ", ".join(set(tone)) if tone else "Neutral"

    # === Local risk scoring logic ===
    probability = 0
    probability += 10 * len(cues)
    if "bank account" in lower_text or "password" in lower_text:
        probability += 20
    if "winner" in lower_text or "prize" in lower_text or "reward" in lower_text:
        probability += 20
    if "confidential" in lower_text or "secret" in lower_text:
        probability += 10
    if "urgent" in lower_text or "immediately" in lower_text:
        probability += 10
    probability = min(probability, 100)
    probability = max(probability, 5)

    if probability > 75:
        risk_color = "red"
        risk_label = "High Risk"
    elif probability > 50:
        risk_color = "orange"
        risk_label = "Moderate-High Risk"
    elif probability > 25:
        risk_color = "yellow"
        risk_label = "Moderate Risk"
    else:
        risk_color = "green"
        risk_label = "Low Risk"

    summary = ""
    if probability >= 50:
        summary = "This message contains multiple cues commonly associated with deception or manipulation. Be very cautious."
    elif probability >= 25:
        summary = "Some deceptive or manipulative cues detected. Use caution and verify."
    else:
        summary = "No strong signs of deception detected, but always use caution with unexpected messages."

    return {
        "deception_likelihood_percent": probability,
        "risk_label": risk_label,
        "risk_color": risk_color,
        "cues": cues,
        "tone": tone,
        "summary": summary,
        "word_count": word_count,
        "unique_word_count": unique_words,
        "average_word_length": avg_word_length,
        "sentence_count": sentence_count
    }
