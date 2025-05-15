# modules/linguistic.py

def analyze_text(text):
    word_count = len(text.split())
    avg_word_length = sum(len(w) for w in text.split()) / max(word_count, 1)
    return {
        'word_count': word_count,
        'average_word_length': round(avg_word_length, 2)
    }
