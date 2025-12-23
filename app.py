import streamlit as st
import pandas as pd
import pickle

# ---------------------------
# Load model & encoders
# ---------------------------
model = pickle.load(open(r"models\readmission_model.pkl", "rb"))
encoders = pickle.load(open(r"models\encoders.pkl", "rb"))

st.set_page_config(page_title="Readmission Prediction", layout="centered")
st.title("🏥 Patient Readmission Prediction")

st.write("Predict whether a patient is likely to be readmitted")

# ---------------------------
# Input Form
# ---------------------------
with st.form("prediction_form"):

    age = st.slider("Age", 18, 100, 60)
    time_in_hospital = st.slider("Time in Hospital (days)", 1, 14, 5)
    n_lab_procedures = st.number_input("Lab Procedures", 0, 100, 40)
    n_procedures = st.number_input("Procedures", 0, 10, 1)
    n_medications = st.number_input("Medications", 0, 50, 10)
    n_outpatient = st.number_input("Outpatient Visits", 0, 20, 0)
    n_inpatient = st.number_input("Inpatient Visits", 0, 20, 0)
    n_emergency = st.number_input("Emergency Visits", 0, 20, 0)

    medical_specialty = st.selectbox(
        "Medical Specialty",
        encoders['medical_specialty'].classes_
    )

    diag_1 = st.selectbox("Primary Diagnosis", encoders['diag_1'].classes_)
    diag_2 = st.selectbox("Secondary Diagnosis", encoders['diag_2'].classes_)
    diag_3 = st.selectbox("Additional Diagnosis", encoders['diag_3'].classes_)

    glucose_test = st.selectbox(
        "Glucose Test",
        encoders['glucose_test'].classes_
    )

    a1ctest = st.selectbox(
        "A1C Test",
        encoders['a1ctest'].classes_
    )

    change = st.selectbox(
        "Medication Change",
        encoders['change'].classes_
    )

    diabetes_med = st.selectbox(
        "Diabetes Medication",
        encoders['diabetes_med'].classes_
    )

    submit = st.form_submit_button("Predict")

# ---------------------------
# Prediction
# ---------------------------
if submit:
    input_data = pd.DataFrame([{
        'age': age,
        'time_in_hospital': time_in_hospital,
        'n_lab_procedures': n_lab_procedures,
        'n_procedures': n_procedures,
        'n_medications': n_medications,
        'n_outpatient': n_outpatient,
        'n_inpatient': n_inpatient,
        'n_emergency': n_emergency,
        'medical_specialty': encoders['medical_specialty'].transform([medical_specialty])[0],
        'diag_1': encoders['diag_1'].transform([diag_1])[0],
        'diag_2': encoders['diag_2'].transform([diag_2])[0],
        'diag_3': encoders['diag_3'].transform([diag_3])[0],
        'glucose_test': encoders['glucose_test'].transform([glucose_test])[0],
        'a1ctest': encoders['a1ctest'].transform([a1ctest])[0],
        'change': encoders['change'].transform([change])[0],
        'diabetes_med': encoders['diabetes_med'].transform([diabetes_med])[0],
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ Patient likely to be readmitted (Probability: {probability:.2%})")
    else:
        st.success(f"✅ Patient unlikely to be readmitted (Probability: {probability:.2%})")
