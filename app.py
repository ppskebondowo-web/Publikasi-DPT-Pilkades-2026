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
    #MainMenu, footer, header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    
    /* Memangkas habis padding atas wadah utama Streamlit */
    .block-container,
    div[data-testid="stAppViewBlockContainer"],
    section.main > div {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

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
    div[data-testid="stTextInput"] input::placeholder {
    font-size: 14px !important;
    opacity: 0.75 !important;
}
    [data-testid="InputInstructions"], div[data-testid="stForm"] small { display: none !important; }
    
    a.tombol-tps-kustom {
        display: block;
        width: 100%;
        padding: 10px 14px;
        margin-bottom: 10px;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.35);
        background-color: rgba(128, 128, 128, 0.08);
        text-decoration: none !important;
        color: inherit !important;
        text-align: center;
        transition: background-color 0.2s;
    }
    a.tombol-tps-kustom:hover, a.tombol-tps-kustom:active {
        background-color: rgba(128, 128, 128, 0.2);
        border-color: rgba(128, 128, 128, 0.6);
    }
        /* Membesarkan label judul dan tulisan opsi radio button (Semua, Laki-laki, Perempuan) */
    div[data-testid="stRadio"] > label p {
        font-size: 16px !important;
        font-weight: 100 !important;
        font-style: italic !important;
        margin-bottom: 6px !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 16px !important;
        font-weight: 100 !important;
    }

    /* Membesarkan lingkaran tombol radio agar mudah disentuh jari */
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 18px !important;
        font-weight: 100 !important; /* Ubah angka ini sesuai selera ketebalan */
    }

    /* Memberi jarak antar opsi agar tidak berdempetan saat diketuk */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 18px !important;
    }

    </style>
