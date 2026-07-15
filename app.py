import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Banking Fraud Detection Analysis",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Fraud Detection Analysis Dashboard")

st.markdown("""
This application provides an interactive overview of the Credit Card Fraud Detection dataset.
""")

try:
    # Automatically load dataset from the repository
    df = pd.read_csv("creditcard.csv")

    st.success("Dataset Loaded Successfully!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", len(df))
    col2.metric("Fraud Transactions", int(df["Class"].sum()))
    col3.metric("Legitimate Transactions", int((df["Class"] == 0).sum()))

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Fraud Distribution")
    st.bar_chart(df["Class"].value_counts())

except FileNotFoundError:
    st.error("creditcard.csv not found. Please add creditcard.csv to the GitHub repository.")
