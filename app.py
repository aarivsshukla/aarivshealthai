import streamlit as st
from thefuzz import process

# Simplified disease database (expand this as needed)
disease_data = {
    "Common Cold": ["sneezing", "runny nose", "sore throat", "cough", "congestion"],
    "Flu": ["fever", "chills", "muscle aches", "fatigue", "cough", "sore throat"],
    "COVID-19": ["fever", "cough", "loss of taste", "loss of smell", "fatigue", "shortness of breath"],
    "Diabetes": ["increased thirst", "frequent urination", "hunger", "fatigue", "blurred vision"],
    "Asthma": ["shortness of breath", "chest tightness", "wheezing", "coughing"],
    "Migraine": ["headache", "nausea", "sensitivity to light", "sensitivity to sound", "vomiting"],
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "fever", "abdominal cramps"],
    "Pneumonia": ["fever", "cough", "chest pain", "shortness of breath", "fatigue"],
    "Malaria": ["fever", "chills", "headache", "nausea", "vomiting", "sweating"],
}

# Flatten all symptoms to help match from natural language
all_symptoms = set(symptom for symptoms in disease_data.values() for symptom in symptoms)

def extract_keywords(user_input):
    matches = process.extract(user_input, list(all_symptoms), limit=5)
    return [match[0] for match in matches if match[1] > 70]

def diagnose(symptoms):
    results = []
    for disease, known_symptoms in disease_data.items():
        match_score = len(set(symptoms) & set(known_symptoms)) / len(set(known_symptoms))
        if match_score >= 0.4:
            results.append((disease, round(match_score * 100)))
    return sorted(results, key=lambda x: x[1], reverse=True)

# Streamlit UI
st.title("🩺 AI Health Assistant")
st.subheader("Describe your symptoms, and I'll try to guess what you might have.")

user_input = st.text_area("Describe how you're feeling:")

if st.button("Diagnose"):
    if user_input.strip() == "":
        st.warning("Please enter some symptoms or description.")
    else:
        keywords = extract_keywords(user_input.lower())
        if keywords:
            st.info(f"🧠 I detected these symptoms: {', '.join(keywords)}")
            diagnosis = diagnose(keywords)
            if diagnosis:
                st.success("Possible conditions based on your symptoms:")
                for disease, confidence in diagnosis:
                    st.write(f"- **{disease}** ({confidence}% match)")
            else:
                st.warning("I couldn't match your symptoms to a known disease. Try rephrasing.")
        else:
            st.warning("I couldn't understand your symptoms clearly. Try being more specific.")
