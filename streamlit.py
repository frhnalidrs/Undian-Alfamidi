"""
Alfamidi Lucky Draw - Sistem Undian Karyawan PT Midi Utama Indonesia Tbk
Aplikasi Undian Doorprize Berkapasitas Puluhan Ribu Peserta
Format Streamlit Python untuk kemudahan deploy di Streamlit Cloud, HuggingFace, atau Server Lokal.

Cara Menjalankan:
1. pip install -r requirements.txt
2. streamlit run streamlit.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import re
import time
import json
import requests
from datetime import datetime

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA ALFAMIDI
# ==============================================================================
st.set_page_config(
    page_title="Alfamidi Lucky Draw - Undian Karyawan",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling bertema Alfamidi (Merah #d71920, Emas #ffcc00, dan Airmail Envelope)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus+Jakarta+Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #b91c1c 0%, #991b1b 50%, #7f1d1d 100%);
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 16px 24px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .alfamidi-badge {
        background-color: #d71920;
        color: white;
        font-weight: 900;
        font-size: 26px;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #fef08a;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-right: 14px;
    }
    
    .slot-chassis {
        background: linear-gradient(180deg, #991b1b 0%, #7f1d1d 50%, #450a0a 100%);
        border: 4px solid #f59e0b;
        border-radius: 24px;
        padding: 24px;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        margin-bottom: 24px;
    }
    
    .slot-marquee {
        background: linear-gradient(90deg, #d97706, #fbbf24, #d97706);
        color: #0f172a;
        font-weight: 900;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        font-size: 22px;
        text-transform: uppercase;
        margin-bottom: 16px;
        border: 2px solid #fef3c7;
        letter-spacing: 1px;
    }
    
    .slot-reel-box {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        border: 3px solid #f59e0b;
        border-radius: 16px;
        padding: 18px;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 6px 15px rgba(0,0,0,0.8);
        text-align: center;
    }
    
    .reel-winner-title {
        color: #ef4444;
        font-size: 22px;
        font-weight: 900;
        text-transform: uppercase;
        line-height: 1.2;
    }
    
    .reel-winner-subtitle {
        color: #334155;
        font-size: 13px;
        font-weight: 700;
        margin-top: 4px;
    }
    
    .vintage-envelope {
        background: #fdfaf3;
        border: 12px solid transparent;
        border-image: repeating-linear-gradient(135deg, #d71920 0, #d71920 18px, transparent 18px, transparent 24px, #1e40af 24px, #1e40af 42px, transparent 42px, transparent 48px) 18;
        border-radius: 12px;
        padding: 24px;
        color: #1e293b;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin-top: 15px;
    }
    
    .vintage-stamp {
        background-color: #991b1b;
        color: white;
        padding: 8px 12px;
        border: 2px dashed #fde047;
        border-radius: 4px;
        text-align: center;
        display: inline-block;
        font-weight: 800;
        font-size: 11px;
    }
    
    .winner-card {
        background: #ffffff;
        border: 1px solid #fee2e2;
        border-left: 5px solid #d71920;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Tombol Merah Khas Mesin Undian */
    div.stButton > button:first-child {
        background: linear-gradient(180deg, #ef4444 0%, #dc2626 50%, #991b1b 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        padding: 12px 28px !important;
        border-radius: 14px !important;
        border: 2px solid #fde047 !important;
        box-shadow: 0 6px 0 #7f1d1d, 0 10px 20px rgba(220,38,38,0.5) !important;
        transition: all 0.15s ease !important;
        width: 100% !important;
        text-transform: uppercase !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 0 #7f1d1d, 0 14px 25px rgba(220,38,38,0.7) !important;
    }
    div.stButton > button:first-child:active {
        transform: translateY(4px) !important;
        box-shadow: 0 2px 0 #7f1d1d, 0 5px 10px rgba(220,38,38,0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. STATE INITIALIZATION (SESSION STATE)
# ==============================================================================
if "candidates_df" not in st.session_state:
    st.session_state.candidates_df = None

if "categories" not in st.session_state:
    st.session_state.categories = [
        {"name": "Grand Prize - Sepeda Motor Honda Beat", "count": 1},
        {"name": "Hadiah Utama 1 - Smart TV 55 Inch & iPhone", "count": 3},
        {"name": "Hadiah Utama 2 - Logam Mulia Emas 10 Gram", "count": 5},
        {"name": "Hadiah Hiburan - Voucher Belanja Alfamidi Rp 1.000.000", "count": 10},
        {"name": "Doorprize Akbar - Paket Elektronik Rumah Tangga", "count": 20},
    ]

if "selected_category" not in st.session_state:
    st.session_state.selected_category = st.session_state.categories[0]["name"]

if "winner_count" not in st.session_state:
    st.session_state.winner_count = st.session_state.categories[0]["count"]

if "event_title" not in st.session_state:
    st.session_state.event_title = "DOORPRIZE 18 TAHUN ALFAMIDI"

if "name_column" not in st.session_state:
    st.session_state.name_column = "NAMA_KARYAWAN"

if "weight_column" not in st.session_state:
    st.session_state.weight_column = "POIN_UNDIAN"

if "use_weighting" not in st.session_state:
    st.session_state.use_weighting = False

if "display_columns" not in st.session_state:
    st.session_state.display_columns = ["JABATAN", "CABANG"]

if "allow_duplicates" not in st.session_state:
    st.session_state.allow_duplicates = False

if "won_ids" not in st.session_state:
    st.session_state.won_ids = set()

if "draw_history" not in st.session_state:
    st.session_state.draw_history = []

if "recent_winners" not in st.session_state:
    st.session_state.recent_winners = None

# ==============================================================================
# 3. HELPER FUNCTIONS: GENERATOR & SAMPLING
# ==============================================================================
def generate_sample_alfamidi_data(count=1000):
    first_names = [
        'Agus', 'Budi', 'Siti', 'Dewi', 'Eko', 'Rina', 'Bambang', 'Wayan', 'Dian', 'Hendra',
        'Rahmat', 'Nur', 'Yanto', 'Tri', 'Ahmad', 'Fitri', 'Wahyu', 'Putri', 'Hadi', 'Ratna',
        'Rizky', 'Fajar', 'Dedi', 'Indah', 'Bayu', 'Mega', 'Surya', 'Anisa', 'Faisal', 'Tika',
        'Joko', 'Sri', 'Dimas', 'Lestari', 'Arif', 'Maya', 'Ilham', 'Wulan', 'Gilang', 'Nita'
    ]
    last_names = [
        'Santoso', 'Pratama', 'Kusuma', 'Wijaya', 'Saputra', 'Lestari', 'Hidayat', 'Nugroho',
        'Wibowo', 'Firmansyah', 'Suryono', 'Utomo', 'Siregar', 'Harahap', 'Nasution', 'Simanjuntak',
        'Pangestu', 'Gunawan', 'Hartono', 'Purnomo', 'Setiawan', 'Kurniawan', 'Ramadhan'
    ]
    positions = [
        'Store Crew', 'Cashier Staff', 'Store Leader (Kepala Toko)',
        'Assistant Store Leader', 'Area Coordinator', 'Warehouse & Logistics Staff',
        'IT & Support Specialist', 'Human Capital Officer', 'Branch Operation Manager'
    ]
    branches = [
        'Cabang Tangerang (Head Office)', 'Cabang Bekasi', 'Cabang Bogor',
        'Cabang Medan', 'Cabang Makassar', 'Cabang Manado', 'Cabang Samarinda',
        'Cabang Palu', 'Cabang Ambon', 'Cabang Yogyakarta'
    ]
    
    np.random.seed(42)
    rows = []
    for i in range(1, count + 1):
        fn = np.random.choice(first_names)
        ln = np.random.choice(last_names)
        pos = np.random.choice(positions, p=[0.45, 0.25, 0.12, 0.08, 0.04, 0.03, 0.015, 0.01, 0.005])
        br = np.random.choice(branches)
        tenure = np.random.randint(1, 16)
        points = tenure * 10 + np.random.randint(10, 90)
        
        rows.append({
            '_id': f'MIDI-{100000 + i}',
            'NIK': f'MIDI-{100000 + i}',
            'NAMA_KARYAWAN': f'{fn} {ln}',
            'JABATAN': pos,
            'CABANG': br,
            'MASA_KERJA_TAHUN': tenure,
            'POIN_UNDIAN': points
        })
    return pd.DataFrame(rows)

# Default: Load 1.000 karyawan jika belum ada data
if st.session_state.candidates_df is None:
    st.session_state.candidates_df = generate_sample_alfamidi_data(1000)

def draw_winners(df, name_col, weight_col, use_weight, k, display_cols, category_name, allow_dup, won_ids):
    # Filter kandidat jika tidak boleh menang ganda
    eligible_df = df.copy()
    if not allow_dup and len(won_ids) > 0:
        eligible_df = eligible_df[~eligible_df['_id'].isin(won_ids)]
        
    if len(eligible_df) == 0:
        return []
        
    k = min(k, len(eligible_df))
    
    if use_weight and weight_col in eligible_df.columns:
        # A-Res Weighted Sampling Without Replacement (Efraimidis & Spirakis)
        weights = pd.to_numeric(eligible_df[weight_col], errors='coerce').fillna(1).clip(lower=0.1).values
        u = np.random.uniform(0, 1, size=len(eligible_df))
        scores = u ** (1.0 / weights)
        top_indices = np.argsort(scores)[::-1][:k]
        selected = eligible_df.iloc[top_indices]
    else:
        # Uniform Random Sampling (Fisher-Yates)
        selected = eligible_df.sample(n=k, replace=False)
        
    winners = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for rank, (_, row) in enumerate(selected.iterrows(), 1):
        name = str(row.get(name_col, 'Tanpa Nama'))
        extra_parts = [str(row[c]) for c in display_cols if c in row and c != name_col and str(row[c]).strip()]
        display_formatted = " - ".join([name] + extra_parts)
        
        winners.append({
            'rank': rank,
            'id': row.get('_id', name),
            'name': name,
            'category': category_name,
            'display_formatted': display_formatted,
            'timestamp': now_str,
            **{c: row[c] for c in df.columns if c != '_id'}
        })
    return winners

# ==============================================================================
# 4. HEADER APLIKASI
# ==============================================================================
st.markdown(f"""
<div class="main-header">
    <div style="display:flex; align-items:center;">
        <div class="alfamidi-badge">A</div>
        <div>
            <div style="font-size:24px; font-weight:900; letter-spacing:0.5px;">ALFAMIDI LUCKY DRAW</div>
            <div style="font-size:12px; opacity:0.9;">PT MIDI UTAMA INDONESIA TBK • Sistem Undian Doorprize Karyawan</div>
        </div>
    </div>
    <div style="text-align:right;">
        <span style="background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;">
            {len(st.session_state.candidates_df):,} Peserta Terdaftar
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigasi Tab
tab_stage, tab_config, tab_data, tab_history = st.tabs([
    "🎰 Panggung Undian", 
    "⚙️ Pengaturan Parameter", 
    "📥 Sumber Data Peserta", 
    "📜 Riwayat & Laporan"
])

