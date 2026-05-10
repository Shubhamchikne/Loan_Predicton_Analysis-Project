import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("Loan Approval Predictor")

# Inputs
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
dependents = st.selectbox("Dependents", [0,1,2,3])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["No", "Yes"])
property_area = st.selectbox("Property Area", ["Urban","Semiurban","Rural"])

income = st.slider("Applicant Income", 1000, 100000, 45000)
coincome = st.slider("Coapplicant Income", 0, 50000, 10000)
loan = st.slider("Loan Amount", 20, 700, 150)
term = st.selectbox("Loan Term", [360,300,240,180,120,84,60])
prev = st.selectbox("Previous Loans", [0,1,2,3])
credit_score = st.slider("Credit Score", 300, 900, 700)
credit_history = st.selectbox("Credit History", [1,0])

# Encode manually (same as training)
gender = 1 if gender=="Male" else 0
married = 1 if married=="Yes" else 0
education = 0 if education=="Graduate" else 1
self_employed = 1 if self_employed=="Yes" else 0
property_area = {"Rural":0,"Semiurban":1,"Urban":2}[property_area]

total_income = income + coincome

# Prediction
if st.button("Predict"):

    # ✅ STEP 1: Create dataframe FIRST
    input_data = pd.DataFrame({
        'Loan_ID': ['LP001'],   # add this if needed
        'Gender':[gender],
        'Married':[married],
        'Dependents':[dependents],
        'Education':[education],
        'Self_Employed':[self_employed],
        'ApplicantIncome':[income],
        'CoapplicantIncome':[coincome],
        'LoanAmount':[loan],
        'Loan_Amount_Term':[term],
        'Previous_Loan':[prev],
        'Credit_Score':[credit_score],
        'Credit_History':[credit_history],
        'Property_Area':[property_area],
        'TotalIncome':[total_income]
    })

    # ✅ STEP 2: Define columns
    cols = [
        
        'Gender','Married','Dependents','Education','Self_Employed',
        'ApplicantIncome','CoapplicantIncome','LoanAmount',
        'Loan_Amount_Term','Previous_Loan','Credit_Score',
        'Credit_History','Property_Area','TotalIncome'
    ]

    # ✅ STEP 3: Reindex
    input_data = input_data.reindex(columns=cols, fill_value=0)

    # ✅ STEP 4: Predict
    prediction = model.predict(input_data)

    # ✅ STEP 5: Output
    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")