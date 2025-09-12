import streamlit as st
from transactions import show_transactions
from models import show_models

st.sidebar.title("Menu")
page = st.sidebar.selectbox("Choose a page", ["Transactions", "Models"])  

if page == "Transactions":
    show_transactions()
elif page == "Models":
    show_models()
