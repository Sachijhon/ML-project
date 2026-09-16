from datetime import datetime
from io import BytesIO
import json
import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, redirect, render_template, request, send_file, session, url_for
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "rf_heart_model.pkl"
CREDENTIAL_FILE = BASE_DIR / "credentials.json"

app = Flask(__name__)
app.secret_key = os.getenv("CARDIOAI_SECRET_KEY", "development-only-change-me")

saved_data = joblib.load(MODEL_PATH)
MODEL = saved_data["model"]
FEATURE_NAMES = saved_data["feature_names"]

latest_report = {}


def get_credentials():
    """Load local credentials, creating a demo-only file when needed."""
    if not CREDENTIAL_FILE.exists():
        demo = {
            "email": os.getenv("CARDIOAI_DEMO_EMAIL", "doctor@cardioai.com"),
            "password": os.getenv("CARDIOAI_DEMO_PASSWORD", "CardioAI@123"),
        }
        CREDENTIAL_FILE.write_text(json.dumps(demo), encoding="utf-8")
    return json.loads(CREDENTIAL_FILE.read_text(encoding="utf-8"))


SECRET_CODE = os.getenv("CARDIOAI_SECRET_CODE", "CARDIOAI-DEMO")


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    creds = get_credentials()
    if email == creds["email"] and password == creds["password"]:
        session["user"] = email
        return redirect(url_for("home"))
    return render_template("login.html", error="Invalid email or password")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/verify-secret", methods=["POST"])
def verify_secret():
    email = request.form["email"]
    secret_code = request.form["secret_code"]
    creds = get_credentials()
    if email == creds["email"] and secret_code == SECRET_CODE:
        return render_template("forgot_password.html", verified=True, email=email)
    return render_template("forgot_password.html", error="Invalid email or secret code")


@app.route("/update-password", methods=["POST"])
def update_password():
    email = request.form["email"]
    new_password = request.form["new_password"]
    creds = get_credentials()
    if email == creds["email"]:
        creds["password"] = new_password
        CREDENTIAL_FILE.write_text(json.dumps(creds), encoding="utf-8")
        return render_template("login.html", error="Password updated successfully. Please log in.")
    return redirect(url_for("forgot_password"))


@app.route("/dashboard")
def home():
    if "user" not in session:
        return redirect(url_for("login_page"))
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login_page"))

    values = [
        int(request.form["age"]), int(request.form["sex"]), int(request.form["cp"]),
        int(request.form["trestbps"]), int(request.form["chol"]), int(request.form["fbs"]),
        int(request.form["restecg"]), int(request.form["thalach"]), int(request.form["exang"]),
        float(request.form["oldpeak"]), int(request.form["slope"]), int(request.form["ca"]),
        int(request.form["thal"]),
    ]

    input_df = pd.DataFrame([values], columns=FEATURE_NAMES)
    proba = MODEL.predict_proba(input_df)[0]
    hd_pct = round(float(proba[1]) * 100, 2)
    no_hd_pct = round(float(proba[0]) * 100, 2)

    if hd_pct >= 65:
        risk, advice = "HIGH RISK", "Immediate cardiology consultation recommended."
    elif hd_pct >= 40:
        risk, advice = "MODERATE RISK", "Further cardiovascular evaluation advised."
    else:
        risk, advice = "LOW RISK", "Routine monitoring recommended."

    factors = [name for name, flag in {
        "High Cholesterol": values[4] > 240,
        "High Blood Pressure": values[3] > 140,
        "Low Maximum Heart Rate": values[7] < 120,
        "Exercise Induced Angina": values[8] == 1,
        "Abnormal ECG": values[6] != 0,
        "Chest Pain Symptoms": values[2] > 0,
    }.items() if flag]
    if not factors:
        factors = ["No major risk contributors detected"]

    ai_summary = (
        "AI analysis indicates significantly elevated cardiovascular risk." if hd_pct >= 65
        else "AI analysis suggests moderate cardiovascular risk." if hd_pct >= 40
        else "AI analysis indicates low cardiovascular risk."
    )

    global latest_report
    latest_report = {
        "prediction": hd_pct, "no_prediction": no_hd_pct, "risk": risk,
        "advice": advice, "factors": factors, "ai_summary": ai_summary,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }
    return render_template("result.html", **latest_report)


@app.route("/download_report")
def download_report():
    if "user" not in session:
        return redirect(url_for("login_page"))
    if not latest_report:
        return redirect(url_for("home"))

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("CardioAI Heart Disease Risk Report")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(140, 800, "Heart Disease Risk Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Date: {latest_report['date']}")
    pdf.drawString(50, 720, f"Heart Disease Probability: {latest_report['prediction']}%")
    pdf.drawString(50, 690, f"No Disease Probability: {latest_report['no_prediction']}%")
    pdf.drawString(50, 660, f"Risk Level: {latest_report['risk']}")
    pdf.drawString(50, 630, f"Advice: {latest_report['advice']}")
    pdf.drawString(50, 600, "AI Summary:")
    pdf.drawString(70, 570, latest_report["ai_summary"][:95])
    pdf.drawString(50, 530, "Risk Factors:")
    y = 500
    for factor in latest_report["factors"]:
        pdf.drawString(70, y, f"- {factor}")
        y -= 25
    pdf.drawString(50, max(y - 10, 80), "Educational use only. Not a substitute for professional medical advice.")
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="CardioAI_Heart_Report.pdf", mimetype="application/pdf")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


@app.after_request
def add_security_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
