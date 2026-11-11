import streamlit as st
import pandas as pd

# 1. Konfigurasi Tampilan untuk HP Android
st.set_page_config(
    page_title="DPT Pilkades 2026", 
    page_icon="🗳️", 
    layout="centered"
)

# Menghilangkan menu bawaan Streamlit agar aplikasi terlihat bersih dan profesional
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. Judul Aplikasi
st.title("🗳️ DPT ONLINE PILKADES 2026")
st.caption("Aplikasi Resmi Publikasi Daftar Pemilih Tetap (Tanpa Data Sensitif NIK/KK)")

# Masukkan ID Google Sheet Anda di sini
SHEET_ID = "1Xvi40Xj5MXFLuu5v4mi-wv3Oyfe7dYuyxNKccXbxXV0"

# 3. FITUR 1: TAMPILKAN REKAPITULASI
st.subheader("📊 Rekapitulasi Pemilih")
@st.cache_data(ttl=600)  # Menyimpan cache selama 10 menit agar aplikasi super ringan & cepat
def load_rekap():
    url = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Rekap"
    return pd.read_csv(url)

try:
    df_rekap = load_rekap()
    st.dataframe(df_rekap, use_container_width=True, hide_index=True)
except:
    st.error("Gagal memuat data rekap. Pastikan nama sheet pertama adalah 'Rekap'")

# 4. FITUR 2: PENCARIAN & DETAIL TPS
st.markdown("---")
st.subheader("🔍 Cek Daftar Pemilih Per TPS")

# Membuat daftar pilihan TPS (TPS 001 sampai TPS 011)
tps_list = [f"TPS {str(i).zfill(3)}" for i in range(1, 12)]
pilihan_tps = st.selectbox("Pilih TPS yang ingin dicari:", ["-- Pilih TPS --"] + tps_list)

if pilihan_tps != "-- Pilih TPS --":
    @st.cache_data(ttl=600)
    def load_tps_data(nama_tps):
        # Format nama TPS untuk URL (mengganti spasi dengan %20)
        sheet_name = nama_tps.replace(" ", "%20")
        url = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)
    
    try:
        df_tps = load_tps_data(pilihan_tps)
        
        # Kolom Input Pencarian Nama
        cari_nama = st.text_input(f"Ketik Nama Pemilih di {pilihan_tps}:", "", placeholder="Contoh: Budi Santoso")
        
        if cari_nama:
            # Filter pencarian secara realtime (tidak sensitif huruf besar/kecil)
            df_filtered = df_tps[df_tps['Nama'].str.contains(cari_nama, case=False, na=False)]
            
            if not df_filtered.empty:
                st.success(f"Ditemukan {len(df_filtered)} data cocok:")
                st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            else:
                st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Pastikan penulisan benar atau cek TPS lain.")
        else:
            # Jika kolom pencarian kosong, tampilkan info total dan data awal
            st.info(f"Menampilkan seluruh pemilih di {pilihan_tps} (Total: {len(df_tps)} orang)")
            st.dataframe(df_tps, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Gagal memuat data {pilihan_tps}. Pastikan nama sheet di Google Sheets sama persis dengan pilihan (contoh: TPS 001)")
