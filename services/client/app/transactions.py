import streamlit as st
import requests
import pandas as pd
from .server import server_host, server_port

BASE_URL = f"http://{server_host}:{server_port}/transactions"


def show_transactions():
    st.header("Transactions Viewer")

    all_data = []
    try:
        response = requests.get(BASE_URL, timeout=5)
        response.raise_for_status()
        all_data = response.json()
        if not isinstance(all_data, list):
            all_data = [all_data]
        available_accounts = sorted(list({t.get("AccountID") for t in all_data if "AccountID" in t}))
    except Exception as e:
        st.error(f"Error fetching accounts: {e}")
        available_accounts = []

    account_id = st.selectbox("Select AccountID", options=["All"] + available_accounts)

    if account_id != "All":
        try:
            resp = requests.get(f"{BASE_URL}/{account_id}", timeout=5)
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
        except Exception as e:
            st.error(f"Error fetching transactions: {e}")
            df = pd.DataFrame()
    else:
        df = pd.DataFrame(all_data)

    st.dataframe(df)
