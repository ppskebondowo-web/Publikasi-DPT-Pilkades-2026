import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Konfigurasi Tampilan HP Android agar Modern & Responsif
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

# 2. Judul Aplikasi Web
st.title("🗳️ DPT ONLINE PILKADES 2026")
st.caption("Aplikasi Resmi Publikasi Daftar Pemilih Tetap (Tanpa Data Sensitif NIK/KK)")

# URL Tautan Google Sheet Publik Anda
GOOGLE_SHEET_URL = "https://google.com"

# Menginisialisasi koneksi resmi Streamlit ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fungsi membaca data ter-cache agar loading web super cepat di HP warga
@st.cache_data(ttl=300) # Simpan cache di memori selama 5 menit
def load_sheet_data(sheet_name):
    # MENYANTUMKAN TAUTAN SPREADSHEET SECARA EKSPLISIT AGAR TIDAK ERROR
    df = conn.read(spreadsheet=GOOGLE_SHEET_URL, worksheet=sheet_name)
    # Bersihkan baris atau kolom kosong otomatis bawaan Google Sheet jika ada
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)
    return df

# 3. FITUR 1: TAMPILKAN REKAPITULASI
st.subheader("📊 Rekapitulasi Pemilih")
try:
    df_rekap = load_sheet_data("Rekap")
    st.dataframe(df_rekap, use_container_width=True, hide_index=True)
except Exception as e:
    st.error("Gagal memuat data sheet 'Rekap'. Silakan muat ulang halaman atau periksa koneksi internet Anda.")

# 4. FITUR 2: PENCARIAN & DETAIL DATA PER TPS
st.markdown("---")
st.subheader("🔍 Cek Daftar Pemilih Per TPS")

# Membuat daftar pilihan TPS 001 sampai TPS 011 sesuai nama tab sheet Anda
tps_list = [f"TPS {str(i).zfill(3)}" for i in range(1, 12)]
pilihan_tps = st.selectbox("Pilih nomor TPS terlebih dahulu:", ["-- Pilih TPS --"] + tps_list)

if pilihan_tps != "-- Pilih TPS --":
    try:
        # Mengambil data TPS secara presisi
        df_tps = load_sheet_data(pilihan_tps)
        
        # Kolom Input Pencarian Nama bagi Warga
        cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: Budi")
        
        if cari_nama:
            # Mengubah kolom Nama menjadi tipe teks string untuk menghindari error type data
            df_tps['Nama'] = df_tps['Nama'].astype(str)
            # Filter pencarian nama tanpa memedulikan huruf besar/kecil (case-insensitive)
            df_filtered = df_tps[df_tps['Nama'].str.contains(cari_nama, case=False, na=False)]
            
            if not df_filtered.empty:
                st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            else:
                st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Pastikan ejaan benar atau coba cari di TPS lain.")
        else:
            # Jika kolom input kosong, tampilkan info total warga dan daftar seluruhnya di TPS tersebut
            st.info(f"Menampilkan seluruh daftar pemilih di {pilihan_tps} (Total: {len(df_tps)} orang)")
            st.dataframe(df_tps, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Gagal memuat data untuk {pilihan_tps}. Silakan coba klik/pilih kembali nama TPS Anda pada menu di atas.")
