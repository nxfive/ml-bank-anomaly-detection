import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000/models"

TRANSACTION_TYPES = ["Credit", "Debit"]
CHANNELS = ["Online", "ATM", "Branch"]
CUSTOMER_OCCUPATIONS = ["Doctor", "Student", "Retired", "Engineer", "Other"]


def show_models():
    st.header("Models Viewer")

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        available_models = response.json().get("available_models", [])
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        available_models = []

    model_choice = st.selectbox("Select Model", options=available_models + ["Both"])
    num_rows = st.number_input("Number of transactions to predict", min_value=1, max_value=10, value=1)

    st.subheader("Predict Transactions")
    transactions = []
    for i in range(num_rows):
        st.markdown(f"**Transaction {i+1}**")
        transaction = {
            "TransactionID": st.text_input(f"TransactionID {i+1}", value=f"TX{i+1:06d}"),
            "AccountID": st.text_input(f"AccountID {i+1}", value=f"AC{i+1:05d}"),
            "TransactionAmount": st.number_input(f"TransactionAmount {i+1}", value=100.0),
            "TransactionDate": st.text_input(f"TransactionDate {i+1}", value="2023-04-11 16:29:14"),
            "TransactionType": st.selectbox(f"TransactionType {i+1}", TRANSACTION_TYPES),
            "Location": st.text_input(f"Location {i+1}", value="Houston"),
            "DeviceID": st.text_input(f"DeviceID {i+1}", value=f"D{i+1:05d}"),
            "IPAddress": st.text_input(f"IPAddress {i+1}", value="200.13.225.150"),
            "MerchantID": st.text_input(f"MerchantID {i+1}", value=f"M{i+1:03d}"),
            "Channel": st.selectbox(f"Channel {i+1}", CHANNELS),
            "CustomerAge": st.number_input(f"CustomerAge {i+1}", value=30),
            "CustomerOccupation": st.selectbox(f"CustomerOccupation {i+1}", CUSTOMER_OCCUPATIONS),
            "TransactionDuration": st.number_input(f"TransactionDuration {i+1}", value=10),
            "LoginAttempts": st.number_input(f"LoginAttempts {i+1}", value=1),
            "AccountBalance": st.number_input(f"AccountBalance {i+1}", value=1000.0),
            "PreviousTransactionDate": st.text_input(f"PreviousTransactionDate {i+1}", value="2023-04-01 16:29:14")
        }
        transactions.append(transaction)

    if st.button("Predict"):
        if transactions and model_choice:
            try:
                if model_choice == "Both":
                    resp = requests.post(f"{BASE_URL}/predict", json=transactions)
                else:
                    resp = requests.post(f"{BASE_URL}/{str(model_choice).replace(" ", "_").lower()}/predict", json=transactions)

                resp.raise_for_status()
                df = pd.DataFrame(resp.json())
                st.success("Predictions done!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error making prediction: {e}")