""", unsafe_allow_html=True)

font_files = [
    ("OCRA_Lokal", "ocra.ttf", "truetype", "ttf"),
    ("Montserrat_Lokal", "montserrat.ttf", "truetype", "ttf"),
    ("Siera_Lokal", "saira.ttf", "truetype", "ttf"),
    ("Stillfish_Lokal", "mdsl.otf", "opentype", "otf"),
    ("StillfishIt_Lokal", "StlfRgIt.otf", "opentype", "otf"),
    ("Oswald_Lokal", "oswldr.ttf", "truetype", "ttf")
]

for f_name, f_file, f_format, f_mime in font_files:
    if os.path.exists(f_file):
        with open(f_file, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode()
        st.markdown(f"<style>@font-face {{ font-family: '{f_name}'; src: url(data:font/{f_mime};base64,{b64_data}) format('{f_format}'); }}</style>", unsafe_allow_html=True)

logo_b64 = base64.b64encode(open("logo.png", "rb").read()).decode() if os.path.exists("logo.png") else None
img_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 85px; margin-bottom: 10px;">' if logo_b64 else ''

st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: flex-start; text-align: left; margin-top: -100px; margin-bottom: 18px;">
    {img_html}
    <div style="font-size: 28px; font-weight: 700; margin-bottom: 4px; line-height: 1.15;">DAFTAR PEMILIH TETAP</div>
    <div style="font-size: 14px; color: gray; line-height: 1.35;">
        Publikasi Resmi Daftar Pemilih Tetap<br>
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

tps_terklik = st.query_params.get("tps_klik", None)

if tps_terklik:
    col_judul, col_tutup = st.columns([3, 1.3])
    with col_judul:
        st.markdown(f'<div style="font-size: 24px; font-weight: 400; padding-top: 8px; line-height: 1.2;">Pemilih di {tps_terklik}</div>', unsafe_allow_html=True)
    with col_tutup:
        if st.button("⬅️ Kembali", use_container_width=True):
            st.query_params.clear()
            st.rerun()
            
    csv_klik = f"{tps_terklik}.csv"
    if os.path.exists(csv_klik):
        df_semua = load_local_csv(csv_klik)
        nama_col_klik = next((c for c in df_semua.columns if c.lower() == 'nama'), None)
        jk_col_klik = next((c for c in df_semua.columns if 'jns' in c.lower() or 'kelamin' in c.lower()), None)
        
        pilihan_jk = st.radio(
            "Tampilkan kategori pemilih:",
            ["Semua", "Laki-laki", "Perempuan"],
            horizontal=True
        )
        
        with st.form(key=f"form_cepat_{tps_terklik}", border=False):
            filter_cepat = st.text_input(
                f"Cari nama di {tps_terklik}:", 
                "", 
                placeholder="Ketik nama lalu tekan Saring (kosongkan untuk semua)"
            )
            tombol_cepat = st.form_submit_button("🔍 Saring Data", use_container_width=True)
            
        df_tampil = df_semua.copy()
        
        if pilihan_jk != "Semua" and jk_col_klik:
            df_tampil = df_tampil[df_tampil[jk_col_klik].str.strip().str.lower() == pilihan_jk.lower()]
            
        if filter_cepat.strip() and nama_col_klik:
            df_tampil = df_tampil[df_tampil[nama_col_klik].str.contains(filter_cepat.strip(), case=False, na=False)]
            
        # Keterangan jumlah data yang tampil sesuai pilihan kategori (Semua / Laki-laki / Perempuan)
        if not df_tampil.empty:
            if pilihan_jk == "Laki-laki":
                teks_kategori = "pemilih laki-laki"
            elif pilihan_jk == "Perempuan":
                teks_kategori = "pemilih perempuan"
            else:
                teks_kategori = "semua pemilih"

            if filter_cepat.strip():
                st.success(f"Ditemukan **{len(df_tampil)}** {teks_kategori} dengan nama '{filter_cepat.strip()}' di **{tps_terklik}**:")
            else:
                st.info(f"Menampilkan {teks_kategori} di **{tps_terklik}** (Total: **{len(df_tampil)}** pemilih)")

            semua_kartu_html = ""
            for _, row in df_tampil.iterrows():
                v_nama = str(row.get('Nama', '-')).upper()
                v_jk = row.get('JnsKlmn', '-')
                v_alamat = row.get('Alamat', '-')
                v_id = row.get('ID', '-')
                v_usia = next((str(row[k]).strip() for k in row.index if k.strip().lower() in ['usia', 'umur']), '')
                jk_usia = f"{v_jk}, {v_usia} tahun" if v_usia and v_usia.lower() not in ['-', 'nan', ''] else v_jk
                semua_kartu_html += f'<div style="text-align: center; padding: 8px 0;"><div style="font-family: \'Siera_Lokal\', sans-serif; font-size: 30px; line-height: 1.2; margin-bottom: 4px;">{v_nama}</div><div style="font-size: 16px; font-style: italic; margin-bottom: 3px;">{jk_usia}</div><div style="font-family: \'Stillfish_Lokal\', sans-serif; font-size: 17px; margin-bottom: 5px;">{v_alamat}</div><div style="font-family: \'OCRA_Lokal\', \'OCR A Extended\', monospace; font-size: 19px; letter-spacing: 1px;"><span style="font-family: sans-serif; letter-spacing: 0;">🆔</span>{v_id}</div></div><hr style="margin: 10px 0; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">'
            st.markdown(semua_kartu_html, unsafe_allow_html=True)
        else:
            st.warning(f"Data pemilih kategori **{pilihan_jk}** tidak ditemukan di {tps_terklik}.")
    else:
        st.error(f"File '{csv_klik}' tidak ditemukan di GitHub.")

else:
    st.subheader("📊 Rekap Pemilih")
    if os.path.exists("Rekap.csv"):
        df_rekap = load_local_csv("Rekap.csv")
        
        peta_dict = {}
        if os.path.exists("PetaPemilih.csv"):
            df_peta = load_local_csv("PetaPemilih.csv")
            col_tps = next((c for c in df_peta.columns if c.strip().lower() == 'tps'), None)
            col_asal = next((c for c in df_peta.columns if 'asal' in c.strip().lower()), None)
            
            if col_tps and col_asal:
                for _, r_peta in df_peta.iterrows():
                    tps_key = str(r_peta.get(col_tps, '')).strip().upper()
                    asal_val = str(r_peta.get(col_asal, '')).strip()
                    if tps_key and asal_val and asal_val.lower() != 'nan':
                        peta_dict[tps_key] = f"{peta_dict[tps_key]}, {asal_val}" if tps_key in peta_dict else asal_val
        
        def fmt_angka(val):
            s = str(val).replace('.', '').strip()
            return f"{int(float(s)):,}".replace(",", ".") if s.isdigit() else val

        for idx, row in df_rekap.iterrows():
            nama_tps = str(next(iter(row.values))).strip()
            val_l = fmt_angka(row.get('L', '0'))
            val_p = fmt_angka(row.get('P', '0'))
            val_total = fmt_angka(row.get('L+P', '0'))
            
            if nama_tps.lower() == 'total':
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; margin-top: 6px; margin-bottom: 14px; border-radius: 8px; background-color: rgba(128, 128, 128, 0); border: 1px solid rgba(128, 128, 128, 0.3); font-size: 16px;">
                    <strong>TOTAL KESELURUHAN: {val_total} Pemilih</strong><br>
                    <span style="font-size: 13px; opacity: 0.85;">Laki-laki: {val_l} &nbsp;|&nbsp; Perempuan: {val_p}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                info_wilayah = peta_dict.get(nama_tps.upper(), "-")
                html_btn = f'<a href="?tps_klik={nama_tps}" target="_self" class="tombol-tps-kustom"><span style="display: block; line-height: 1.25; margin-bottom: 3px;"><span style="font-family: \'Siera_Lokal\', sans-serif; font-size: 20px;">{nama_tps} ({val_total}): {val_l}</span><span style="font-size: 10px; opacity: 0.85;"> laki-laki &nbsp;</span><span style="font-family: \'Siera_Lokal\', sans-serif; font-size: 18px;">{val_p}</span><span style="font-size: 10px; opacity: 0.85;"> perempuan</span></span><span style="display: block; font-size: 14px; opacity: 0.9;">{info_wilayah}</span></a>'
                st.markdown(html_btn, unsafe_allow_html=True)

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
                    cari_nama = st.text_input(f"Ketik Nama yang dicari di {pilihan_tps}:", "", placeholder="Contoh: BUDI LUHUR")
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
                                st.markdown(f'<div style="text-align: center; padding: 8px 0;"><div style="font-family: \'Siera_Lokal\', sans-serif; font-size: 30px; line-height: 1.2; margin-bottom: 4px;">{v_nama}</div><div style="font-size: 16px; font-style: italic; margin-bottom: 3px;">{jk_usia}</div><div style="font-family: \'Stillfish_Lokal\', sans-serif; font-size: 17px; margin-bottom: 5px;">{v_alamat}</div><div style="font-family: \'OCRA_Lokal\', \'OCR A Extended\', monospace; font-size: 19px; letter-spacing: 1px;"><span style="font-family: sans-serif; letter-spacing: 0;">🆔</span>{v_id}</div></div><hr style="margin: 10px 0; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.3);">', unsafe_allow_html=True)
                        else:
                            st.warning(f"Nama '{cari_nama}' tidak ditemukan di {pilihan_tps}.")
                    else:
                        st.warning("Silakan ketikkan nama terlebih dahulu.")
                else:
                    st.info("Ketik nama pemilih di atas lalu tekan tombol 🔍 Cari Pemilih.")

# --- SELESAI ---
