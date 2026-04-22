from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def normalize_attendance(attendance):
    if attendance > 85:
        return 0, []
    elif attendance >= 60:
        return 0.5, ["Moderate attendance"]
    else:
        return 1, ["Low attendance"]


def normalize_assignment(assignment):
    if assignment <= 3:
        return 0, []
    elif assignment <= 7:
        return 0.5, ["Moderate workload"]
    else:
        return 1, ["High workload"]


def normalize_sleep(sleep):
    if sleep >= 7:
        return 0, []
    elif sleep >= 5:
        return 0.5, ["Less sleep"]
    else:
        return 1, ["Sleep deprivation"]


def analyze_mood(mood):
    negative_words = ["stress", "tired", "anxious", "depressed"]
    positive_words = ["happy", "good", "relaxed"]

    score = 0
    reasons = []

    for word in negative_words:
        if word in mood:
            score += 1

    for word in positive_words:
        if word in mood:
            score -= 1

    if score > 1:
        reasons.append("Negative mood detected")
        return 1, reasons
    elif score >= 0:
        return 0.5, reasons
    else:
        return 0, reasons


def calculate_risk(a, b, c, d):
    return (a * 0.25) + (b * 0.25) + (c * 0.30) + (d * 0.20)


def classify_risk(score):
    if score <= 0.3:
        return "LOW", "Maintain routine"
    elif score <= 0.6:
        return "MEDIUM", "Improve sleep and manage workload"
    else:
        return "HIGH", "Take breaks, reduce stress, seek support"


def get_nearby_doctors():
    return [
        ("Psychologist Near Me", "https://www.google.com/maps/search/psychologist+near+me"),
        ("Mental Health Clinic", "https://www.google.com/maps/search/mental+health+clinic+near+me"),
        ("General Physician", "https://www.google.com/maps/search/general+physician+near+me"),
        ("Counseling Center", "https://www.google.com/maps/search/student+counseling+center+near+me"),
        ("Hospital Nearby", "https://www.google.com/maps/search/hospital+near+me")
    ]


# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        attendance = int(request.form['attendance'])
        assignment = int(request.form['assignment'])
        sleep = float(request.form['sleep'])
        mood = request.form['mood'].lower()

        reasons = []

        # VALIDATION
        if attendance < 0 or attendance > 100:
            return render_template('index.html', error="Attendance must be 0-100")

        if assignment < 1 or assignment > 10:
            return render_template('index.html', error="Assignment must be 1-10")

        if sleep < 0 or sleep > 24:
            return render_template('index.html', error="Sleep must be 0-24 hours")

        # NORMALIZATION
        a, r1 = normalize_attendance(attendance)
        b, r2 = normalize_assignment(assignment)
        c, r3 = normalize_sleep(sleep)
        d, r4 = analyze_mood(mood)

        reasons.extend(r1 + r2 + r3 + r4)

        # ADVANCED REASONING
        if sleep < 5:
            reasons.append("Critical sleep deprivation")

        if assignment > 8:
            reasons.append("Excessive academic workload")

        if attendance < 60:
            reasons.append("Very low attendance affecting performance")

        # RISK CALCULATION
        risk_score = calculate_risk(a, b, c, d)
        risk_percent = round(risk_score * 100, 2)

        # CLASSIFICATION
        risk, suggestion = classify_risk(risk_score)

        # DOCTOR FEATURE (FIXED POSITION)
        doctors = []
        if risk == "HIGH":
            doctors = get_nearby_doctors()

        return render_template(
            'index.html',
            risk_score=risk_percent,
            risk=risk,
            suggestion=suggestion,
            reasons=reasons,
            doctors=doctors
        )

    except Exception as e:
        return render_template('index.html', error="Invalid input or system error")


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)