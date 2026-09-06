import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="ELINK Dashboard", layout="wide", page_icon="🏢")

# CSS BIRU MIRIP ELINK
st.markdown("""
<style>
    .big-card {background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); padding: 25px; border-radius: 15px; color: white; margin-bottom: 20px;}
    .outlet-card {background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #E0E0E0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px;}
    [data-testid="stMetric"] {background: rgba(255,255,255,0.15); padding: 10px; border-radius: 10px;}
    [data-testid="stMetricLabel"] {color: white !important; font-size: 12px;}
    [data-testid="stMetricValue"] {color: white !important; font-size: 20px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("🏢 ELINK")
    st.write("**SEFTIANUS RUBEN**")
    st.markdown("---")
    st.button("📊 Dashboard", use_container_width=True)
    st.button("💳 Transaksi", use_container_width=True)
    with st.expander("📁 KELOLA DATA"):
        st.button("Pindah Saldo")
        st.button("Saldo Awal")

# HEADER + FILTER
col1, col2, col3, col4 = st.columns([2,2,2,1])
with col1: tahun = st.selectbox("Tahun", [2024,2025,2026], index=2)
with col2: bulan = st.selectbox("Bulan", ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"], index=8)
with col3: tanggal = st.selectbox("Tanggal", list(range(1,31)), index=6)
with col4: st.button("🔍 FILTER", use_container_width=True, type="primary")

periode = f"{tanggal} {bulan} {tahun}"
st.write(f"**Periode: {periode}**")

# DATA DUMMY - NANTI GANTI PAKE EXCEL
data_outlet = {
    "AGEN BAOMEKOT": {"cash": 0, "saldo": 16465098},
    "AGEN SIKU EHA": {"cash": 0, "saldo": 7435888},
    "AGEN HABIBOLA": {"cash": 0, "saldo": 6346689},
    "AGEN WATUBLAPI": {"cash": 0, "saldo": 7703080},
    "AGEN UTAMA": {"cash": 160754000, "saldo": 96378281},
}
total_cash = sum([v["cash"] for v in data_outlet.values()])
total_saldo = sum([v["saldo"] for v in data_outlet.values()])
total_aset = total_cash + total_saldo

# RINGKASAN KESELURUHAN
st.markdown('<div class="big-card">', unsafe_allow_html=True)
st.subheader("🏢 RINGKASAN KESELURUHAN OUTLET")
st.caption(f"Total {len(data_outlet)} Outlet Aktif")

c1, c2, c3, c4 = st.columns(4)
c1.metric("ASSET CASH", f"Rp {total_cash:,.0f}")
c2.metric("ASSET SALDO", f"Rp {total_saldo:,.0f}")
c3.metric("PROFIT KOTOR", "Rp 0")
c4.metric("PENGELUARAN", "Rp 0")

c1, c2, c3 = st.columns(3)
c1.metric("TOTAL ASSET", f"Rp {total_aset:,.0f}")
c2.metric("PROFIT BERSIH", "Rp 0")
c3.metric("TOTAL TRANSAKSI", "0")
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# CARD PER OUTLET
st.subheader("Detail Per Outlet")
cols = st.columns(2)
i = 0
for nama, data in data_outlet.items():
    with cols[i%2]:
        st.markdown('<div class="outlet-card">', unsafe_allow_html=True)
        st.markdown(f"### {nama}")
        st.caption(periode)
        st.selectbox("Pegawai", ["Semua Pegawai"], key=nama)
        
        c1, c2 = st.columns(2)
        c1.metric("Total Transaksi", 0)
        c2.metric("Omset", 0)
        c1.metric("Profit Kotor", 0)
        c2.metric("Pot Bank+Ops", 0)
        c1.metric("Pengeluaran", 0)
        c2.metric("Profit Bersih", 0)
        
        c1, c2 = st.columns(2)
        c1.metric("Aset Cash", f"Rp {data['cash']:,.0f}")
        c2.metric("Aset Saldo", f"Rp {data['saldo']:,.0f}")
        st.metric("Total Aset", f"Rp {data['cash']+data['saldo']:,.0f}")
        
        b1, b2, b3 = st.columns(3)
        b1.button("Tahunan", key=f"t{nama}")
        b2.button("Bulanan", key=f"b{nama}")
        b3.button("Mode Transaksi", key=f"m{nama}")
        st.markdown('</div>', unsafe_allow_html=True)
    i += 1
