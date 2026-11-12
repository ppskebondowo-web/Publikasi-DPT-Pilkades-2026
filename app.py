import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(
    page_title="DPT Pilkades Kebondowo 2026",
    page_icon="🗳️",
    layout="centered"
)

st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Merriweather:wght@700&family=Montserrat:wght@300;400;600;700;800&family=Open+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&family=Poppins:wght@600;700;800&family=Roboto:wght@300;400;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    html, body, [class*="css"], p, div, span, td, th {
        font-family: 'Open Sans', sans-serif;
    }
    
    div[data-testid="stSelectbox"] label p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        font-size: 15px !important;
    }

    div[data-testid="stTextInput"] label p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        font-size: 18px !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] input {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
        line-height: 1.5 !important;
        min-height: 28px !important;
    }
    
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

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextInput"] input::placeholder {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
    }

    [data-testid="InputInstructions"],
    [data-testid="InputInstructions"] *,
    div[data-testid="stForm"] small,
    div[data-testid="stTextInput"] small {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        opacity: 0 !important;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image("logo.png")
img_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 85px; height: auto; margin-bottom: 10px; object-fit: contain;">' if logo_base64 else ''

st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: flex-start; text-align: left; margin-bottom: 18px;">
    {img_html}
    <div style="font-family: 'Open Sans', sans-serif; font-size: 28px; font-weight: 700; margin: 0px 0px 4px 0px; padding: 0px; line-height: 1.15;">
        DAFTAR PEMILIH TETAP
    </div>
    <div style="font-family: 'Open Sans', sans-serif; font-size: 13px; color: gray; line-height: 1.35; margin: 0px; padding: 0px;">
        Aplikasi Resmi Publikasi Daftar Pemilih Tetap<br>
        Pemilihan Kepala Desa Kebondowo Tahun 2026<br>
        © Panitia Pilkades Kebondowo
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_local_csv(filename):
    try:
        # sep=None mendeteksi pemisah titik koma (;) maupun koma (,) secara otomatis
        df = pd.read_csv(filename, sep=None, header=0, dtype=str, encoding='utf-8', on_bad_lines='skip', engine='python')
        df = df.dropna(how='all', axis=0)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception:
        lines = []
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline().strip()
            sep = ';' if ';' in first_line else ','
            header = first_line.split(sep)
            for line in f:
                parts = line.strip().split(sep)
                if len(parts) == len(header):
                    lines.append(parts)
        return pd.DataFrame(lines, columns=header)

st.subheader("📊 Rekapitulasi Pemilih")
if os.path.exists("Rekap.csv"):
    df_rekap = load_local_csv("Rekap.csv")
    
    def format_ribuan(val):
        try:
            num = int(float(str(val).replace('.', '').replace(',', '').strip()))
            return f"{num:,}".replace(",", ".")
        except Exception:
            return val

    for col in ['L', 'P', 'L+P']:
        if col in df_rekap.columns:
            df_rekap[col] = df_rekap[col].apply(format_ribuan)
    
    html_table = '<div style="overflow-x: auto; margin-bottom: 10px;">'
    html_table += '<table style="width: 100%; border-collapse: collapse; font-size: 18px;">'
    html_table += '<thead><tr style="background-color: rgba(128, 128, 128, 0.2);">'
    for col in df_rekap.columns:
        html_table += f'<th style="text-align: center; font-weight: bold; padding: 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{col}</th>'
    html_table += '</tr></thead><tbody>'
    
    for index, row in df_rekap.iterrows():
        is_total = str(row.iloc[0]).strip().lower() == 'total'
        row_style = 'font-weight: bold; background-color: rgba(128, 128, 128, 0.15);' if is_total else ''
        html_table += f'<tr style="{row_style}">'
        for val in row:
            html_table += f'<td style="text-align: center; padding: 7px 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{val}</td>'
        html_table += '</tr>'
    html_table += '</tbody></table></div>'
    
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.error("File 'Rekap.csv' tidak ditemukan.")

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
        st.error(f"File '{csv_file}' belum diunggah ke GitHub.")
    else:
        df_tps = load_local_csv(csv_file)
        kolom_nama = [col for col in df_tps.columns if col.lower() == 'nama']
        
        if not kolom_nama:
            st.error(f"Kolom 'Nama' tidak ditemukan di {pilihan_tps}.")
        else:
            nama_key = kolom_nama[0]
            df_tps[nama_key] = df_tps[nama_key].fillna('').astype(str).str.strip()
            
            with st.form(key=f"form_cari_{pilihan_tps}", border=False):
                cari_nama = st.text_input(
                    f"Ketik Nama yang dicari di {pilihan_tps}:", 
                    "", 
                    placeholder="Contoh: JOHN DOE"
                )
                tombol_cari = st.form_submit_button("🔍 Cari Pemilih", use_container_width=True)
            
            if tombol_cari or cari_nama:
                if cari_nama.strip():
                    df_filtered = df_tps[df_tps[nama_key].str.contains(cari_nama.strip(), case=False, na=False)]
                    
                    if not df_filtered.empty:
                        st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                        
                        for index, row in df_filtered.iterrows():
                            v_nama = row.get('Nama', '-').upper()
                            v_jk = row.get('JnsKlmn', '-')
                            v_alamat = row.get('Alamat', '-')
                            v_id = row.get('ID', '-')
                            
                            # Mencari kolom usia secara fleksibel (mendukung Usia, USIA, Umur, UMUR)
                            v_usia = ''
                            for k in row.index:
                                if k.strip().lower() in ['usia', 'umur']:
                                    v_usia = str(row[k]).strip()
                                    break
                            
                            if v_usia and v_usia != '-' and v_usia.lower() != 'nan':
                                jk_usia_text = f"{v_jk}, {v_usia} tahun"
                            else:
                                jk_usia_text = v_jk
                            
                            import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(
    page_title="DPT Pilkades Kebondowo 2026",
    page_icon="🗳️",
    layout="centered"
)

st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Merriweather:wght@700&family=Montserrat:wght@300;400;600;700;800&family=Open+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&family=Poppins:wght@600;700;800&family=Roboto:wght@300;400;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    html, body, [class*="css"], p, div, span, td, th {
        font-family: 'Open Sans', sans-serif;
    }
    
    div[data-testid="stSelectbox"] label p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        font-size: 15px !important;
    }

    div[data-testid="stTextInput"] label p {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
        font-size: 18px !important;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] input {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
        line-height: 1.5 !important;
        min-height: 28px !important;
    }
    
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

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextInput"] input::placeholder {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 400 !important;
        font-size: 18px !important;
    }

    [data-testid="InputInstructions"],
    [data-testid="InputInstructions"] *,
    div[data-testid="stForm"] small,
    div[data-testid="stTextInput"] small {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        opacity: 0 !important;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image("logo.png")
img_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 85px; height: auto; margin-bottom: 10px; object-fit: contain;">' if logo_base64 else ''

st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: flex-start; text-align: left; margin-bottom: 18px;">
    {img_html}
    <div style="font-family: 'Open Sans', sans-serif; font-size: 28px; font-weight: 700; margin: 0px 0px 4px 0px; padding: 0px; line-height: 1.15;">
        DAFTAR PEMILIH TETAP
    </div>
    <div style="font-family: 'Open Sans', sans-serif; font-size: 13px; color: gray; line-height: 1.35; margin: 0px; padding: 0px;">
        Aplikasi Resmi Publikasi Daftar Pemilih Tetap<br>
        Pemilihan Kepala Desa Kebondowo Tahun 2026<br>
        © Panitia Pilkades Kebondowo
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_local_csv(filename):
    try:
        df = pd.read_csv(filename, sep=None, header=0, dtype=str, encoding='utf-8', on_bad_lines='skip', engine='python')
        df = df.dropna(how='all', axis=0)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception:
        lines = []
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline().strip()
            sep = ';' if ';' in first_line else ','
            header = first_line.split(sep)
            for line in f:
                parts = line.strip().split(sep)
                if len(parts) == len(header):
                    lines.append(parts)
        return pd.DataFrame(lines, columns=header)

st.subheader("📊 Rekapitulasi Pemilih")
if os.path.exists("Rekap.csv"):
    df_rekap = load_local_csv("Rekap.csv")
    
    def format_ribuan(val):
        try:
            num = int(float(str(val).replace('.', '').replace(',', '').strip()))
            return f"{num:,}".replace(",", ".")
        except Exception:
            return val

    for col in ['L', 'P', 'L+P']:
        if col in df_rekap.columns:
            df_rekap[col] = df_rekap[col].apply(format_ribuan)
    
    html_table = '<div style="overflow-x: auto; margin-bottom: 10px;">'
    html_table += '<table style="width: 100%; border-collapse: collapse; font-size: 18px;">'
    html_table += '<thead><tr style="background-color: rgba(128, 128, 128, 0.2);">'
    for col in df_rekap.columns:
        html_table += f'<th style="text-align: center; font-weight: bold; padding: 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{col}</th>'
    html_table += '</tr></thead><tbody>'
    
    for index, row in df_rekap.iterrows():
        is_total = str(row.iloc[0]).strip().lower() == 'total'
        row_style = 'font-weight: bold; background-color: rgba(128, 128, 128, 0.15);' if is_total else ''
        html_table += f'<tr style="{row_style}">'
        for val in row:
            html_table += f'<td style="text-align: center; padding: 7px 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{val}</td>'
        html_table += '</tr>'
    html_table += '</tbody></table></div>'
    
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.error("File 'Rekap.csv' tidak ditemukan.")

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
        st.error(f"File '{csv_file}' belum diunggah ke GitHub.")
    else:
        df_tps = load_local_csv(csv_file)
        kolom_nama = [col for col in df_tps.columns if col.lower() == 'nama']
        
        if not kolom_nama:
            st.error(f"Kolom 'Nama' tidak ditemukan di {pilihan_tps}.")
        else:
            nama_key = kolom_nama[0]
            df_tps[nama_key] = df_tps[nama_key].fillna('').astype(str).str.strip()
            
            with st.form(key=f"form_cari_{pilihan_tps}", border=False):
                cari_nama = st.text_input(
                    f"Ketik Nama yang dicari di {pilihan_tps}:", 
                    "", 
                    placeholder="Contoh: BARRU LINGGANATUR"
                )
                tombol_cari = st.form_submit_button("🔍 Cari Pemilih", use_container_width=True)
            
            if tombol_cari or cari_nama:
                if cari_nama.strip():
                    df_filtered = df_tps[df_tps[nama_key].str.contains(cari_nama.strip(), case=False, na=False)]
                    
                    if not df_filtered.empty:
                        st.success(f"Ditemukan {len(df_filtered)} data yang cocok:")
                        
                        for index, row in df_filtered.iterrows():
                            v_nama = row.get('Nama', '-').upper()
                            v_jk = row.get('JnsKlmn', '-')
                            v_alamat = row.get('Alamat', '-')
                            v_id = row.get('ID', '-')
                            
                            # Pencarian kolom Usia/Umur secara otomatis
                            v_usia = ''
                            for k in row.index:
                                if k.strip().lower() in ['usia', 'umur']:
                                    v_usia = str(row[k]).strip()
                                    break
                            
                            if v_usia and v_usia != '-' and v_usia.lower() != 'nan':
                                jk_usia_text = f"{v_jk}, {v_usia} tahun"
                            else:
                                jk_usia_text = v_jk
                            
                            # Desain Kartu Rata Tengah (Center) Persis Sesuai Gambar Contoh
                            html_card = f'<div style="text-align: center; padding: 8px 0;"><div style="font-family: \'Roboto\', sans-serif; font-size: 28px; font-weight: 400; line-height: 1.2; margin-bottom: 4px;">{v_nama}</div><div style="font-size: 16px; font-style: italic; line-height: 1.3; margin-bottom: 3px;">{jk_usia_text}</div><div style="font-size: 16px; line-height: 1.3; margin-bottom: 5px;">{v_alamat}</div><div style="font-family: \'OCR A Extended\', \'OCR-A\', \'Share Tech Mono\', monospace; font-size: 19px; font-weight: 400; letter-spacing: 1px; line-height: 1.3;"><span style="font-family: sans-serif; letter-spacing: 0;">🆔</span> {v_id}</div></div><hr style="margin: 10px 0; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">'
                            st.markdown(html_card, unsafe_allow_html=True)
                   
                    else:
                        st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}.")
                else:
                    st.warning("Silakan ketikkan nama terlebih dahulu.")
            else:
                st.info("Ketik nama pemilih di atas lalu tekan tombol 🔍 Cari Pemilih.")

# --- SELESAI ---
