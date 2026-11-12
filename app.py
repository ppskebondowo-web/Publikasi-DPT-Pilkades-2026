import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="DPT Pilkades Kebondowo 2026", page_icon="🗳️", layout="centered")

st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Montserrat:wght@300;400;600;700&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400&family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    html, body, [class*="css"], p, div, span, td, th { font-family: 'Open Sans', sans-serif; }
    div[data-testid="stSelectbox"] label p { font-family: 'Montserrat_Lokal', sans-serif !important; font-size: 12px !important; }
    div[data-testid="stTextInput"] label p { font-family: 'Montserrat_Lokal', sans-serif !important; font-size: 12px !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"],
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
    div[data-baseweb="popover"] li, [role="option"] { font-size: 18px !important; padding: 8px !important; }
    div[data-testid="stTextInput"] input { font-size: 18px !important; }
    [data-testid="InputInstructions"], div[data-testid="stForm"] small { display: none !important; }
    </style>
""", unsafe_allow_html=True)

if os.path.exists("ocra.ttf"):
    with open("ocra.ttf", "rb") as f:
        font_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"<style>@font-face {{ font-family: 'OCRA_Lokal'; src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}</style>", unsafe_allow_html=True)

if os.path.exists("montserrat.ttf"):
    with open("montserrat.ttf", "rb") as f:
        mont_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"<style>@font-face {{ font-family: 'Montserrat_Lokal'; src: url(data:font/ttf;base64,{mont_b64}) format('truetype'); }}</style>", unsafe_allow_html=True)

if os.path.exists("saira.ttf"):
    with open("saira.ttf", "rb") as f:
        siera_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"<style>@font-face {{ font-family: 'Siera_Lokal'; src: url(data:font/ttf;base64,{siera_b64}) format('truetype'); }}</style>", unsafe_allow_html=True)

logo_b64 = base64.b64encode(open("logo.png", "rb").read()).decode() if os.path.exists("logo.png") else None
img_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 85px; margin-bottom: 10px;">' if logo_b64 else ''

st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: flex-start; text-align: left; margin-bottom: 18px;">
    {img_html}
    <div style="font-size: 28px; font-weight: 700; margin-bottom: 4px; line-height: 1.15;">DAFTAR PEMILIH TETAP</div>
    <div style="font-size: 13px; color: gray; line-height: 1.35;">
        Aplikasi Resmi Publikasi Daftar Pemilih Tetap<br>
        Pemilihan Kepala Desa Kebondowo Tahun 2026<br>
        © Panitia Pilkades Kebondowo
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_local_csv(filename):
    df = pd.read_csv(filename, sep=None, header=0, dtype=str, encoding='utf-8', on_bad_lines='skip', engine='python')
    df = df.dropna(how='all', axis=0)
    df.columns = df.columns.str.strip()
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]


st.subheader("📊 Rekapitulasi Pemilih")
if os.path.exists("Rekap.csv"):
    df_rekap = load_local_csv("Rekap.csv")
    for col in ['L', 'P', 'L+P']:
        if col in df_rekap.columns:
            df_rekap[col] = df_rekap[col].apply(lambda x: f"{int(float(str(x).replace('.', '').strip())):,}".replace(",", ".") if str(x).replace('.', '').strip().isdigit() else x)
    
    html_table = '<div style="overflow-x: auto; margin-bottom: 10px;"><table style="width: 100%; border-collapse: collapse; font-size: 18px;">'
    html_table += '<thead><tr style="background-color: rgba(128, 128, 128, 0.2);">' + ''.join([f'<th style="text-align: center; font-weight: bold; padding: 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{c}</th>' for c in df_rekap.columns]) + '</tr></thead><tbody>'
    for _, row in df_rekap.iterrows():
        is_total = str(row.iloc[0]).strip().lower() == 'total'
        style = 'font-weight: bold; background-color: rgba(128, 128, 128, 0.15);' if is_total else ''
        html_table += f'<tr style="{style}">' + ''.join([f'<td style="text-align: center; padding: 7px 8px; border: 1px solid rgba(128, 128, 128, 0.3);">{v}</td>' for v in row]) + '</tr>'
    st.markdown(html_table + '</tbody></table></div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("🔍 Cek Data Pemilih")
tps_list = ["TPS 001", "TPS 002", "TPS 003", "TPS 004", "TPS 005", "TPS 006", "TPS 007", "TPS 008", "TPS 009", "TPS 010", "TPS 011"]
pilihan_tps = st.selectbox("Pilih nomor TPS terlebih dahulu:", ["-- Pilih TPS --"] + tps_list)

if pilihan_tps != "-- Pilih TPS --":
    csv_file = f"{pilihan_tps}.csv"
    if os.path.exists(csv_file):
        df_tps = load_local_csv(csv_file)
        nama_col = next((c for c in df_tps.columns if c.lower() == 'nama'), None)
        if nama_col:
            with st.form(key=f"form_{pilihan_tps}", border=False):
                cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: BARRU LINGGANATUR")
                tombol_cari = st.form_submit_button("🔍 Cari Pemilih", use_container_width=True)
            if tombol_cari or cari_nama:
                if cari_nama.strip():
                    hasil = df_tps[df_tps[nama_col].str.contains(cari_nama.strip(), case=False, na=False)]
                    if not hasil.empty:
                        st.success(f"Ditemukan {len(hasil)} data yang cocok:")
                        for _, row in hasil.iterrows():
                            v_nama = str(row.get('Nama', '-')).upper()
                            v_jk = row.get('JnsKlmn', '-')
                            v_alamat = row.get('Alamat', '-')
                            v_id = row.get('ID', '-')
                            v_usia = next((str(row[k]).strip() for k in row.index if k.strip().lower() in ['usia', 'umur']), '')
                            jk_usia = f"{v_jk}, {v_usia} tahun" if v_usia and v_usia.lower() not in ['-', 'nan', ''] else v_jk
                            st.markdown(f'<div style="text-align: center; padding: 8px 0;"><div style="font-family: \'Siera_Lokal\', \'Roboto\', sans-serif; font-size: 30px; line-height: 1.2; margin-bottom: 4px;">{v_nama}</div><div style="font-size: 16px; font-style: italic; margin-bottom: 3px;">{jk_usia}</div><div style="font-size: 16px; margin-bottom: 5px;">{v_alamat}</div><div style="font-family: \'OCRA_Lokal\', \'OCR A Extended\', monospace; font-size: 19px; letter-spacing: 1px;"><span style="font-family: sans-serif; letter-spacing: 0;">🆔</span>{v_id}</div></div><hr style="margin: 10px 0; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">', unsafe_allow_html=True)
                    else:
                        st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}.")
                else:
                    st.warning("Silakan ketikkan nama terlebih dahulu.")
            else:
                st.info("Ketik nama pemilih di atas lalu tekan tombol 🔍 Cari Pemilih.")
# --- SELESAI ---
