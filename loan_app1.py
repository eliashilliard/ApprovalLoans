
import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load model
model = pickle.load(open("finalexam458.pkl", "rb"))

st.title("Loan Approval & Lender Optimizer")

st.write("Enter applicant details below:")

# NUMERIC FEATURES

loan = st.number_input("Requested Loan Amount", 0, 100000, 10000)
fico = st.slider("FICO Score", 300, 850, 650)
income = st.number_input("Monthly Gross Income", 0, 100000, 4000)
housing = st.number_input("Monthly Housing Payment", 0, 50000, 1200)


# CATEGORICAL FEATURES

reason = st.selectbox("Loan Reason", ["DebtCon", "HomeImp"])
job = st.selectbox("Employment Status", ["Employed", "Unemployed", "Self-employed"])
sector = st.selectbox("Employment Sector", ["Private", "Public", "Unknown"])
lender = st.selectbox("Preferred Lender", ["A", "B", "C"])
bankrupt = st.selectbox("Ever Bankrupt/Foreclose?", ["No", "Yes"])

bankrupt = 1 if bankrupt == "Yes" else 0


# Input data frame
input_data = pd.DataFrame([{
    "Requested_Loan_Amount": loan,
    "FICO_score": fico,
    "Monthly_Gross_Income": income,
    "Monthly_Housing_Payment": housing,
    "Ever_Bankrupt_or_Foreclose": bankrupt,
    "Reason": reason,
    "Employment_Status": job,
    "Employment_Sector": sector,
    "Lender": lender
}])


input_encoded = pd.get_dummies(input_data)


input_encoded = input_encoded[model_cols]

#Prediction
if st.button("Predict Approval"):

    pred = model.predict(input_encoded)[0]
    prob = model.predict_proba(input_encoded)[0][1]

    st.subheader("Result")

    if pred == 1:
        st.success("Loan APPROVED")
    else:
        st.error("Loan DENIED")

    st.write(f"Approval Probability: {prob:.2%}")


    # RECOMMENDATION

    st.subheader("Recommended Lender")

    if pred == 1:
        if prob > 0.75:
            st.write("👉 Choose Lender B ($350 payout)")
        elif prob > 0.5:
            st.write("👉 Choose Lender A ($250 payout)")
        else:
            st.write("👉 Choose Lender C ($150 payout)")
    else:
        st.write("No lender recommended (high risk)")
