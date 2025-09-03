from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load database CSV files
sym_des = pd.read_csv("Dataset/symptoms_df.csv")
precautions = pd.read_csv("Dataset/precautions_df (1).csv")
workout = pd.read_csv("Dataset/workout_df.csv")
description = pd.read_csv("Dataset/description.csv")
medications = pd.read_csv("Dataset/medications (1).csv")
diets = pd.read_csv("Dataset/diets (1).csv")

# Load trained model
svc = pickle.load(open("models/svc.pkl", 'rb'))

# Initialize Flask app
app = Flask(__name__)

# ========================== Helper Functions ==========================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']

    return desc, pre, med, die, wrkout

symptoms_dict = {...}  # Keep your original symptoms_dict here
diseases_list = {...}  # Keep your original diseases_list here

def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# ========================== Routes ==========================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        user_symptoms = [s.strip() for s in symptoms.split(',')]
        user_symptoms = [sym.strip("[]' ") for sym in user_symptoms]
        predicted_disease = get_predicted_value(user_symptoms)

        desc, pre, med, die, wrkout = helper(predicted_disease)

        my_med = []
        for i in med[0]:
            my_med.append(i)

        return render_template(
            'index.html',
            predicted_disease=predicted_disease,
            dis_des=desc,
            dis_pre=pre,
            dis_med=med,
            dis_wrkout=wrkout,
            dis_diet=die
        )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

# ========================== Gemini Healthcare Chatbot ==========================
@app.route('/chatbot')
def chatbot_page():
    """Render chatbot UI"""
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Gemini-powered chatbot API"""
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"You are a healthcare assistant. Answer this query carefully: {user_message}"
        )

        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================== Main ==========================
if __name__ == "__main__":
    app.run(debug=True)
