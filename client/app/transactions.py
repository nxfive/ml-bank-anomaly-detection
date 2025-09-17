import streamlit as st
import requests
import pandas as pd
from .server import server_host, server_port

BASE_URL = f"http://{server_host}:{server_port}/transactions"


def show_transactions():
    st.header("Transactions Viewer")

    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        all_data = response.json()
        available_accounts = sorted(list({t["AccountID"] for t in all_data}))
    except Exception as e:
        st.error(f"Error fetching accounts: {e}")
        available_accounts = []

    account_id = st.selectbox("Select AccountID", options=["All"] + available_accounts)

    if account_id != "All":
        try:
            resp = requests.get(f"{BASE_URL}/{account_id}")
            resp.raise_for_status()
            df = pd.DataFrame(resp.json())
        except Exception as e:
            st.error(f"Error fetching transactions: {e}")
            df = pd.DataFrame()
    else:
        df = pd.DataFrame(all_data)


    st.dataframe(df)
