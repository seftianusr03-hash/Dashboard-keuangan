import streamlit as st
import pandas as pd

st.set_page_config(page_title="ELINK FULL", layout="wide")

st.markdown("""
<style>
    .big-card {background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); padding: 25px; border-radius: 15px; color: white;}
    .outlet-card {background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #E0E0E0;}
</style>
""", unsafe_allow_html=True)

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        st.title("Login ELINK")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and pw == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Username/Password salah")
        st.stop()
login()

st.title("🏢 ELINK SMART SYSTEM")

df_transaksi = pd.read_excel("DATA_ELINK.xlsx", sheet_name="Transaksi")
df_saldo = pd.read_excel("DATA_ELINK.xlsx", sheet_name="Saldo_Awal")
df_outlet = pd.read_excel("DATA_ELINK.xlsx", sheet_name="Outlet")

col1, col2, col3 = st.columns(3)
tahun = col1.selectbox("Tahun", [2024,2025,2026])
bulan = col2.selectbox("Bulan", df_transaksi["Tanggal"].dt.month.unique())
outlet = col3.selectbox("Pilih Outlet", ["Semua"] + list(df_outlet["Nama_Outlet"].unique()))

df_filter = df_transaksi.copy()
if outlet != "Semua":
    df_filter = df_filter[df_filter["Outlet"] == outlet]

total_omset = df_filter["Omset"].sum()
total_modal = df_filter["Modal"].sum()
total_pengeluaran = df_filter["Pengeluaran"].sum()
profit_kotor = total_omset - total_modal
profit_bersih = profit_kotor - total_pengeluaran
total_aset = df_saldo["Aset_Cash"].sum() + df_saldo["Aset_Saldo"].sum()

st.markdown('<div class="big-card">', unsafe_allow_html=True)
st.subheader("RINGKASAN KESELURUHAN")
c1, c2, c3, c4 = st.columns(4)
c1.metric("TOTAL OMSET", f"Rp {total_omset:,.0f}")
c2.metric("PROFIT KOTOR", f"Rp {profit_kotor:,.0f}")
c3.metric("PENGELUARAN", f"Rp {total_pengeluaran:,.0f}")
c4.metric("TOTAL ASET", f"Rp {total_aset:,.0f}")
st.markdown('</div>', unsafe_allow_html=True)

st.dataframe(df_filter)
