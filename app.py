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

# ID Google Sheet Publik Anda
SHEET_ID = "1Xvi40Xj5MXFLuu5v4mi-wv3Oyfe7dYuyxNKccXbxXV0"

# Fungsi membaca data ter-cache dengan pembersihan data tingkat lanjut
@st.cache_data(ttl=60)
def load_sheet_data(sheet_name):
    url = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    # Membaca seluruh data sebagai text/string demi keamanan data tipe nomor
    df = pd.read_csv(url, header=0, dtype=str)
    
    # 1. Bersihkan baris yang kosong total di Google Sheet
    df = df.dropna(how='all', axis=0)
    
    # 2. Bersihkan nama kolom dari spasi tersembunyi
    df.columns = df.columns.str.strip()
    
    # 3. BUANG KOLOM KOSONG (UNNAMED) SECARA OTOMATIS
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
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
        # Mengambil data TPS dengan fungsi pembersihan baru
        df_tps = load_sheet_data(pilihan_tps)
        
        # Validasi Dinamis untuk mendeteksi kolom nama secara fleksibel
        kolom_nama = [col for col in df_tps.columns if col.lower() == 'nama']
        
        if not kolom_nama:
            st.error(f"Eror Struktur: Kolom dengan nama 'Nama' tidak ditemukan di tab {pilihan_tps}. Periksa tulisan header di Google Sheets Anda.")
        else:
            nama_key = kolom_nama[0] # Mengambil nama kolom yang tepat (misal 'Nama')
            df_tps[nama_key] = df_tps[nama_key].fillna('').astype(str).str.strip()
            
            # Kolom Input Pencarian Nama bagi Warga
            cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: ALAM KHODIRUN")
            
            if cari_nama:
                # Filter pencarian nama tanpa memedulikan huruf besar/kecil (case-insensitive)
                df_filtered = df_tps[df_tps[nama_key].str.contains(cari_nama, case=False, na=False)]
                
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
