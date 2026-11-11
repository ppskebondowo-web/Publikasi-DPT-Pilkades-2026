import streamlit as st
import pandas as pd
import os

# 1. Konfigurasi Tampilan untuk HP Android agar Modern & Responsif
st.set_page_config(
    page_title="DPT Pilkades 2026", 
    page_icon="🗳️", 
    layout="centered"
)

# Style CSS Kustom untuk menyembunyikan menu bawaan agar web bersih di HP warga
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. Judul Utama Aplikasi
st.title("🗳️ DPT ONLINE PILKADES 2026")
st.caption("Aplikasi Resmi Publikasi Daftar Pemilih Tetap (Tanpa Data Sensitif NIK/KK)")

# Fungsi membaca data lokal CSV secara instan (100% Kebal Eror Jaringan)
@st.cache_data
def load_local_csv(filename):
    # Membaca file CSV lokal yang berada satu folder dengan app.py
    df = pd.read_csv(filename, header=0, dtype=str)
    df = df.dropna(how='all', axis=0)
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

# 3. FITUR 1: TAMPILKAN REKAPITULASI
st.subheader("📊 Rekapitulasi Pemilih")
try:
    if os.path.exists("Rekap.csv"):
        df_rekap = load_local_csv("Rekap.csv")
        st.dataframe(df_rekap, use_container_width=True, hide_index=True)
    else:
        st.error("File 'Rekap.csv' tidak ditemukan di server aplikasi. Pastikan Anda sudah mengunggahnya ke GitHub.")
except Exception as e:
    st.error("Gagal memproses data Rekapitulasi lokal.")

# 4. FITUR 2: PENCARIAN & DETAIL DATA PER TPS
st.markdown("---")
st.subheader("🔍 Cek Daftar Pemilih Per TPS")

# Membuat daftar nama file CSV lokal sesuai pilihan TPS
tps_options = {
    "TPS 001": "TPS_001.csv",
    "TPS 002": "TPS_002.csv",
    "TPS 003": "TPS_003.csv",
    "TPS 004": "TPS_004.csv",
    "TPS 005": "TPS_005.csv",
    "TPS 006": "TPS_006.csv",
    "TPS 007": "TPS_007.csv",
    "TPS 008": "TPS_008.csv",
    "TPS 009": "TPS_009.csv",
    "TPS 010": "TPS_010.csv",
    "TPS 011": "TPS_011.csv"
}

pilihan_tps = st.selectbox("Pilih nomor TPS terlebih dahulu:", ["-- Pilih TPS --"] + list(tps_options.keys()))

if pilihan_tps != "-- Pilih TPS --":
    csv_file = tps_options[pilihan_tps]
    
    if not os.path.exists(csv_file):
        st.error(f"File '{csv_file}' belum diunggah ke GitHub Anda.")
    else:
        try:
            df_tps = load_local_csv(csv_file)
            kolom_nama = [col for col in df_tps.columns if col.lower() == 'nama']
            
            if not kolom_nama:
                st.error(f"Eror Struktur: Kolom dengan nama 'Nama' tidak ditemukan di {pilihan_tps}.")
            else:
                nama_key = kolom_nama[0]
                df_tps[nama_key] = df_tps[nama_key].fillna('').astype(str).str.strip()
                
                # Kolom Input Pencarian Nama bagi Warga
                cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: ALAM KHODIRUN")
                
                if cari_nama:
                    df_filtered = df_tps[df_tps[nama_key].str.contains(cari_nama, case=False, na=False)]
                    if not df_filtered.empty:
                        st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
                    else:
                        st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Periksa ejaan kembali.")
                else:
                    st.info(f"Menampilkan seluruh daftar pemilih di {pilihan_tps} (Total: {len(df_tps)} orang)")
                    st.dataframe(df_tps, use_container_width=True, hide_index=True)
                
        except Exception as e:
            st.error(f"Gagal memuat data lokal untuk {pilihan_tps}.")
