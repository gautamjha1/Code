import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Database setup
conn = sqlite3.connect('mortgage_crm.db', check_same_thread=False)
cursor = conn.cursor()

# Clients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    loan_type TEXT,
    amount REAL,
    status TEXT,
    notes TEXT
)
""")

conn.commit()

st.set_page_config(page_title="Mortgage Broker CRM", layout="wide")
st.title("🏠 Mortgage Broker CRM")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["➕ Add Client", "📋 Clients", "📊 Analytics", "📄 File Upload"])

if page == "➕ Add Client":
    st.header("➕ Add Client")
    with st.form("client_form"):
        name = st.text_input("Client Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        loan_type = st.selectbox("Loan Type", ["Purchase", "Refinance", "HELOC", "Other"])
        amount = st.number_input("Loan Amount ($)", min_value=0.0, step=1000.0)
        status = st.selectbox("Status", ["Lead", "Application", "Pre-Approval", "Approved", "Funded", "Declined"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Client")
        if submitted:
            cursor.execute("INSERT INTO clients (name, email, phone, loan_type, amount, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (name, email, phone, loan_type, amount, status, notes))
            conn.commit()
            st.success("Client added successfully!")

elif page == "📋 Clients":
    st.header("📋 Client List")
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    loan_filter = st.selectbox("Filter by Loan Type", ["All"] + df["loan_type"].unique().tolist())
    if loan_filter != "All":
        df = df[df["loan_type"] == loan_filter]
    st.dataframe(df)

elif page == "📊 Analytics":
    st.header("📊 Basic Analytics")
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    loan_counts = df['loan_type'].value_counts()
    loan_status_counts = df['status'].value_counts()

    st.subheader("Loans by Type")
    st.bar_chart(loan_counts)

    st.subheader("Loans by Status")
    st.bar_chart(loan_status_counts)

elif page == "📄 File Upload":
    st.header("📄 Upload Mortgage Documents")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileSize": uploaded_file.size}
        st.write(file_details)
        st.success("File uploaded successfully! (Processing feature coming soon)")