# ==============================================================================
# TAB 1: PANGGUNG UNDIAN
# ==============================================================================
with tab_stage:
    df = st.session_state.candidates_df
    available_count = len(df) if st.session_state.allow_duplicates else max(0, len(df) - len(st.session_state.won_ids))
    
    st.markdown('<div class="slot-chassis">', unsafe_allow_html=True)
    
    # Marquee Title
    st.markdown(f'<div class="slot-marquee">✨ {st.session_state.event_title} ✨</div>', unsafe_allow_html=True)
    
    # Box Kategori Hadiah & Jumlah Pemenang (Rapi dan Tidak keluar boks)
    col_kategori, col_kosong = st.columns([1, 0.01])
    with col_kategori:
        cat_names = [c["name"] for c in st.session_state.categories]
        curr_idx = cat_names.index(st.session_state.selected_category) if st.session_state.selected_category in cat_names else 0
        
        selected_cat = st.selectbox(
            "🎁 Kategori Hadiah:",
            cat_names,
            index=curr_idx,
            key="stage_cat_select"
        )
        if selected_cat != st.session_state.selected_category:
            st.session_state.selected_category = selected_cat
            # Set default winner count for that category
            matched = next((c for c in st.session_state.categories if c["name"] == selected_cat), None)
            if matched:
                st.session_state.winner_count = matched["count"]
                st.rerun()

        # Jumlah Pemenang dipindahkan ke bawah Kategori Hadiah dengan icon Users (3 orang)
        st.markdown("**👥 Jumlah Pemenang:**")
        col_input, col_preset = st.columns([1, 2])
        with col_input:
            winner_count_input = st.number_input(
                "Jumlah Orang",
                min_value=1,
                max_value=max(1, available_count),
                value=int(st.session_state.winner_count),
                label_visibility="collapsed",
                key="stage_winner_count_input"
            )
            st.session_state.winner_count = winner_count_input
            
        with col_preset:
            p_cols = st.columns(5)
            for i, p_val in enumerate([1, 3, 5, 10, 20]):
                if p_cols[i].button(f"{p_val}", key=f"quick_p_{p_val}"):
                    st.session_state.winner_count = p_val
                    st.rerun()

    st.markdown("<hr style='border-color: rgba(245, 158, 11, 0.4); margin: 16px 0;'>", unsafe_allow_html=True)
    
    # Visual Slot Reels Box
    num_reels = min(3, max(1, st.session_state.winner_count))
    reels_cols = st.columns(num_reels)
    
    # Tampilkan pemenang di slot jika <= 3 orang
    recent = st.session_state.recent_winners
    is_slot_winner = recent is not None and len(recent) <= 3
    
    for idx in range(num_reels):
        with reels_cols[idx]:
            if is_slot_winner and idx < len(recent):
                w = recent[idx]
                st.markdown(f"""
                <div class="slot-reel-box" style="background:#fffbeb; border-color:#f59e0b;">
                    <div>
                        <div style="font-size:11px; background:#d71920; color:white; border-radius:10px; padding:2px 8px; display:inline-block; font-weight:800; margin-bottom:4px;">
                            PEMENANG #{idx+1}
                        </div>
                        <div class="reel-winner-title">{w['name']}</div>
                        <div class="reel-winner-subtitle">{w['display_formatted']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="slot-reel-box">
                    <div>
                        <div style="color:#fbbf24; font-size:24px; font-weight:900;">ALFAMIDI</div>
                        <div style="color:#94a3b8; font-size:12px; font-weight:600; margin-top:4px;">SIAP DIUNDI</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # TOMBOL MERAH BESAR (Menggantikan Animasi Tuas)
    col_btn_center = st.columns([1, 2, 1])
    with col_btn_center[1]:
        start_draw_clicked = st.button("🔴 TEKAN UNTUK PUTAR UNDIAN", key="big_red_spin_button")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # LOGIKA PENGUNDIAN SAAT TOMBOL MERAH DITEKAN
    if start_draw_clicked:
        if available_count <= 0:
            st.error("Tidak ada peserta yang tersisa untuk diundi.")
        else:
            # Efek Animasi Slot Berputar
            with st.spinner("🎰 Memutar Mesin Undian Alfamidi..."):
                time.sleep(1.2)
                
            winners = draw_winners(
                df=df,
                name_col=st.session_state.name_column,
                weight_col=st.session_state.weight_column,
                use_weight=st.session_state.use_weighting,
                k=st.session_state.winner_count,
                display_cols=st.session_state.display_columns,
                category_name=st.session_state.selected_category,
                allow_dup=st.session_state.allow_duplicates,
                won_ids=st.session_state.won_ids
            )
            
            st.session_state.recent_winners = winners
            
            # Catat ke riwayat
            st.session_state.draw_history.insert(0, {
                'id': f"draw-{int(time.time())}",
                'category': st.session_state.selected_category,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'count': len(winners),
                'winners': winners
            })
            
            # Kunci ID agar tidak menang 2x
            if not st.session_state.allow_duplicates:
                for w in winners:
                    st.session_state.won_ids.add(w['id'])
                    
            st.rerun()

    # TAMPILAN HASIL PEMENANG BERDASARKAN ATURAN JUMLAH PEMENANG
    if recent is not None:
        count = len(recent)
        
        # JIKA 1 - 3 PEMENANG: Sudah otomatis muncul di kaca slot machine di atas
        if count <= 3:
            st.success(f"🎉 Selamat kepada {count} Pemenang Kategori '{st.session_state.selected_category}'! Hasil tampil langsung pada slot machine.")
            
        # JIKA 4 - 10 PEMENANG: Format Amplop Vintage PT Midi Utama Indonesia Tbk (amplop.png)
        elif 4 <= count <= 10:
            st.markdown(f"""
            <div class="vintage-envelope">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #b91c1c; padding-bottom:12px; margin-bottom:16px;">
                    <div>
                        <div style="font-family:'Playfair Display', serif; font-weight:900; font-size:18px; color:#1e293b;">
                            PT MIDI UTAMA INDONESIA TBK
                        </div>
                        <div style="font-size:11px; color:#64748b; font-family:'Playfair Display', serif;">
                            Alfa Tower Alam Sutera, Jl. Jalur Sutera Bar. No.Kav. 7-9,<br>
                            Kota Tangerang, Banten, Indonesia, 15143
                        </div>
                    </div>
                    <div class="vintage-stamp">
                        <div style="font-size:18px; line-height:1;">A</div>
                        Alfamidi
                    </div>
                </div>
                
                <div style="text-align:center; margin-bottom:16px;">
                    <div style="font-size:12px; font-weight:900; color:#991b1b; letter-spacing:1px; text-transform:uppercase;">
                        TO : THE WINNER OF
                    </div>
                    <div style="font-family:'Playfair Display', serif; font-size:24px; font-weight:900; color:#b91c1c; text-transform:uppercase;">
                        {st.session_state.event_title}
                    </div>
                    <div style="font-size:13px; font-weight:700; color:#475569; margin-top:4px;">
                        Kategori: {st.session_state.selected_category} ({count} Pemenang Sah)
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for w in recent:
                st.markdown(f"""
                <div class="winner-card">
                    <div>
                        <span style="background:#d71920; color:white; font-size:11px; font-weight:800; padding:2px 7px; border-radius:12px; margin-right:8px;">
                            #{w['rank']}
                        </span>
                        <strong style="font-size:15px; color:#0f172a;">{w['name']}</strong>
                        <div style="font-size:12px; color:#475569; margin-top:3px; margin-left:26px;">
                            {w['display_formatted']}
                        </div>
                    </div>
                    <div style="color:#059669; font-weight:700; font-size:12px;">
                        ✓ TERPILIH
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
                <div style="text-align:right; font-size:11px; color:#94a3b8; margin-top:14px; font-style:italic;">
                    Sah dan Terverifikasi oleh Sistem Pengundian PT Midi Utama Indonesia Tbk
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # JIKA > 10 PEMENANG: Format Tabel Komprehensif
        else:
            st.markdown(f"### 📊 Tabel Hasil Pengundian: {st.session_state.selected_category} ({count} Pemenang)")
            table_data = []
            for w in recent:
                row = {
                    "No": w['rank'],
                    "Nama Pemenang": w['name'],
                    "Format Pengumuman": w['display_formatted'],
                }
                for c in st.session_state.display_columns:
                    row[c] = w.get(c, "-")
                table_data.append(row)
                
            result_df = pd.DataFrame(table_data)
            st.dataframe(result_df, use_container_width=True)
            
            # Quick Excel Download
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False, sheet_name="Pemenang Undian")
            st.download_button(
                label="📥 Unduh Hasil Format Excel (.xlsx)",
                data=excel_buffer.getvalue(),
                file_name=f"Alfamidi_{st.session_state.selected_category}_{int(time.time())}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# ==============================================================================
# TAB 2: PENGATURAN PARAMETER UNDIAN
# ==============================================================================
with tab_config:
    st.subheader("⚙️ Parameter & Pengelompokan Hadiah")
    
    col_cfg1, col_cfg2 = st.columns(2)
    
    with col_cfg1:
        st.session_state.event_title = st.text_input(
            "Judul Acara / Header Undian:",
            value=st.session_state.event_title
        )
        
        st.markdown("#### 🎁 Pengaturan Kategori Hadiah (Bulk)")
        st.caption("Atur banyak kategori sekaligus. Format: **Nama Hadiah | Jumlah Pemenang** (1 baris per kategori).")
        
        bulk_cat_text = "\n".join([f"{c['name']} | {c['count']}" for c in st.session_state.categories])
        new_bulk = st.text_area(
            "Daftar Kategori Hadiah:",
            value=bulk_cat_text,
            height=140
        )
        
        if st.button("💾 Terapkan Kategori Hadiah"):
            parsed_cats = []
            for line in new_bulk.strip().split("\n"):
                if "|" in line:
                    parts = line.split("|")
                    name = parts[0].strip()
                    cnt = int(re.sub(r'[^0-9]', '', parts[1])) if re.sub(r'[^0-9]', '', parts[1]) else 1
                    if name:
                        parsed_cats.append({"name": name, "count": cnt})
                elif line.strip():
                    parsed_cats.append({"name": line.strip(), "count": 1})
                    
            if parsed_cats:
                st.session_state.categories = parsed_cats
                st.session_state.selected_category = parsed_cats[0]["name"]
                st.session_state.winner_count = parsed_cats[0]["count"]
                st.success("Kategori hadiah berhasil diperbarui!")
                st.rerun()

        # Pemilihan Kolom Identitas Pemenang
        cols = list(st.session_state.candidates_df.columns)
        clean_cols = [c for c in cols if c != '_id']
        name_idx = clean_cols.index(st.session_state.name_column) if st.session_state.name_column in clean_cols else 0
        
        st.session_state.name_column = st.selectbox(
            "Kolom Utama / Nama yang Diundi:",
            clean_cols,
            index=name_idx
        )

    with col_cfg2:
        st.markdown("#### 📈 Bobot Peluang Kemenangan (Weighted Draw)")
        st.session_state.use_weighting = st.checkbox(
            "Aktifkan Probabilitas Berbobot (Karyawan dengan poin lebih tinggi lebih berpeluang menang)",
            value=st.session_state.use_weighting
        )
        
        if st.session_state.use_weighting:
            numeric_cols = [c for c in clean_cols if pd.to_numeric(st.session_state.candidates_df[c], errors='coerce').notnull().sum() > 0]
            w_idx = numeric_cols.index(st.session_state.weight_column) if st.session_state.weight_column in numeric_cols else 0
            
            st.session_state.weight_column = st.selectbox(
                "Pilih Kolom Penentu Bobot / Poin:",
                numeric_cols if numeric_cols else clean_cols,
                index=w_idx
            )
            st.caption("✓ Menggunakan Algoritma A-Res (Weighted Reservoir Sampling) yang matematis dan adil.")

        st.markdown("#### 👁️ Kolom Ditampilkan Selain Nama")
        st.caption("Pilih informasi staf untuk digabungkan, misal: NAMA - JABATAN - CABANG")
        
        selected_display = []
        for c in clean_cols:
            if c != st.session_state.name_column:
                is_checked = c in st.session_state.display_columns
                if st.checkbox(f"Tampilkan kolom '{c}'", value=is_checked, key=f"disp_{c}"):
                    selected_display.append(c)
        st.session_state.display_columns = selected_display

        st.markdown("#### 🔒 Pencegahan Pemenang Ganda")
        st.session_state.allow_duplicates = not st.checkbox(
            "Cegah Karyawan Menang 2x (Karyawan yang sudah menang otomatis tidak diundi lagi)",
            value=not st.session_state.allow_duplicates
        )

# ==============================================================================
# TAB 3: SUMBER DATA PESERTA
# ==============================================================================
with tab_data:
    st.subheader("📥 Input Data Peserta Undian")
    st.caption("Mendukung lebih dari puluhan ribu entri dari Google Spreadsheet, Excel, CSV, atau ketik manual.")
    
    src_option = st.radio(
        "Pilih Sumber Data:",
        ["Sampel Alfamidi (Siap Pakai)", "Upload File Excel (.xlsx)", "Upload File CSV (.csv)", "Google Spreadsheet", "Ketik Manual"],
        horizontal=True
    )
    
    if src_option == "Sampel Alfamidi (Siap Pakai)":
        st.info("Gunakan data simulasi resmi lengkap dengan NIK, Nama Karyawan, Jabatan, Cabang, dan Poin Kinerja.")
        c1, c2, c3 = st.columns(3)
        if c1.button("Muat 1.000 Karyawan Demo"):
            st.session_state.candidates_df = generate_sample_alfamidi_data(1000)
            st.session_state.won_ids = set()
            st.session_state.recent_winners = None
            st.success("Berhasil memuat 1.000 karyawan!")
            st.rerun()
        if c2.button("Muat 10.000 Karyawan"):
            st.session_state.candidates_df = generate_sample_alfamidi_data(10000)
            st.session_state.won_ids = set()
            st.session_state.recent_winners = None
            st.success("Berhasil memuat 10.000 karyawan!")
            st.rerun()
        if c3.button("Muat 25.000 Karyawan"):
            st.session_state.candidates_df = generate_sample_alfamidi_data(25000)
            st.session_state.won_ids = set()
            st.session_state.recent_winners = None
            st.success("Berhasil memuat 25.000 karyawan!")
            st.rerun()

    elif src_option == "Upload File Excel (.xlsx)":
        uploaded_excel = st.file_uploader("Pilih file Excel:", type=["xlsx", "xls"])
        if uploaded_excel:
            df_up = pd.read_excel(uploaded_excel)
            if '_id' not in df_up.columns:
                df_up['_id'] = [f"row-{i+1}" for i in range(len(df_up))]
            st.session_state.candidates_df = df_up
            st.session_state.won_ids = set()
            st.success(f"Berhasil memuat {len(df_up):,} entri dari Excel!")

    elif src_option == "Upload File CSV (.csv)":
        uploaded_csv = st.file_uploader("Pilih file CSV:", type=["csv"])
        if uploaded_csv:
            df_up = pd.read_csv(uploaded_csv)
            if '_id' not in df_up.columns:
                df_up['_id'] = [f"row-{i+1}" for i in range(len(df_up))]
            st.session_state.candidates_df = df_up
            st.session_state.won_ids = set()
            st.success(f"Berhasil memuat {len(df_up):,} entri dari CSV!")

    elif src_option == "Google Spreadsheet":
        gsheet_url = st.text_input("Masukkan tautan Google Spreadsheet (Pastikan setel Publik):")
        if st.button("Tarik Data Spreadsheet"):
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', gsheet_url)
            if match:
                sheet_id = match.group(1)
                export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                try:
                    df_up = pd.read_csv(export_url)
                    if '_id' not in df_up.columns:
                        df_up['_id'] = [f"row-{i+1}" for i in range(len(df_up))]
                    st.session_state.candidates_df = df_up
                    st.session_state.won_ids = set()
                    st.success(f"Berhasil memuat {len(df_up):,} data dari Google Spreadsheet!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal mengambil spreadsheet: {e}. Pastikan hak akses 'Anyone with link can view'.")
            else:
                st.error("Tautan Google Spreadsheet tidak valid.")

    elif src_option == "Ketik Manual":
        st.caption("Gunakan koma (,) untuk memisahkan kolom dan ENTER untuk baris baru:")
        manual_txt = st.text_area(
            "Ketik Data:",
            value="NIK,NAMA_KARYAWAN,JABATAN,CABANG,POIN_UNDIAN\nMIDI-001,Budi Santoso,Store Leader,Makassar,150\nMIDI-002,Siti Aminah,Cashier Staff,Bekasi,90\nMIDI-003,Eko Pratama,Store Crew,Tangerang,120",
            height=150
        )
        if st.button("Terapkan Data Manual"):
            try:
                df_up = pd.read_csv(io.StringIO(manual_txt.strip()))
                if '_id' not in df_up.columns:
                    df_up['_id'] = [f"row-{i+1}" for i in range(len(df_up))]
                st.session_state.candidates_df = df_up
                st.session_state.won_ids = set()
                st.success(f"Berhasil memuat {len(df_up)} data manual!")
                st.rerun()
            except Exception as e:
                st.error(f"Format teks manual tidak valid: {e}")

    # Pratinjau 5 Baris Data
    if st.session_state.candidates_df is not None:
        st.markdown(f"**Pratinjau Data ({len(st.session_state.candidates_df):,} total entri):**")
        disp_preview = st.session_state.candidates_df[[c for c in st.session_state.candidates_df.columns if c != '_id']].head(5)
        st.dataframe(disp_preview, use_container_width=True)

# ==============================================================================
# TAB 4: RIWAYAT & LAPORAN
# ==============================================================================
with tab_history:
    st.subheader("📜 Riwayat Putaran Undian")
    
    if len(st.session_state.draw_history) == 0:
        st.info("Belum ada riwayat undian. Jalankan putaran undian di tab 'Panggung Undian'.")
    else:
        col_act1, col_act2 = st.columns([1, 4])
        with col_act1:
            if st.button("🗑️ Reset Semua Riwayat"):
                st.session_state.draw_history = []
                st.session_state.won_ids = set()
                st.session_state.recent_winners = None
                st.rerun()
                
        # Gabungkan semua pemenang untuk ekspor global
        all_winners = []
        for h in st.session_state.draw_history:
            for w in h['winners']:
                all_winners.append(w)
                
        all_df = pd.DataFrame(all_winners)
        clean_export_df = all_df[[c for c in all_df.columns if c not in ['_id', 'id']]]
        
        excel_buffer_all = io.BytesIO()
        with pd.ExcelWriter(excel_buffer_all, engine='openpyxl') as writer:
            clean_export_df.to_excel(writer, index=False, sheet_name="Semua Pemenang")
            
        st.download_button(
            label="📥 Ekspor Seluruh Putaran ke Excel (.xlsx)",
            data=excel_buffer_all.getvalue(),
            file_name=f"Alfamidi_Semua_Pemenang_{int(time.time())}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        for idx, entry in enumerate(st.session_state.draw_history):
            with st.expander(f"Putaran #{len(st.session_state.draw_history) - idx}: {entry['category']} ({entry['count']} Pemenang) - {entry['timestamp']}"):
                entry_df = pd.DataFrame(entry['winners'])
                clean_entry = entry_df[['rank', 'name', 'display_formatted'] + [c for c in st.session_state.display_columns if c in entry_df.columns]]
                st.dataframe(clean_entry, use_container_width=True)
