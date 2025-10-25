from flask import Flask, render_template, request, jsonify
import re, math

app = Flask(__name__)

COMMON_PATTERNS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "letmein", "admin", "welcome", "iloveyou"
]

def char_classes(password):
    return {
        "lower": bool(re.search(r"[a-z]", password)),
        "upper": bool(re.search(r"[A-Z]", password)),
        "digits": bool(re.search(r"[0-9]", password)),
        "symbols": bool(re.search(r"[^\w\s]", password)),
    }

def estimate_pool_size(classes):
    size = 0
    if classes["lower"]: size += 26
    if classes["upper"]: size += 26
    if classes["digits"]: size += 10
    if classes["symbols"]: size += 32
    return size

def entropy_estimate(password):
    if not password:
        return 0.0
    classes = char_classes(password)
    pool = estimate_pool_size(classes)
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)

def basic_penalties(password):
    score = 0
    pw_lower = password.lower()
    for p in COMMON_PATTERNS:
        if p in pw_lower:
            score -= 20
    if re.search(r"(012|123|234|345|456|567|678|789)", pw_lower):
        score -= 10
    if re.search(r"(abc|bcd|cde|def)", pw_lower):
        score -= 10
    if re.search(r"(.)\1\1\1", password):
        score -= 10
    if len(password) < 6:
        score -= 20
    return score

def compute_score(password):
    entropy = entropy_estimate(password)
    base = entropy
    penalty = basic_penalties(password)
    raw = base + penalty
    normalized = max(0, min(100, int((raw / 80.0) * 100)))
    return normalized, entropy

def strength_label_and_color(score):
    if score < 20:
        return "Very Weak", "red"
    if score < 40:
        return "Weak", "orange"
    if score < 60:
        return "Moderate", "yellow"
    if score < 80:
        return "Strong", "lightgreen"
    return "Very Strong", "green"

def feedback(password):
    suggestions = []
    if len(password) < 12:
        suggestions.append("Use at least 12 characters.")
    classes = char_classes(password)
    if not classes["upper"]:
        suggestions.append("Add uppercase letters.")
    if not classes["lower"]:
        suggestions.append("Add lowercase letters.")
    if not classes["digits"]:
        suggestions.append("Include numbers (0–9).")
    if not classes["symbols"]:
        suggestions.append("Add symbols (!@#$%^&*).")
    if any(p in password.lower() for p in COMMON_PATTERNS):
        suggestions.append("Avoid common words or sequences.")
    if not suggestions:
        suggestions.append("Excellent! Strong password.")
    return suggestions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    password = data.get("password", "")
    score, entropy = compute_score(password)
    label, color = strength_label_and_color(score)
    suggestions = feedback(password)
    return jsonify({
        "score": score,
        "entropy": round(entropy, 1),
        "label": label,
        "color": color,
        "suggestions": suggestions
    })

if __name__ == "__main__":
    app.run(debug=True)
