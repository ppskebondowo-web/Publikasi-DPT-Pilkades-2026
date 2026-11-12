import streamlit as st
import pandas as pd
import os

# 1. Konfigurasi Tampilan untuk HP Android agar Modern & Responsif
st.set_page_config(
    page_title="DPT Pilkades 2026", 
    page_icon="", 
    layout="centered"
)

# 1. Memuat Google Fonts (Menambahkan Montserrat varian 300/Light)
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Merriweather:wght@700&family=Montserrat:wght@300;400;600;700;800&family=Open+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&family=Poppins:wght@600;700;800&family=Roboto:wght@400;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 2. Style CSS Kustom
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Menerapkan Open Sans sebagai font dasar */
    html, body, [class*="css"], p, div, span, td, th {
        font-family: 'Open Sans', sans-serif;
    }
    
    /* Label 'Pilih nomor TPS terlebih dahulu:' & 'Ketik Nama...' -> Montserrat Light (300) ukuran 18px */
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stTextInput"] label p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        font-size: 18px !important;
    }
    
        /* Kotak Dropdown TPS ('TPS 006') -> Memaksa semua teks di dalamnya menjadi 18px */
    div[data-testid="stSelectbox"] div[data-baseweb="select"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
    div[data-baseweb="select"] [value] {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
        line-height: 1.4 !important;
    }

    
    /* Daftar pilihan saat menu dropdown TPS dibuka -> Ukuran 18px */
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] div,
    ul[role="listbox"] li,
    [role="option"] {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }

    /* Kotak Input Nama ('Contoh: JOHN DOE' & teks ketikan) -> Disamakan ukurannya menjadi 18px */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextInput"] input::placeholder {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. Judul Utama Aplikasi Web
st.title("DAFTAR PEMILIH TETAP")
st.markdown("""
<div style="font-family: 'Roboto', sans-serif; font-size: 16px; color: gray; line-height: 1.4; margin-top: -10px; margin-bottom: 15px;">
    Aplikasi Resmi Publikasi Daftar Pemilih Tetap<br>
    Pemilihan Kepala Desa Kebondowo Tahun 2026<br>
    © Panitia Pilkades Kebondowo
</div>
""", unsafe_allow_html=True)

# Fungsi membaca data lokal CSV secara instan dengan proteksi kerusakan baris teks
@st.cache_data
def load_local_csv(filename):
    try:
        df = pd.read_csv(filename, header=0, dtype=str, encoding='utf-8', on_bad_lines='skip', engine='python')
        df = df.dropna(how='all', axis=0)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        lines = []
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            header = f.readline().strip().split(',')
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == len(header):
                    lines.append(parts)
        return pd.DataFrame(lines, columns=header)

# 3. FITUR 1: TAMPILKAN REKAPITULASI (Header Center & Tebal + Titik Ribuan)
st.subheader("📊 Rekapitulasi Pemilih")
try:
    if os.path.exists("Rekap.csv"):
        df_rekap = load_local_csv("Rekap.csv")
        
        # Fungsi otomatis untuk menambahkan titik pemisah ribuan pada angka
        def format_ribuan(val):
            try:
                num = int(float(str(val).replace('.', '').replace(',', '').strip()))
                return f"{num:,}".replace(",", ".")
            except:
                return val

        # Terapkan pemisah titik ke kolom L, P, dan L+P
        for col in ['L', 'P', 'L+P']:
            if col in df_rekap.columns:
                df_rekap[col] = df_rekap[col].apply(format_ribuan)
        
        # Membangun Tabel HTML Kustom agar Header Center & Tebal
        html_table = '<div style="overflow-x: auto; margin-bottom: 10px;">'
        html_table += '<table style="width: 100%; border-collapse: collapse; font-size: 18px;">'
        
        # Bagian Header (Center & Tebal)
        html_table += '<thead><tr style="background-color: rgba(128, 128, 128, 0.2);">'
        for col in df_rekap.columns:
            html_table += f'<th style="text-align: center; font-weight: bold; padding: 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{col}</th>'
        html_table += '</tr></thead>'
        
        # Bagian Isi Tabel (Semua Sel Rata Tengah / Center)
        html_table += '<tbody>'
        for index, row in df_rekap.iterrows():
            # Mengecek apakah baris ini adalah baris 'Total' untuk dicetak tebal
            is_total = str(row.iloc[0]).strip().lower() == 'total'
            row_style = 'font-weight: bold; background-color: rgba(128, 128, 128, 0.15);' if is_total else ''
            
            html_table += f'<tr style="{row_style}">'
            for val in row:
                html_table += f'<td style="text-align: center; padding: 7px 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{val}</td>'
            html_table += '</tr>'
        html_table += '</tbody></table></div>'


        
        st.markdown(html_table, unsafe_allow_html=True)
    else:
        st.error("File 'Rekap.csv' tidak ditemukan di server aplikasi. Pastikan Anda sudah mengunggahnya ke GitHub.")
