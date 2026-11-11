import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Konfigurasi Tampilan HP Android agar Modern & Responsif
st.set_page_config(
    page_title="DPT Pilkades 2026", 
    page_icon="🗳️", 
    layout="centered"
)

# Style CSS Kustom untuk menyembunyikan menu bawaan & mempercantik tabel di HP
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

# URL Google Sheet Publik Anda
GOOGLE_SHEET_URL = "https://google.com"

# Membuat koneksi aman dan stabil ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fungsi membaca data ter-cache agar loading web super cepat di HP warga
@st.cache_data(ttl=300) # Data disimpan di memori selama 5 menit
def load_sheet_data(sheet_name):
    # Membaca sheet berdasarkan nama tab secara presisi
    df = conn.read(spreadsheet=GOOGLE_SHEET_URL, worksheet=sheet_name)
    # Bersihkan baris atau kolom kosong bawaan Google Sheet jika ada
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)
    return df

# 3. FITUR 1: TAMPILKAN REKAPITULASI
st.subheader("📊 Rekapitulasi Pemilih")
try:
    df_rekap = load_sheet_data("Rekap")
    st.dataframe(df_rekap, use_container_width=True, hide_index=True)
except Exception as e:
    st.error("Gagal memuat data sheet 'Rekap'. Pastikan akses Google Sheet tetap diatur publik.")

# 4. FITUR 2: PENCARIAN & DETAIL DATA PER TPS
st.markdown("---")
st.subheader("🔍 Cek Daftar Pemilih Per TPS")

# Membuat daftar opsi pilihan TPS 001 sampai TPS 011 sesuai nama tab Anda
tps_list = [f"TPS {str(i).zfill(3)}" for i in range(1, 12)]
pilihan_tps = st.selectbox("Pilih nomor TPS terlebih dahulu:", ["-- Pilih TPS --"] + tps_list)

if pilihan_tps != "-- Pilih TPS --":
    try:
        # Mengambil data TPS menggunakan GSheetsConnection
        df_tps = load_sheet_data(pilihan_tps)
        
        # Kolom Pencarian Nama bagi Warga
        cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: Budi")
        
        if cari_nama:
            # Mengubah kolom Nama menjadi teks string untuk menghindari error type
            df_tps['Nama'] = df_tps['Nama'].astype(str)
            # Cari nama tanpa memedulikan huruf besar/kecil (case-insensitive)
            df_filtered = df_tps[df_tps['Nama'].str.contains(cari_nama, case=False, na=False)]
            
            if not df_filtered.empty:
                st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            else:
                st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Coba ketik nama panggilan atau cek kembali TPS-nya.")
        else:
            # Jika kolom pencarian kosong, tampilkan info total warga di TPS tersebut
            st.info(f"Menampilkan seluruh daftar pemilih di {pilihan_tps} (Total: {len(df_tps)} orang)")
            st.dataframe(df_tps, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Gagal memuat data untuk {pilihan_tps}. Sistem mendeteksi pemutusan koneksi sementara dari Google. Silakan coba pilih ulang opsi TPS.")
