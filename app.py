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

# 2. Judul Utama Aplikasi Web
st.title("🗳️ DPT ONLINE PILKADES 2026")
st.caption("Aplikasi Resmi Publikasi Daftar Pemilih Tetap (Tanpa Data Sensitif NIK/KK)")

# Fungsi membaca data lokal CSV secara instan (100% Kebal Eror Jaringan)
@st.cache_data
def load_local_csv(filename):
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

# 4. FITUR 2: PENCARIAN DATA PER TPS (Tanpa Pratinjau Tabel & Menggunakan Kustom Font)
st.markdown("---")
st.subheader("🔍 Cek Daftar Pemilih Per TPS")

# Pemetaan Nama Pilihan ke Nama File CSV Asli Anda (Menggunakan Spasi, bukan Underscore)
tps_options = {
    "TPS 001": "TPS 001.csv",
    "TPS 002": "TPS 002.csv",
    "TPS 003": "TPS 003.csv",
    "TPS 004": "TPS 004.csv",
    "TPS 005": "TPS 005.csv",
    "TPS 006": "TPS 006.csv",
    "TPS 007": "TPS 007.csv",
    "TPS 008": "TPS 008.csv",
    "TPS 009": "TPS 009.csv",
    "TPS 010": "TPS 010.csv",
    "TPS 011": "TPS 011.csv"
}

pilihan_tps = st.selectbox("Pilih nomor TPS terlebih dahulu:", ["-- Pilih TPS --"] + list(tps_options.keys()))

if pilihan_tps != "-- Pilih TPS --":
    csv_file = tps_options[pilihan_tps]
    
    if not os.path.exists(csv_file):
        st.error(f"File '{csv_file}' belum diunggah ke GitHub Anda. Pastikan nama file menggunakan spasi, bukan garis bawah.")
    else:
        try:
            df_tps = load_local_csv(csv_file)
            
            # Deteksi otomatis kolom Nama (toleransi huruf besar/kecil)
            kolom_nama = [col for col in df_tps.columns if col.lower() == 'nama']
            
            if not kolom_nama:
                st.error(f"Eror Struktur: Kolom dengan nama 'Nama' tidak ditemukan di {pilihan_tps}.")
            else:
                nama_key = kolom_nama[0]
                df_tps[nama_key] = df_tps[nama_key].fillna('').astype(str).str.strip()
                
                # Kolom Input Pencarian Nama bagi Warga
                cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: GITA ARYU")
                
                if cari_nama:
                    # Filter pencarian nama (case-insensitive)
                    df_filtered = df_tps[df_tps[nama_key].str.contains(cari_nama, case=False, na=False)]
                    
                    if not df_filtered.empty:
                        st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                        
                        # FORMAT OUTPUT: Desain Kartu Kustom Font & Pemisahan Emoji Anti-Error
                        for index, row in df_filtered.iterrows():
                            v_nama = row.get('Nama', '-').upper()
                            v_jk = row.get('JnsKlmn', '-')
                            v_alamat = row.get('Alamat', '-')
                            v_id = row.get('ID', '-')
                            
                            # 1. Tampilan Nama Pemilih (Besar, Tebal, Font Modern Sans-Serif)
                            st.markdown("###")
                            st.markdown(f"""
                            <div style="font-family: 'Arial Black', Gadget, sans-serif; font-size: 24px; margin-top: -40px; margin-bottom: 10px;">
                                {v_nama}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 2. Tampilan Jenis Kelamin (Italic) & Alamat
                            st.markdown(f"👤 *{v_jk}*")
                            st.markdown(f"📍 {v_alamat}")
                            
                            # 3. Tampilan ID (Font Tebal Bergaya Kode Monospace)
                            st.markdown("🆔")
                            st.markdown(f"""
                            <div style="font-family: 'Courier New', Courier, monospace; font-size: 18px; font-weight: bold; margin-top: -40px;">
                                {v_id}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("---") # Garis pembatas tipis antar nama
                                
                    else:
                        st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Periksa ejaan kembali.")
                else:
                    # Tampilan bersih jika belum mengetik nama
                    st.info(f"Silakan ketik nama pemilih pada kolom di atas untuk mencari data di {pilihan_tps}.")
                
        except Exception as e:
            st.error(f"Gagal memuat data lokal untuk {pilihan_tps}. Periksa format struktur file CSV tersebut.")