except Exception as e:
    st.error("Gagal memproses data Rekapitulasi lokal.")



# 4. FITUR 2: PENCARIAN DATA PER TPS
st.markdown("---")
st.subheader("🔍 Cek Data Pemilih")

tps_options = {
    "TPS 001": "TPS 001.csv", "TPS 002": "TPS 002.csv", "TPS 003": "TPS 003.csv",
    "TPS 004": "TPS 004.csv", "TPS 005": "TPS 005.csv", "TPS 006": "TPS 006.csv",
    "TPS 007": "TPS 007.csv", "TPS 008": "TPS 008.csv", "TPS 009": "TPS 009.csv",
    "TPS 010": "TPS 010.csv", "TPS 011": "TPS 011.csv"
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
                
                            # Membungkus kotak pencarian dengan st.form agar tulisan "Press Enter to apply" hilang & diganti tombol
                with st.form(key=f"form_cari_{pilihan_tps}", border=False):
                    cari_nama = st.text_input(
                        f"Ketik Nama yang dicari di {pilihan_tps}:", 
                        "", 
                        placeholder="Contoh: JOHN DOE"
                    )
                    # Tombol pencarian yang nyaman diketuk di layar HP
                    tombol_cari = st.form_submit_button("🔍 Cari Pemilih", use_container_width=True)
                
                if tombol_cari or cari_nama:
                    if cari_nama.strip():
                        # Filter pencarian nama (case-insensitive)
                        df_filtered = df_tps[df_tps[nama_key].str.contains(cari_nama.strip(), case=False, na=False)]
                        
                        if not df_filtered.empty:
                            st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                            
                            for index, row in df_filtered.iterrows():
                                v_nama = row.get('Nama', '-').upper()
                                v_jk = row.get('JnsKlmn', '-')
                                v_alamat = row.get('Alamat', '-')
                                v_id = row.get('ID', '-')
                                
                                html_card = f'<div style="padding: 2px 0;"><div style="font-family: \'Arial Black\', Gadget, sans-serif; font-size: 20px; font-weight: bold; line-height: 1.2; margin-bottom: 4px;"><span style="font-family: sans-serif;">📋</span> {v_nama}</div><div style="font-size: 15px; line-height: 1.3; margin-bottom: 2px;">👤 <span style="font-style: italic;">{v_jk}</span></div><div style="font-size: 15px; line-height: 1.3; margin-bottom: 3px;">📍 {v_alamat}</div><div style="font-family: \'OCR A Extended\', \'OCR-A\', Courier, monospace; font-size: 16px; font-weight: bold; line-height: 1.2;"><span style="font-family: sans-serif;">🆔</span> {v_id}</div></div><hr style="margin: 8px 0; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">'
                                
                                st.markdown(html_card, unsafe_allow_html=True)
                                    
                        else:
                            st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Periksa ejaan kembali.")
                    else:
                        st.warning("Silakan ketikkan nama terlebih dahulu sebelum menekan tombol cari.")
                else:
                    st.info(f"Ketik nama pemilih pada kolom di atas lalu tekan tombol 🔍 Cari Pemilih.")

                            
                            # HTML 1 baris penuh untuk mengunci jarak rapat antara garis, nama, dan elemen bawahnya
                            html_card = f'<div style="padding: 2px 0;"><div style="font-family: \'Roboto\', Gadget, sans-serif; font-size: 28px; font-weight: light; line-height: 1.2; margin-bottom: 6px;"><span style="font-family: sans-serif;">{v_nama}</div><div style="font-size: 16px; line-height: 1.3; margin-bottom: 7px;">👤 <span style="font-style: italic;">{v_jk}</span></div><div style="font-size: 16px; line-height: 1.3; margin-bottom: 7px;">📍 {v_alamat}</div><div style="font-family: \'OCR A Extended\', \'OCR-A\', Courier, monospace; font-size: 18px; font-weight: regular; line-height: 1.3;"><span style="font-family: sans-serif;">🆔</span>{v_id}</div></div><hr style="margin: 8px 0; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">'
                            
                            st.markdown(html_card, unsafe_allow_html=True)
                                
                    else:
                        st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}. Periksa ejaan kembali.")
                else:
                    st.info(f"Silakan ketik nama pemilih pada kolom di atas untuk mencari data di {pilihan_tps}.")
                
        except Exception as e:
            st.error(f"Gagal memuat data lokal untuk {pilihan_tps}. Pastikan struktur dalam file CSV sudah benar.")
