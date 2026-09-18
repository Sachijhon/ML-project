# ❤️ CardioAI — Heart Disease Risk Prediction System

### Machine Learning • Python • Flask • Random Forest

[![GitHub](https://img.shields.io/badge/GitHub-Sachijhon-181717?logo=github)](https://github.com/Sachijhon) [![Project](https://img.shields.io/badge/Portfolio-Featured-0A66C2)](https://github.com/Sachijhon/ML-project)

> A machine-learning powered clinical decision-support prototype built with **Random Forest, Flask, HTML/CSS, and ReportLab**.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Random Forest](https://img.shields.io/badge/Model-Random%20Forest-2E8B57)](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)
[![ReportLab](https://img.shields.io/badge/Reporting-ReportLab-8A2BE2)](https://www.reportlab.com/)
[![Project Status](https://img.shields.io/badge/Status-Academic%20Project-success)](#)

## 📌 Overview

**CardioAI** is a web-based heart disease risk prediction system designed to assist healthcare professionals by analyzing clinical parameters with a trained machine-learning model.

The project combines a tuned **Random Forest classifier** with a Flask web interface. A user enters clinical measurements, the application generates probability-based output, classifies the result into a risk level, shows contributing factors, and can generate a downloadable PDF report.

The academic documentation describes approximately **90% test accuracy** and approximately **0.97 AUC-ROC** for the model used in the project.

> ⚠️ **Disclaimer:** This project is for educational and academic purposes. It is a clinical decision-support prototype and is **not a substitute for professional medical diagnosis or treatment**.

## ✨ Key Features

- 🔐 Login and session-based access
- 🩺 Clinical input form with 13 model features
- 🤖 Random Forest heart disease prediction
- 📊 Probability-based risk output
- 🚦 Low / Moderate / High risk categorization
- 🔎 Risk-factor breakdown
- 🧠 AI-generated clinical summary
- 📈 Circular risk meter and visual gauge
- 📄 Downloadable PDF report
- 📱 Responsive HTML/CSS interface

## 🧠 Machine Learning Pipeline

```text
Clinical Dataset
      ↓
Data Preprocessing
      ↓
Feature Preparation
      ↓
Train / Test Split
      ↓
Random Forest + GridSearchCV
      ↓
Model Evaluation
      ↓
Saved Model (.pkl)
      ↓
Flask Application
      ↓
Risk Probability + Result
      ↓
PDF Report
```

## 🧾 Clinical Input Features

The application accepts the following 13 features:

| Feature | Description |
|---|---|
| `age` | Age |
| `sex` | Sex / gender encoding |
| `cp` | Chest pain type |
| `trestbps` | Resting blood pressure |
| `chol` | Serum cholesterol |
| `fbs` | Fasting blood sugar |
| `restecg` | Resting ECG result |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise-induced angina |
| `oldpeak` | ST depression |
| `slope` | ST segment slope |
| `ca` | Number of major vessels |
| `thal` | Thalassemia classification |

## 📈 Model & Evaluation

The project uses a **Random Forest classifier** with hyperparameter tuning through **GridSearchCV**. The project report documents approximately:

- **Test Accuracy:** 90%
- **AUC-ROC:** 0.97
- **Classification Type:** Binary heart disease risk prediction

The notebook contains the training and evaluation workflow, while the trained serialized model is used by the Flask application.

## 🖥️ Application Flow

### 1. Login

Users authenticate through the CardioAI login interface before accessing the prediction dashboard.

### 2. Clinical Data Entry

The dashboard accepts 13 clinical inputs used by the trained model.

### 3. Prediction

The Flask backend loads the trained Random Forest model and calculates class probabilities.

### 4. Risk Interpretation

The application converts the predicted probability into a displayed risk level and identifies selected contributing factors.

### 5. Reporting

A PDF report can be generated with the prediction probability, risk category, advice, AI summary, and contributing factors.

## 🗂️ Repository Structure

```text
ML-project/
│
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
├── LICENSE
│
├── data/
│   └── heart_cleveland_upload.csv
│
├── models/
│   └── rf_heart_model.pkl
│
├── notebooks/
│   └── Heart_Disease_Prediction.ipynb
│
├── templates/
│   ├── login.html
│   ├── forgot_password.html
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── login.css
│   └── style.css
│
└── docs/
    ├── CardioAI_Project_Report.docx
    ├── Heart_Disease_Report.pdf
    └── synopsis.docx
```

## ⚙️ Tech Stack

**Machine Learning:** Python, pandas, scikit-learn, Random Forest, GridSearchCV  
**Backend:** Flask  
**Frontend:** HTML, CSS, JavaScript  
**Reporting:** ReportLab  
**Model Persistence:** joblib  
**Data:** UCI Cleveland Heart Disease dataset

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Sachijhon/ML-project.git
cd ML-project
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and provide local development values. **Never commit real credentials or secrets.**

### 5. Start the application

```bash
python app.py
```

Then open the local Flask URL shown in your terminal.

## 🔐 Security Notes

This repository intentionally excludes credential files and secrets. Use environment variables or another secure local configuration method for development credentials.

Do not commit:

```text
credentials.json
.env
```

## 📚 Documentation

The `docs/` directory contains the academic project report, synopsis, and generated heart disease report associated with the project.

## 🎓 Project Context

CardioAI was developed as an academic machine-learning project focused on applying supervised learning to healthcare-oriented prediction and demonstrating an end-to-end path from model development to web deployment.

## 👤 Author

**Sachin B A**  
Aspiring Data Analyst | Python | SQL | Excel | Power BI | Machine Learning

🔗 [GitHub Profile](https://github.com/Sachijhon) · [LinkedIn](https://www.linkedin.com/in/sachin-b-a-/)

GitHub: [@Sachijhon](https://github.com/Sachijhon)

---

⭐ **Learning project:** built to demonstrate machine learning, model evaluation, Flask deployment, and practical data-to-application workflow.
