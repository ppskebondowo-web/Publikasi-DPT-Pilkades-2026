import streamlit as st
import pandas as pd
import urllib.request
import io
import ssl

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

# ID Google Sheet Publik Anda
SHEET_ID = "1Xvi40Xj5MXFLuu5v4mi-wv3Oyfe7dYuyxNKccXbxXV0"

# Kamus Pemetaan ID Tab (GID) berdasarkan data asli Google Sheet Anda
GID_MAP = {
    "Rekap": "1866580022",
    "TPS 001": "402733912",
    "TPS 002": "577903264",
    "TPS 003": "981448162",
    "TPS 004": "1342674488",
    "TPS 005": "688461718",
    "TPS 006": "1657805169",
    "TPS 007": "315575510",
    "TPS 008": "1468164319",
    "TPS 009": "1009029986",
    "TPS 010": "377507340",
    "TPS 011": "452778848"
}

# Fungsi membaca data murni BYPASS SSL agar terbebas dari error koneksi server
@st.cache_data(ttl=30)
def load_sheet_secure(sheet_name):
    gid = GID_MAP.get(sheet_name)
    url = f"https://google.com{SHEET_ID}/export?format=csv&gid={gid}"
    
    # Membuat context untuk mengabaikan verifikasi SSL yang sering membuat koneksi macet
    context = ssl._create_unverified_context()
    
    # Mengunduh data sebagai raw byte teks
    with urllib.request.urlopen(url, context=context) as response:
        html_data = response.read()
        
    # Membaca file mentah ke dalam bentuk tabel pandas dataframe
    df = pd.read_csv(io.BytesIO(html_data), header=0, dtype=str)
    df = df.dropna(how='all', axis=0)
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

# 3. FITUR 1: TAMPILKAN REKAPITULASI
st.subheader("📊 Rekapitulasi Pemilih")
try:
    df_rekap = load_sheet_secure("Rekap")
    st.dataframe(df_rekap, use_container_width=True, hide_index=True)
except Exception as e:
    st.error("Gagal terhubung dengan server Google. Silakan klik tombol 'Muat Ulang Hubungan Data' di bawah.")

# Tombol refresh darurat untuk menghapus memori sistem yang nyangkut
if st.button("🔄 Muat Ulang Hubungan Data"):
    st.cache_data.clear()
    st.rerun()

# 4. FITUR 2: PENCARIAN & DETAIL DATA PER TPS
st.markdown("---")
st.subheader("🔍 Cek Daftar Pemilih Per TPS")

tps_list = [f"TPS {str(i).zfill(3)}" for i in range(1, 12)]
pilihan_tps = st.selectbox("Pilih nomor TPS terlebih dahulu:", ["-- Pilih TPS --"] + tps_list)

if pilihan_tps != "-- Pilih TPS --":
    try:
        df_tps = load_sheet_secure(pilihan_tps)
        kolom_nama = [col for col in df_tps.columns if col.lower() == 'nama']
        
        if not kolom_nama:
            st.error(f"Eror Struktur: Kolom dengan nama 'Nama' tidak ditemukan di {pilihan_tps}.")
        else:
            nama_key = kolom_nama[0]
            df_tps[nama_key] = df_tps[nama_key].fillna('').astype(str).str.strip()
            
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
        st.error(f"Gagal memuat data {pilihan_tps}. Silakan coba klik tombol 'Muat Ulang Hubungan Data' di atas.")
