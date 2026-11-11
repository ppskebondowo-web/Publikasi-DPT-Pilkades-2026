import streamlit as st
import pandas as pd

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

# 2. Judul Aplikasi Web
st.title("🗳️ DPT ONLINE PILKADES 2026")
st.caption("Aplikasi Resmi Publikasi Daftar Pemilih Tetap (Tanpa Data Sensitif NIK/KK)")

# ID Google Sheet Publik Anda yang diambil dari link asli
SHEET_ID = "1Xvi40Xj5MXFLuu5v4mi-wv3Oyfe7dYuyxNKccXbxXV0"

# Fungsi membaca data ter-cache agar loading web super cepat di HP warga
@st.cache_data(ttl=60) # Simpan cache pendek agar tidak memicu error pemutusan dari Google
def load_sheet_data(sheet_name):
    # Menggunakan metode ekspor CSV resmi dari Google Docs API
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    # Memaksa pandas membaca baris pertama sebagai header agar stabil
    df = pd.read_csv(url, header=0)
    # Bersihkan baris atau kolom kosong otomatis bawaan Google Sheet jika ada
    df = df.dropna(how='all', axis=0)
    return df

# 3. FITUR 1: TAMPILKAN REKAPITULASI
st.subheader("📊 Rekapitulasi Pemilih")
try:
    df_rekap = load_sheet_data("Rekap")
    st.dataframe(df_rekap, use_container_width=True, hide_index=True)
except Exception as e:
    st.error("Sistem sedang memuat ulang koneksi ke Google Sheets. Silakan tekan tombol 'Segarkan Data' di bawah.")

# Tombol manual untuk membersihkan memori eror jika Google sempat memblokir koneksi
if st.button("🔄 Segarkan Data (Refresh Data)"):
    st.cache_data.clear()
    st.rerun()

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
        st.error(f"Gagal memuat data {pilihan_tps}. Silakan ketuk tombol 'Segarkan Data' di atas terlebih dahulu.")
