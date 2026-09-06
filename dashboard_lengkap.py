import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard 7 SEPT 2026", layout="wide")

def login():
    st.title("🔐 Login Dashboard")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("Username/Password salah")
    st.info("Default: admin / 1234")

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in: login(); st.stop()

st.title("📊 Dashboard Keuangan & Agen 2026")
st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False))
uploaded_file = st.file_uploader("Upload file 7_SEPT_2026_UPDATE_FORMAT.xlsx", type="xlsx")

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    menu = st.sidebar.selectbox("Menu", ["Ringkasan", "Data Agen", "Rekap Bulanan", "Keuangan", "Kios & Bon"])
    if menu == "Ringkasan": st.dataframe(pd.read_excel(xls, "TAHUNAN", header=None))
    if menu == "Data Agen": st.dataframe(pd.read_excel(xls, st.selectbox("Pilih Agen", ["AGEN BAOMEKOT","AGEN SIKU EHA","AGEN HABIBOLA","AGEN WATUBLAPI"]), header=None))
    if menu == "Rekap Bulanan": st.dataframe(pd.read_excel(xls, "2026", header=None))
    if menu == "Keuangan":
        tab1, tab2 = st.tabs(["Pengeluaran", "Gaji"])
        with tab1: st.dataframe(pd.read_excel(xls, "ESTIMASI PENGELUARAN BULAN", header=None))
        with tab2: st.dataframe(pd.read_excel(xls, "HITUNG GAJI REGULER KARYAWAN", header=None))
    if menu == "Kios & Bon": st.dataframe(pd.read_excel(xls, "KIOS", header=None))
else: st.warning("Upload file Excel dulu ya")
