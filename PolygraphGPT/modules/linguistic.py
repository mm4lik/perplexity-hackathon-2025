import re
from urllib.parse import urlparse

PHISHING_PHRASES = [
    "verify your account", "urgent action required", "click here to update",
    "your account will be suspended", "confirm your password", "login to your account",
    "reset your password", "update your information", "sensitive information",
    "bank account", "security alert", "unusual activity", "limited time", "act now",
    "restore your account", "temporarily locked", "permanently suspended", "do not ignore this message",
    "confirm your identity", "permanently closed", "restore access", "24 hours"
]

SAFE_DOMAINS = [
    "paypal.com", "apple.com", "microsoft.com", "google.com", "amazon.com", "yourbank.com"
]

def extract_links(text):
    url_pattern = r'(https?://[^\s\)]+)'
    return re.findall(url_pattern, text)

def is_suspicious_domain(sender_email):
    match = re.search(r'@([A-Za-z0-9.-]+)', sender_email)
    if not match:
        return True
    domain = match.group(1).lower()
    if domain.startswith("www."):
        domain = domain[4:]
    for safe in SAFE_DOMAINS:
        if domain == safe:
            return False
        if domain.endswith(safe) and domain != safe:
            return True
    return True

def extract_header(text, header):
    pattern = re.compile(rf"{header}:(.*)", re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else None

def summarize_body(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    body_lines = [l for l in lines if not any(l.lower().startswith(h) for h in ['subject:', 'from:', 'to:', 'date:'])]
    return " ".join(body_lines[:2]) if body_lines else ""

def analyze_text(text):
    subject = extract_header(text, "Subject") or "(not found)"
    sender = extract_header(text, "From") or "(not found)"
    recipient = extract_header(text, "To") or "(not found)"
    date = extract_header(text, "Date") or "(not found)"

    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    avg_word_length = round(sum(len(w) for w in words) / max(word_count, 1), 2)
    unique_words = len(set(w.lower() for w in words))
    sentence_count = len(re.findall(r'[.!?]', text))

    lower_text = text.lower()
    red_flags = [phrase for phrase in PHISHING_PHRASES if phrase in lower_text]

    links = extract_links(text)
    suspicious_sender = is_suspicious_domain(sender)
    suspicious_links = [url for url in links if is_suspicious_domain(urlparse(url).netloc)]

    # QR code and attachment checks (placeholder)
    qr_found = "qr code" in lower_text or "scan this code" in lower_text
    attachment_found = "attachment" in lower_text or "attached file" in lower_text

    # Tone & sentiment (simple heuristic)
    tone = []
    if any(w in lower_text for w in ["urgent", "immediately", "action required", "24 hours", "do not ignore"]):
        tone.append("Urgent")
    if any(w in lower_text for w in ["suspended", "locked", "closed", "permanently"]):
        tone.append("Authoritative")
    if any(w in lower_text for w in ["avoid", "risk", "protect", "security", "threat"]):
        tone.append("Fear-driven")
    tone = ", ".join(set(tone)) if tone else "Neutral"

    spoof_indicators = []
    if suspicious_sender:
        spoof_indicators.append(f"Suspicious sender domain ({sender.split('@')[-1]}) mimics real institution.")
    if "dear customer" in lower_text or "valued customer" in lower_text:
        spoof_indicators.append('Missing personalisation (uses "Dear Customer").')
    if qr_found:
        spoof_indicators.append("Contains QR code (potential phishing vector).")
    if attachment_found:
        spoof_indicators.append("Contains attachment (potential phishing vector).")

    advanced = []
    if links:
        advanced.append("Links found in email.")
    if suspicious_links:
        advanced.append("Suspicious links detected.")

    advice = [
        "🛡️ Quarantine email.",
        "Notify user with warning banner.",
        "Auto-report to security team for threat intel.",
        "Log and tag in SIEM for future correlation.",
        "Add to training dataset for phishing ML model."
    ]

    # === Local risk scoring logic ===
    probability = 0
    if suspicious_sender:
        probability += 40
    probability += 8 * len(red_flags)
    if "dear customer" in lower_text or "valued customer" in lower_text:
        probability += 10
    if "password" in lower_text or "verify" in lower_text:
        probability += 8
    if links:
        probability += 10
    if len(red_flags) >= 3 or (suspicious_sender and len(red_flags) > 0):
        probability = max(probability, 90)
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

    return {
        "subject": subject,
        "sender": sender,
        "recipient": recipient,
        "date": date,
        "body_summary": summarize_body(text),
        "phishing_likelihood_percent": probability,
        "risk_label": risk_label,
        "risk_color": risk_color,
        "key_triggers": red_flags,
        "tone": tone,
        "spoof_indicators": spoof_indicators,
        "advanced": advanced,
        "advice": advice,
        "links": links,
        "suspicious_links": suspicious_links,
        "word_count": word_count,
        "unique_word_count": unique_words,
        "average_word_length": avg_word_length,
        "sentence_count": sentence_count
    }
