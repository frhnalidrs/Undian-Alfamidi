"""
Alfamidi Lucky Draw - Sistem Undian Karyawan PT Midi Utama Indonesia Tbk
Aplikasi Undian Doorprize Berkapasitas Puluhan Ribu Peserta
Tampilan Corporate Red & White

Cara Menjalankan:
1. pip install -r requirements.txt
2. streamlit run streamlit.py
"""

import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import json

# Ambil direktori absolut dari lokasi streamlit.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64_image(relative_path):
    # Gabungkan path absolut dengan relative path
    full_path = os.path.join(BASE_DIR, relative_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    # Tampilkan peringatan di Streamlit Cloud jika file gagal dibaca
    st.warning(f"⚠️ File gambar tidak ditemukan di path: {full_path}")
    return ""

logo_b64 = get_base64_image("assets/images/logo.png")
logo_panjang_b64 = get_base64_image("assets/images/Alfamidi_2015.svg")
bg_b64 = get_base64_image("assets/images/bg.png")

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Alfamidi Lucky Draw - Sistem Undian Karyawan",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Hilangkan padding default Streamlit
st.markdown("""
<style>
    /* Sembunyikan Header bawaan Streamlit secara total */
    [data-testid="stHeader"], header, #MainMenu, footer {
        display: none !important;
    }
    
    /* Hilangkan margin & padding container utama Streamlit */
    .stApp, [data-testid="stAppViewContainer"], .main {
        margin: 0 !important;
        padding: 0 !important;
        top: 0 !important;
        background-color: #f8fafc !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hilangkan gap vertical block bawaan Streamlit */
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding: 0 !important;
    }
    
    iframe {
        width: 100% !important;
        border: none !important;
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
        vertical-align: top !important;
    }
</style>
""", unsafe_allow_html=True)


# 3. Full Standalone HTML, CSS & JavaScript - Corporate Light Theme (Rakornas 2026 Style)
ALFAMIDI_HTML = """<!doctype html>
<html lang="id">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Alfamidi Lucky Draw</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.4/dist/confetti.browser.min.js"></script>

    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #1e293b;
            overflow-x: hidden;

            /* Gradient Overlay (Lapisan Transparan) + Gambar Background */
            background-image: 
            linear-gradient(rgba(248, 250, 252, 0.35), rgba(248, 250, 252, 0.35)), 
            url("data:image/png;base64,%%BG_B64%%");
            background-position: center center;
            background-repeat: no-repeat;
            background-size: cover;
            background-attachment: fixed;
        }

        .airmail-border {
            background: repeating-linear-gradient(135deg,
                    #d71920 0,
                    #d71920 18px,
                    transparent 18px,
                    transparent 24px,
                    #1e40af 24px,
                    #1e40af 42px,
                    transparent 42px,
                    transparent 48px);
        }

        .stamp-border {
            clip-path: polygon(0% 4%, 4% 0%, 8% 4%, 12% 0%, 16% 4%, 20% 0%, 24% 4%, 28% 0%, 32% 4%, 36% 0%,
                    40% 4%, 44% 0%, 48% 4%, 52% 0%, 56% 4%, 60% 0%, 64% 4%, 68% 0%, 72% 4%, 76% 0%,
                    80% 4%, 84% 0%, 88% 4%, 92% 0%, 96% 4%, 100% 0%, 100% 100%, 0% 100%);
        }
    /* ANIMASI RIAK (RIPPLE EFFECT) TOMBOL BULAT UNDI */
        @keyframes ripple-ring {
            0% {
                transform: scale(0.88);
                opacity: 0.7;
            }
            50% {
                opacity: 0.35;
            }
            100% {
                transform: scale(1.45);
                opacity: 0;
            }
        }

        .animate-ripple-1 {
            animation: ripple-ring 2.2s cubic-bezier(0.1, 0.4, 0.8, 1) infinite;
        }

        .animate-ripple-2 {
            animation: ripple-ring 2.2s cubic-bezier(0.1, 0.4, 0.8, 1) infinite;
            animation-delay: 1.1s;
        }
    </style>
</head>

<body class="min-h-screen antialiased flex flex-col pb-10">

    <!-- TOP HEADER (Clean White with Red Accent) -->
    <header class="sticky top-0 z-40 bg-white border-b-2 border-red-600 shadow-xs px-4 sm:px-8 py-3">
        <div class="max-w-7xl mx-auto grid grid-cols-[1fr_auto_1fr] items-center gap-4">
            
            <!-- Kolom 1 (Kiri): Logo Alfamidi -->
            <div class="flex items-center justify-start min-w-0">
                <div class="flex-shrink-0">
                    <img src="data:image/svg+xml;base64,%%LOGO_PANJANG%%" alt="Alfamidi Logo" class="h-9 sm:h-8 w-auto object-contain"/>
                </div>
            </div>

            <!-- Kolom 2 (Tengah): Navigation Tabs (Persis di Tengah & 1 Baris) -->
            <div class="flex justify-center">
                <nav class="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200 whitespace-nowrap" role="tablist">
                    <button id="tab-btn-stage" class="nav-tab active flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer bg-red-600 text-white shadow-sm whitespace-nowrap">
                        <span>✨</span>
                        <span class="hidden sm:inline">Panggung Undian</span>
                        <span class="sm:hidden">Undian</span>
                    </button>
                    <button id="tab-btn-config" class="nav-tab flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer text-slate-600 hover:bg-slate-200/60 hover:text-slate-900 whitespace-nowrap">
                        <span>⚙️</span>
                        <span class="hidden sm:inline">Pengaturan Undian</span>
                        <span class="sm:hidden">Setting</span>
                    </button>
                    <button id="tab-btn-data" class="nav-tab flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer text-slate-600 hover:bg-slate-200/60 hover:text-slate-900 whitespace-nowrap">
                        <span>📁</span>
                        <span class="hidden sm:inline">Data Peserta</span>
                        <span class="sm:hidden">Data</span>
                    </button>
                </nav>
            </div>

            <!-- Kolom 3 (Kanan): Right Header Tools -->
            <div class="flex items-center justify-end gap-2 whitespace-nowrap">
                <button id="btn-view-last-modal" class="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-700 border border-amber-300 text-xs font-bold transition-all cursor-pointer shadow-2xs" title="Buka kembali modal hasil undian terakhir">
                    <span>👁️</span>
                    <span>Modal Terakhir</span>
                </button>

                <button id="btn-open-history" class="relative p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition-colors cursor-pointer flex items-center gap-1 text-xs font-semibold" title="Lihat Riwayat Putaran Undian">
                    <span class="text-red-600">🕒</span>
                    <span class="hidden md:inline">Riwayat</span>
                    <span id="history-badge-count" class="w-5 h-5 rounded-full bg-red-600 text-white text-[10px] font-black hidden items-center justify-center">0</span>
                </button>

                <button id="btn-toggle-sound" class="flex items-center gap-1 text-xs font-bold text-slate-600 hover:text-slate-900 bg-slate-100 px-2.5 py-1.5 rounded-xl border border-slate-300 transition-colors cursor-pointer ml-1" title="Nyalakan/Matikan Suara">
                    <span>🔊</span>
                    <span id="sound-status-text" class="hidden sm:inline">Suara ON</span>
                </button>
            </div>

        </div>
    </header>

    <!-- MAIN APP CONTAINER -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 pt-6">

        <!-- HEADER TITLE BANNER (Identik Gambar 2) -->
        <div class="text-center mb-6 space-y-1">
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                Sistem Undian Karyawan
            </h1>
            <p id="marquee-event-title" class="text-sm sm:text-base font-bold text-slate-700">
                Alfamidi Lucky Draw 2026
            </p>
            <div class="w-12 h-1 bg-red-600 mx-auto rounded-full my-2"></div>
            <br>
            <p class="text-xs sm:text-sm text-slate-500 max-w-xl mx-auto">
                Mulai undiannya, bawa pulang hadiahnya!
            </p>
        </div>

        <!-- QUICK INFO STRIP -->
        <div class="mb-6 flex flex-wrap items-center justify-between gap-3 p-3.5 bg-red-50/100 rounded-2xl border border-red-400 text-xs shadow-2xs">
            <div class="flex items-center gap-3 flex-wrap">
                <div class="flex items-center gap-1.5 text-slate-700 font-medium">
                    <span class="text-red-600 text-sm">🎁</span>
                    <span>Hadiah Aktif: <strong id="info-active-group" class="text-red-700 font-bold">Grand Prize - Sepeda Motor Honda Beat</strong></span>
                </div>
                <span class="text-slate-300 hidden sm:inline">•</span>
                <div class="text-slate-700">
                    Jumlah: <strong id="info-winner-count" class="text-red-700 font-bold font-mono">1 Pemenang</strong>
                </div>
                <span class="text-slate-300 hidden sm:inline">•</span>
                <div class="text-slate-700">
                    Format: <span id="info-format-preview" class="font-mono text-slate-600 font-semibold">[-]</span>
                </div>
            </div>

            <div class="flex items-center gap-2">
                <span class="text-slate-500">Sisa Peserta Dapat Diundi:</span>
                <span id="info-candidate-stats" class="px-2.5 py-0.5 rounded-full bg-red-600 text-white font-bold font-mono text-xs shadow-2xs">
                    1.000 / 1.000
                </span>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- SECTION 1: PANGGUNG UNDIAN (SLOT MACHINE ARENA) -->
        <!-- ============================================================== -->
        <section id="section-stage" class="space-y-6">

            <!-- KATEGORI HADIAH & JUMLAH PEMENANG CONTROL BAR -->
            <div class="max-w-4xl mx-auto bg-white p-3.5 sm:p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-3 sm:gap-4">
                <div class="flex items-center gap-2 flex-1 min-w-[240px]">
                    <label for="stage-category-select" class="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5 flex-shrink-0">
                        <span class="text-red-600">🎁</span> Kategori Hadiah:
                    </label>
                    <select id="stage-category-select" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs sm:text-sm font-bold text-slate-900 focus:outline-none focus:border-red-500 cursor-pointer shadow-2xs truncate">
                    </select>
                </div>

                <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1 flex-shrink-0">
                        <span>👥</span> Jumlah Pemenang:
                    </span>
                    <div class="flex items-center gap-1">
                        <button type="button" class="btn-quick-count px-2.5 py-1 text-xs font-bold rounded-lg border transition-colors cursor-pointer" data-count="1">1</button>
                        <button type="button" class="btn-quick-count px-2.5 py-1 text-xs font-bold rounded-lg border transition-colors cursor-pointer" data-count="3">3</button>
                        <button type="button" class="btn-quick-count px-2.5 py-1 text-xs font-bold rounded-lg border transition-colors cursor-pointer" data-count="5">5</button>
                        <button type="button" class="btn-quick-count px-2.5 py-1 text-xs font-bold rounded-lg border transition-colors cursor-pointer" data-count="10">10</button>
                        <button type="button" class="btn-quick-count px-2.5 py-1 text-xs font-bold rounded-lg border transition-colors cursor-pointer" data-count="20">20</button>
                    </div>
                    <div class="flex items-center gap-1 bg-slate-100 px-2 py-1 rounded-lg border border-slate-300">
                        <input id="stage-winner-count-input" type="number" min="1" value="1" class="w-12 bg-transparent text-xs sm:text-sm text-red-600 font-mono font-extrabold text-center focus:outline-none" />
                        <span class="text-[11px] text-slate-500 font-semibold">Orang</span>
                    </div>
                </div>
            </div>

            <!-- MAIN SLOT MACHINE CHASSIS (Panjang & Presisi Gambar 2) -->
            <div class="relative w-full max-w-5xl mx-auto">

                <!-- 3D Red Frame Container -->
                <div class="relative w-full bg-gradient-to-b from-red-600 via-red-600 to-red-700 p-3 sm:p-5 rounded-[32px] shadow-[0_20px_50px_rgba(220,38,38,0.25)] border-4 border-red-500">

                    <!-- Inner White Reel Window -->
                    <div class="relative w-full bg-white rounded-2xl p-4 sm:p-6 shadow-inner border border-slate-200 overflow-hidden min-h-[220px] flex items-center justify-center">

                        <!-- Side Arrow Indicators (Identik Gambar 2) -->
                        <div class="absolute inset-y-0 left-2 my-auto h-12 w-6 flex items-center justify-center z-10 pointer-events-none">
                            <svg class="w-6 h-6 text-red-600 drop-shadow-sm fill-red-600" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        </div>
                        <div class="absolute inset-y-0 right-2 my-auto h-12 w-6 flex items-center justify-center z-10 pointer-events-none">
                            <svg class="w-6 h-6 text-red-600 drop-shadow-sm fill-red-600 transform rotate-180" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                        </div>

                        <!-- Reels Grid Container -->
                        <div id="slot-reels-grid" class="w-full grid gap-4 sm:gap-6 relative z-0 grid-cols-1 sm:grid-cols-3">
                        </div>
                    </div>
                </div>

                <!-- <!-- TOMBOL UNDI BULAT DENGAN EFEK RIAK (DESAIN 3D ARCADE) -->
                <div class="flex flex-col items-center justify-center my-8 relative">
                    <!-- Ripple Animation Rings -->
                    <div class="relative flex items-center justify-center">
                        <div class="absolute w-44 h-44 sm:w-56 sm:h-56 rounded-full bg-red-600/30 animate-ripple-1 pointer-events-none"></div>
                        <div class="absolute w-44 h-44 sm:w-56 sm:h-56 rounded-full bg-amber-500/25 animate-ripple-2 pointer-events-none"></div>

                        <!-- Outer Metallic Gold Rim Container -->
                        <div class="relative p-2.5 sm:p-3 rounded-full bg-gradient-to-b from-amber-200 via-amber-400 to-yellow-600 shadow-[0_15px_35px_rgba(217,119,6,0.4)] border border-amber-300">
                            <!-- Inner Dark Ring Frame -->
                            <div class="p-1.5 sm:p-2 rounded-full bg-slate-900 shadow-inner">
                                <!-- Red Dome 3D Glossy Button -->
                                <button id="btn-main-spin" type="button" class="relative w-32 h-32 sm:w-40 sm:h-40 rounded-full bg-gradient-to-b from-red-500 via-red-600 to-red-800 shadow-[inset_0_-8px_14px_rgba(0,0,0,0.5),0_12px_24px_rgba(220,38,38,0.5)] cursor-pointer flex flex-col items-center justify-center border-2 border-red-400/60 hover:scale-105 active:scale-95 transition-all duration-200 group overflow-hidden">
                                    <!-- Shiny Glass Reflection Arc -->
                                    <div class="absolute top-1.5 w-3/4 h-2/5 bg-gradient-to-b from-white/60 to-transparent rounded-t-full pointer-events-none"></div>
                                    
                                    <!-- Play Icon -->
                                    <svg class="w-7 h-7 sm:w-8 sm:h-8 fill-white drop-shadow-md mb-0.5 group-hover:scale-110 transition-transform" viewBox="0 0 24 24">
                                        <polygon points="6 4 20 12 6 20 6 4"></polygon>
                                    </svg>
                                    
                                    <!-- Inner Button Labels -->
                                    <span class="font-black text-white text-xs sm:text-sm tracking-wider uppercase drop-shadow-md leading-none">MULAI</span>
                                    <span id="btn-main-spin-text" class="font-extrabold text-amber-200 text-[10px] sm:text-xs tracking-widest uppercase drop-shadow-md leading-tight mt-0.5">(START)</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Outer Text Label -->
                    <span class="mt-3.5 text-xs sm:text-sm font-extrabold text-amber-700 tracking-widest uppercase drop-shadow-2xs">TEKAN UNTUK MEMULAI</span>

                    <button id="btn-arcade-red-button" type="button" class="hidden"></button>
                    <span id="btn-arcade-red-text" class="hidden"></span>

                    <!-- Undi Ulang Button -->
                    <button id="btn-reset-draw" type="button" class="hidden mt-3 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-full border border-slate-300 flex items-center gap-1.5 transition-colors cursor-pointer shadow-2xs">
                        <span>🔄</span>
                        <span>Undi Ulang</span>
                    </button>
                </div>

                <!-- KARTU PEMENANG BAGIAN BAWAH (Identik Gambar 2) -->
                <div class="w-full max-w-5xl mx-auto bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs space-y-3">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                        <div class="flex items-center gap-2 text-slate-900 font-extrabold text-sm sm:text-base">
                            <span class="text-red-600 text-lg">🏆</span>
                            <span>Latest Winner</span>
                        </div>
                        <div class="text-xs text-slate-500 font-medium">
                            Total Kandidat: <strong id="bottom-total-candidates" class="text-slate-900 font-mono font-bold">1.000</strong> peserta
                        </div>
                    </div>

                    <!-- Dynamic Winner Slots Below -->
                    <div id="bottom-winner-slots" class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
                    </div>

                    <!-- Action Last Modal Trigger -->
                    <div class="flex justify-end pt-1">
                        <button id="btn-bottom-last-modal" class="hidden text-xs text-red-600 font-bold hover:underline flex items-center gap-1">
                            <span>👁️</span>
                            <span id="btn-bottom-last-modal-text">Lihat Modal Terakhir</span>
                        </button>
                    </div>
                </div>

            </div>
        </section>

        <!-- ============================================================== -->
        <!-- SECTION 2: PENGATURAN PARAMETER UNDIAN (CONFIG) -->
        <!-- ============================================================== -->
        <section id="section-config" class="hidden max-w-4xl mx-auto space-y-5">
            <div class="bg-white border border-slate-200 rounded-2xl p-4 sm:p-6 shadow-xs space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                    <h2 class="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span>⚙️</span> Pengaturan Parameter Undian
                    </h2>
                    <span class="text-xs text-slate-500">
                        Tersedia: <strong id="config-available-count" class="text-slate-900 font-bold">1.000</strong> peserta
                    </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6">
                    <div class="space-y-4">
                        <div>
                            <label for="input-event-title" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                                Judul Acara / Header Undian
                            </label>
                            <input id="input-event-title" type="text" value="Alfamidi Lucky Draw 2026" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-red-500" />
                        </div>

                        <!-- Bulk Kategori Hadiah -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                            <div class="flex items-center justify-between">
                                <label for="textarea-bulk-categories" class="text-xs font-bold text-red-600 uppercase tracking-wider">
                                    Daftar Kategori / Grup Hadiah (Bulk)
                                </label>
                                <span id="config-categories-count" class="text-[10px] text-slate-500 font-mono">4 Kategori Aktif</span>
                            </div>
                            <p class="text-[11px] text-slate-500">
                                Format: <span class="text-red-600 font-semibold">Nama Hadiah | Jumlah Pemenang</span> (1 baris per kategori).
                            </p>
                            <textarea id="textarea-bulk-categories" rows="5" class="w-full bg-white border border-slate-300 rounded-xl p-3 font-mono text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-red-500"></textarea>
                            <div class="flex items-center justify-between pt-1">
                                <span class="text-[10px] text-slate-400 italic">* Pilih kategori di panggung undian</span>
                                <button id="btn-apply-bulk-categories" type="button" class="px-3.5 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-lg transition-colors cursor-pointer shadow-2xs">
                                    Terapkan Kategori
                                </button>
                            </div>
                            <div id="config-categories-chips" class="pt-2 border-t border-slate-200 space-y-1.5 max-h-36 overflow-y-auto pr-1"></div>
                        </div>

                        <div>
                            <label for="select-name-column" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                                Kolom Utama / Nama yang Diundi
                            </label>
                            <select id="select-name-column" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-red-500 cursor-pointer"></select>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <div class="flex items-center justify-between mb-1.5">
                                <label for="input-default-winner-count" class="text-xs font-bold text-slate-700 uppercase tracking-wider">
                                    Jumlah Pemenang Default
                                </label>
                                <span id="label-default-winner-count" class="text-xs font-mono font-bold text-red-600">1 Orang</span>
                            </div>
                            <div class="flex items-center gap-2 mb-2.5">
                                <input id="input-default-winner-count" type="number" min="1" value="1" class="w-24 bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 font-mono text-center focus:outline-none focus:border-red-500" />
                                <div class="flex flex-wrap gap-1">
                                    <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" data-count="1">1</button>
                                    <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" data-count="3">3</button>
                                    <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" data-count="5">5</button>
                                    <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" data-count="10">10</button>
                                    <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-100 text-slate-700 hover:bg-slate-200" data-count="20">20</button>
                                </div>
                            </div>
                            <div id="animation-notice-badge" class="p-2.5 rounded-xl border flex items-center gap-2 text-xs font-bold text-red-700 bg-red-50 border-red-200">
                                <span id="animation-notice-text">🎰 Slot Machine</span>
                            </div>
                        </div>

                        <!-- Weighted probability -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Bobot Kemenangan</span>
                                <label class="relative inline-flex items-center cursor-pointer">
                                    <input id="checkbox-use-weighting" type="checkbox" class="sr-only peer" />
                                    <div class="w-9 h-5 bg-slate-300 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-red-600"></div>
                                </label>
                            </div>
                            <div id="weight-column-container" class="hidden space-y-2 pt-2 border-t border-slate-200">
                                <select id="select-weight-column" class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none cursor-pointer"></select>
                            </div>
                        </div>
                        
                        <!-- Filter Kriteria Peserta -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold text-slate-700 uppercase tracking-wider">Filter Kriteria Peserta</span>
                                <label class="relative inline-flex items-center cursor-pointer">
                                    <input id="checkbox-use-filtering" type="checkbox" class="sr-only peer" />
                                    <div class="w-9 h-5 bg-slate-300 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-red-600"></div>
                                </label>
                            </div>
                            
                            <div id="filter-rules-container" class="hidden space-y-3 pt-2 border-t border-slate-200">
                                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
                                    <select id="select-filter-column" class="bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 focus:outline-none cursor-pointer"></select>
                                    <select id="select-filter-operator" class="bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 focus:outline-none cursor-pointer">
                                        <option value="contains">Berisi Kata (Contains)</option>
                                        <option value="=">Sama Dengan (=)</option>
                                        <option value="!=">Tidak Sama (!=)</option>
                                        <option value=">">Lebih Dari (&gt;)</option>
                                        <option value=">=">Lebih Dari / Sama (&gt;=)</option>
                                        <option value="<">Kurang Dari (&lt;)</option>
                                        <option value="<=">Kurang Dari / Sama (&lt;=)</option>
                                    </select>
                                    <input id="input-filter-value" type="text" placeholder="Nilai (cth: OFFICE / 30)" class="bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 focus:outline-none" />
                                </div>
                                <div class="flex justify-end">
                                    <button id="btn-add-filter-rule" type="button" class="px-3.5 py-1.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-lg transition-colors cursor-pointer shadow-2xs">
                                        + Tambah Filter
                                    </button>
                                </div>
                                <div id="filter-chips-list" class="space-y-1.5 pt-1 max-h-36 overflow-y-auto pr-1"></div>
                            </div>
                        </div>

                        <!-- Kolom Tampilan -->
                        <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                            <span class="text-xs font-bold text-slate-700 uppercase tracking-wider block">Kolom yang akan ditampilkan</span>
                            <div id="config-display-checkboxes-grid" class="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto pr-1"></div>
                            <div id="config-format-sample-box" class="px-3 py-1.5 rounded-lg bg-white border border-slate-300 font-mono text-xs text-red-600 font-bold truncate"></div>
                        </div>

                        <!-- Duplicate lock -->
                        <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200">
                            <span class="text-xs font-bold text-slate-700">Kunci Pemenang (Cegah Menang 2x)</span>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input id="checkbox-prevent-duplicate" type="checkbox" checked class="sr-only peer" />
                                <div class="w-9 h-5 bg-slate-300 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-emerald-600"></div>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="flex justify-end pt-3 border-t border-slate-100">
                    <button id="btn-save-to-stage" type="button" class="px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl shadow-xs transition-transform hover:scale-105 active:scale-95 cursor-pointer">
                        Simpan & Menuju Panggung Undian
                    </button>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- SECTION 3: SUMBER DATA PESERTA -->
        <!-- ============================================================== -->
        <section id="section-data" class="hidden max-w-4xl mx-auto space-y-5">
            <div class="bg-white border border-slate-200 rounded-2xl p-4 sm:p-6 shadow-xs">
                <div class="flex flex-wrap items-center justify-between gap-3 mb-5 border-b border-slate-100 pb-4">
                    <h2 class="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span>📁</span> Sumber Data Peserta Undian
                    </h2>
                    <div class="px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold">
                        <span id="data-active-counter-text">1.000 Peserta Aktif</span>
                    </div>
                </div>

                <div class="flex flex-wrap gap-1.5 p-1 bg-slate-100 rounded-xl mb-5 border border-slate-200">
                    <button class="subtab-btn active px-3.5 py-2 rounded-lg text-xs font-bold bg-red-600 text-white" data-target="panel-sample">Sampel Alfamidi</button>
                    <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-bold text-slate-600" data-target="panel-excel">Upload Excel (.xlsx)</button>
                    <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-bold text-slate-600" data-target="panel-csv">Upload CSV</button>
                    <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-bold text-slate-600" data-target="panel-gsheet">Google Spreadsheet</button>
                    <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-bold text-slate-600" data-target="panel-manual">Ketik Manual</button>
                </div>

                <div class="space-y-4">
                    <div id="panel-sample" class="data-subpanel bg-slate-50 p-4 sm:p-5 rounded-xl border border-slate-200">
                        <p class="text-xs text-slate-600 mb-4">Gunakan data simulasi resmi lengkap dengan NIK, Nama Karyawan, Jabatan, Cabang se-Indonesia, dan Poin Kinerja.</p>
                        <div class="flex flex-wrap gap-3">
                            <button type="button" id="btn-load-sample-1k" class="px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl cursor-pointer">Muat 1.000 Karyawan</button>
                            <button type="button" id="btn-load-sample-10k" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-900 text-amber-300 text-xs font-bold rounded-xl cursor-pointer">Muat 10.000 Karyawan</button>
                            <button type="button" id="btn-load-sample-25k" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-900 text-emerald-400 text-xs font-bold rounded-xl cursor-pointer">Muat 25.000 Karyawan</button>
                        </div>
                    </div>

                    <div id="panel-excel" class="data-subpanel hidden border-2 border-dashed border-slate-300 rounded-xl p-6 text-center bg-slate-50">
                        <p class="text-sm font-bold text-slate-800 mb-2">Pilih File Excel (.xlsx, .xls)</p>
                        <label class="inline-block px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl cursor-pointer">
                            Pilih Berkas Excel
                            <input id="input-file-excel" type="file" accept=".xlsx, .xls" class="hidden" />
                        </label>
                    </div>

                    <div id="panel-csv" class="data-subpanel hidden border-2 border-dashed border-slate-300 rounded-xl p-6 text-center bg-slate-50">
                        <p class="text-sm font-bold text-slate-800 mb-2">Pilih File CSV (.csv)</p>
                        <label class="inline-block px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl cursor-pointer">
                            Pilih Berkas CSV
                            <input id="input-file-csv" type="file" accept=".csv, text/csv" class="hidden" />
                        </label>
                    </div>

                    <div id="panel-gsheet" class="data-subpanel hidden bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                        <div class="flex gap-2">
                            <input id="input-gsheet-url" type="url" placeholder="https://docs.google.com/spreadsheets/d/.../edit" class="flex-1 bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900" />
                            <button id="btn-fetch-gsheet" type="button" class="px-4 py-2 bg-red-600 text-white text-xs font-bold rounded-xl">Tarik Data</button>
                        </div>
                    </div>

                    <div id="panel-manual" class="data-subpanel hidden bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                        <textarea id="textarea-manual-data" rows="6" class="w-full bg-white border border-slate-300 rounded-xl p-3 font-mono text-xs text-slate-800">NIK,NAMA_KARYAWAN,JABATAN,CABANG,POIN_UNDIAN
MIDI-202401,Budi Santoso,Store Leader,Makassar,150
MIDI-202402,Siti Nurhaliza,Cashier Staff,Bekasi,90
MIDI-202403,Ahmad Pratama,Store Crew,Tangerang,120</textarea>
                        <div class="flex justify-end">
                            <button id="btn-apply-manual-data" type="button" class="px-5 py-2 bg-red-600 text-white text-xs font-bold rounded-xl">Terapkan Data</button>
                        </div>
                    </div>

                    <div id="data-import-alert" class="hidden p-3 rounded-xl text-xs font-semibold"></div>

                    <div class="mt-4 pt-4 border-t border-slate-200">
                        <span class="text-xs font-bold text-slate-700 block mb-2">Pratinjau Data (5 Baris Pertama):</span>
                        <div class="overflow-x-auto rounded-lg border border-slate-200 bg-white">
                            <table class="w-full text-left text-xs">
                                <thead id="data-preview-thead" class="bg-slate-100 text-slate-700 font-bold"></thead>
                                <tbody id="data-preview-tbody" class="divide-y divide-slate-100"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>
    
    <!-- FOOTER -->
    <footer class="w-full text-center text-xs font-medium text-slate-600 py-6">
        Copyright &copy; Alfamidi 2026, Designed by Google AI Studio, Coded by Farhan Abyan Putra Karim
    </footer>

    <!-- ============================================================== -->
    <!-- MODAL 1: SURAT AMPLOP VINTAGE (4-10 PEMENANG) -->
    <!-- ============================================================== -->
    <div id="modal-envelope" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-slate-900/60 backdrop-blur-md">
        <div class="relative w-full max-w-3xl flex flex-col items-center my-auto">
            <button id="btn-close-envelope-modal" class="absolute -top-12 right-0 p-2 text-white bg-slate-900/80 rounded-full border border-white/20">✕</button>

            <div class="relative w-full flex flex-col items-center">
                <!-- Letter -->
                <div id="envelope-letter" class="w-full max-w-2xl bg-[#fffef9] text-slate-800 rounded-xl shadow-2xl border border-amber-200/80 p-5 sm:p-8 z-20">
                    <div class="flex items-center justify-between border-b-2 border-red-600 pb-4 mb-4">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white font-black text-xl shadow-xs">
                                <img src="data:image/png;base64,%%LOGO_B64%%" alt="Alfamidi Logo" class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl border border-amber-400/40 shadow-xs object-cover" />
                            </div>
                            <div>
                                <h3 class="font-extrabold text-sm sm:text-base text-slate-900 uppercase">PT MIDI UTAMA INDONESIA TBK</h3>
                                <p class="text-[11px] text-slate-500">Surat Keputusan Pemenang Undian Resmi</p>
                            </div>
                        </div>
                        <div class="text-right">
                            <span id="letter-category-name" class="text-xs font-semibold uppercase text-red-600 block"></span>
                            <span id="letter-current-date" class="text-[10px] text-slate-400"></span>
                        </div>
                    </div>

                    <div class="text-center mb-5">
                        <h2 id="letter-event-title" class="text-xl sm:text-2xl font-black text-red-700 uppercase font-serif">SISTEM UNDIAN KARYAWAN</h2>
                        <p id="letter-subtitle" class="text-xs text-slate-600 mt-1"></p>
                    </div>

                    <div id="envelope-winners-list" class="space-y-2.5 max-h-[42vh] overflow-y-auto pr-1"></div>

                    <div class="mt-5 pt-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
                        <span class="italic">Sah & Terverifikasi oleh Sistem Pengundian Alfamidi</span>
                        <span id="letter-total-winners-count" class="font-mono text-[11px] text-slate-400"></span>
                    </div>

                    <div class="mt-5 flex items-center justify-end gap-2.5">
                        <button id="btn-envelope-export-excel" class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-2xs">Unduh Excel</button>
                        <button id="btn-envelope-export-pdf" class="px-3.5 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg shadow-2xs">Cetak PDF</button>
                        <button id="btn-envelope-finish" class="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold rounded-lg">Selesai</button>
                    </div>
                </div>

                <!-- Envelope Chassis -->
                <div id="envelope-chassis" class="w-full max-w-xl aspect-[1.65/1] rounded-lg shadow-2xl relative overflow-hidden translate-y-12 sm:translate-y-16 scale-90 sm:scale-95 opacity-90" style="background-color: #f5efe4;">
                    <div class="absolute inset-0 p-2 sm:p-3 airmail-border">
                        <div class="w-full h-full bg-[#fbf7f0] rounded-sm relative p-4 sm:p-7 flex flex-col justify-between shadow-inner">
                            <div class="flex items-start justify-between">
                                <div>
                                    <h4 class="font-serif font-black text-xs sm:text-base text-slate-800 uppercase">PT MIDI UTAMA INDONESIA TBK</h4>
                                    <p class="text-[9px] sm:text-[11px] text-slate-600 font-serif mt-1">Alfa Tower Alam Sutera, Jl. Jalur Sutera Bar. No.Kav. 7-9 <br> Kota Tangerang, Banten, 15143</p>
                                </div>
                                <div class="w-16 h-20 bg-[#a35e38] p-1.5 rounded-sm shadow-md stamp-border flex items-center justify-center">
                                    <div class="w-full h-full bg-white flex flex-col items-center justify-center p-1">
                                        <img src="data:image/png;base64,%%LOGO_B64%%" alt="Alfamidi Logo" class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl border border-amber-400/40 shadow-xs object-cover" />
                                        <span class="text-[10px] font-black text-red-600 mt-1">Alfamidi</span>
                                    </div>
                                </div>
                            </div>

                            <div class="my-auto pl-4 py-2">
                                <div class="text-xs font-serif font-black text-red-800">TO : THE WINNER OF</div>
                                <div id="envelope-body-event-title" class="text-base sm:text-2xl font-serif font-black text-red-700 uppercase"><strong>SISTEM UNDIAN KARYAWAN</strong></div>
                                <div id="envelope-body-subtitle" class="text-[10px] sm:text-xs font-semibold text-slate-600 uppercase mt-1">HADIAH UTAMA • UNTUK PEMENANG</div>
                            </div>

                            <div class="flex justify-between text-[9px] text-slate-400 font-mono">
                                <span>AIRMAIL / PAR AVION</span>
                                <span>CONFIDENTIAL & OFFICIAL</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- MODAL 2: TABEL PEMENANG (>10 PEMENANG) -->
    <!-- ============================================================== -->
    <div id="modal-table" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/60 backdrop-blur-md">
        <div class="relative w-full max-w-5xl max-h-[85vh] h-auto my-auto flex flex-col bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden">
            <div class="bg-gradient-to-r from-red-700 via-red-600 to-red-700 p-4 text-white flex items-center justify-between">
                <div>
                    <span id="table-modal-winner-count-badge" class="text-xs font-bold text-amber-300">0 PEMENANG</span>
                    <h2 id="table-modal-event-title" class="text-lg font-black uppercase">SISTEM UNDIAN KARYAWAN</h2>
                    <p id="table-modal-category-name" class="text-xs text-red-100"></p>
                </div>
                <button id="btn-close-table-modal" class="p-2 text-white bg-white/10 rounded-full hover:bg-white/20">✕</button>
            </div>

            <div class="p-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between gap-3">
                <input id="input-search-table-modal" type="text" placeholder="Cari pemenang..." class="flex-1 max-w-md px-3 py-2 bg-white border border-slate-300 rounded-lg text-sm text-slate-900" />
                <div class="flex gap-2">
                    <button id="btn-table-copy-list" class="px-3 py-2 bg-slate-700 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg">Salin Teks</button>
                    <button id="btn-table-export-excel" class="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg">Unduh Excel</button>
                    <button id="btn-table-export-pdf" class="px-3 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg">Cetak PDF</button>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto">
                <table class="w-full text-left text-sm">
                    <thead id="table-modal-thead" class="sticky top-0 bg-slate-100 text-slate-700 text-xs uppercase font-bold border-b border-slate-200">
                    </thead>
                    <tbody id="table-modal-tbody" class="divide-y divide-slate-100"></tbody>
                </table>
            </div>

            <div class="p-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
                <div id="table-modal-pagination-info"></div>
                <div class="flex items-center gap-2">
                    <button id="btn-table-prev-page" class="p-1.5 rounded bg-slate-200 text-slate-800 font-bold hover:bg-slate-300">◀</button>
                    <span id="table-modal-page-num" class="text-slate-900 font-bold px-2"></span>
                    <button id="btn-table-next-page" class="p-1.5 rounded bg-slate-200 text-slate-800 font-bold hover:bg-slate-300">▶</button>
                    <button id="btn-table-bottom-close" class="ml-3 px-4 py-1.5 bg-slate-800 hover:bg-slate-900 text-white rounded-lg font-semibold">Tutup</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- DRAWER: RIWAYAT UNDIAN -->
    <!-- ============================================================== -->
    <div id="drawer-history" class="hidden fixed inset-0 z-50 flex items-center justify-end bg-slate-900/50 backdrop-blur-xs">
        <div class="w-full max-w-lg h-full bg-white border-l border-slate-200 shadow-2xl flex flex-col">
            <div class="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
                <h3 class="font-bold text-slate-900 text-base">Riwayat Putaran Undian</h3>
                <button id="btn-close-history-drawer" class="p-1.5 text-slate-400 hover:text-slate-800">✕</button>
            </div>
            <div id="drawer-history-list" class="flex-1 overflow-y-auto p-4 space-y-3"></div>
            <div class="p-3.5 border-t border-slate-200 bg-slate-50 flex justify-between items-center">
                <button id="btn-history-reset-all" class="text-xs font-bold text-red-600 hover:text-red-700">Reset Riwayat</button>
                <button id="btn-history-bottom-close" class="px-4 py-1.5 bg-slate-800 text-white text-xs font-semibold rounded-lg">Tutup</button>
            </div>
        </div>
    </div>

    <!-- SCRIPT LOGIC -->
    <script>
        // Audio Synthesizer
        class SoundFx {
            constructor() {
                this.ctx = null;
                this.enabled = true;
            }
            getCtx() {
                if (!this.enabled) return null;
                if (!this.ctx) {
                    const AudioContext = window.AudioContext || window.webkitAudioContext;
                    if (AudioContext) this.ctx = new AudioContext();
                }
                if (this.ctx && this.ctx.state === 'suspended') this.ctx.resume();
                return this.ctx;
            }
            playClick() {
                const ctx = this.getCtx();
                if (!ctx) return;
                const now = ctx.currentTime;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(160, now);
                osc.frequency.exponentialRampToValueAtTime(40, now + 0.12);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.13);
            }
            playTick() {
                const ctx = this.getCtx();
                if (!ctx) return;
                const now = ctx.currentTime;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(440 + Math.random() * 40 - 20, now);
                osc.frequency.exponentialRampToValueAtTime(220, now + 0.04);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.045);
            }
            playFanfare() {
                const ctx = this.getCtx();
                if (!ctx) return;
                const notes = [
                    { freq: 523.25, time: 0, d: 0.15 },
                    { freq: 659.25, time: 0.16, d: 0.15 },
                    { freq: 783.99, time: 0.32, d: 0.18 },
                    { freq: 1046.50, time: 0.52, d: 0.65 }
                ];
                const base = ctx.currentTime;
                notes.forEach(({ freq, time, d }) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, base + time);
                    gain.gain.setValueAtTime(0.25, base + time);
                    gain.gain.exponentialRampToValueAtTime(0.001, base + time + d);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(base + time);
                    osc.stop(base + time + d + 0.05);
                });
            }
        }
        const sound = new SoundFx();

        // Default Categories
        const defaultCategories = [
            { id: 'cat-1', name: 'Grand Prize - Sepeda Motor Honda Beat', winnerCount: 1 },
            { id: 'cat-2', name: 'Hadiah Utama 1 - Iphone 17 Pro Max', winnerCount: 3 },
            { id: 'cat-3', name: 'Hadiah Utama 2 - Apple Smartwatch', winnerCount: 5 },
            { id: 'cat-4', name: 'Hadiah Hiburan - Voucher Belanja Alfamidi Rp 400.000', winnerCount: 10 }
        ];

        // State
        const state = {
            candidates: [],
            columns: [],
            settings: {
                nameColumn: 'NAMA_KARYAWAN',
                useWeighting: false,
                weightColumn: 'POIN_UNDIAN',
                useFiltering: false,
                filterRules: [],
                winnerCount: 1,
                groupName: defaultCategories[0].name,
                displayColumns: ['NIK', 'JABATAN'],
                eventTitle: 'Alfamidi Lucky Draw 2026',
                allowDuplicateWinners: false,
                categories: defaultCategories,
            },
            wonIds: new Set(),
            drawHistory: [],
            recentWinners: null,
            allSessionWinners: [],
            lastDrawSession: null,
            isSpinning: false,
            activeTab: 'stage',
            tableSearchTerm: '',
            tableCurrentPage: 1,
            tablePageSize: 15,
            reelItems: [
                { name: 'ALFAMIDI', extra: 'SIAP UNDI' },
                { name: 'LUCKY DRAW', extra: 'SIAP UNDI' },
                { name: 'SYSTEM', extra: 'SIAP UNDI' },
            ],
        };

        const $ = id => document.getElementById(id);

        // Alfamidi Data Generator
        function generateAlfamidiData(count = 1000) {
            const firstNames = ['Agus', 'Budi', 'Siti', 'Dewi', 'Eko', 'Rina', 'Bambang', 'Wayan', 'Dian', 'Hendra', 'Rahmat', 'Nur', 'Yanto', 'Tri', 'Ahmad', 'Fitri', 'Wahyu', 'Putri', 'Hadi', 'Ratna'];
            const lastNames = ['Santoso', 'Pratama', 'Kusuma', 'Wijaya', 'Saputra', 'Lestari', 'Hidayat', 'Nugroho', 'Wibowo', 'Firmansyah', 'Suryono', 'Utomo', 'Siregar', 'Gunawan', 'Hartono'];
            const positions = ['Store Crew', 'Cashier Staff', 'Store Leader (Kepala Toko)', 'Assistant Store Leader', 'Area Coordinator', 'Warehouse Staff', 'IT Support', 'Human Capital Officer'];
            const branches = ['Cabang Tangerang (Head Office)', 'Cabang Bekasi', 'Cabang Bogor', 'Cabang Medan', 'Cabang Makassar', 'Cabang Manado', 'Cabang Samarinda', 'Cabang Yogyakarta'];

            const rows = [];
            for (let i = 1; i <= count; i++) {
                const fn = firstNames[Math.floor(Math.random() * firstNames.length)];
                const ln = lastNames[Math.floor(Math.random() * lastNames.length)];
                const pos = positions[Math.floor(Math.random() * positions.length)];
                const br = branches[Math.floor(Math.random() * branches.length)];
                const tenure = Math.floor(Math.random() * 15) + 1;
                const points = tenure * 10 + Math.floor(Math.random() * 80) + 10;
                rows.push({
                    _id: `MIDI-${100000 + i}`,
                    NIK: `MIDI-${100000 + i}`,
                    NAMA_KARYAWAN: `${fn} ${ln}`,
                    JABATAN: pos,
                    CABANG: br,
                    MASA_KERJA_TAHUN: tenure,
                    POIN_UNDIAN: points,
                });
            }
            return {
                headers: ['NIK', 'NAMA_KARYAWAN', 'JABATAN', 'CABANG', 'MASA_KERJA_TAHUN', 'POIN_UNDIAN'],
                rows
            };
        }

        function applyData(headers, rows) {
            state.candidates = rows;
            state.wonIds.clear();
            state.recentWinners = null;
            state.allSessionWinners = [];
            state.lastDrawSession = null;
            state.columns = headers.map(h => ({
                name: h,
                isNumeric: rows.slice(0, 50).every(r => typeof r[h] === 'number' || (!isNaN(Number(r[h])) && r[h] !== ''))
            }));

            const foundNameCol = headers.find(h => /nama|name/i.test(h)) || headers[0];
            
            state.settings.nameColumn = foundNameCol;
            // Gunakan 2 kolom awal sebagai default tanpa memaksa memasukkan NAMA
            state.settings.displayColumns = headers.slice(0, 2);

            updateUI();
        }
        
        function passesFilters(candidate) {
            if (!state.settings.useFiltering || state.settings.filterRules.length === 0) return true;
            
            return state.settings.filterRules.every(rule => {
                const val = candidate[rule.column];
                const target = rule.value;
                if (val === undefined || val === null) return false;

                const numVal = Number(val);
                const numTarget = Number(target);
                const isNumericComparison = !isNaN(numVal) && !isNaN(numTarget) && String(target).trim() !== '';

                switch (rule.operator) {
                    case '=':
                        return isNumericComparison ? numVal === numTarget : String(val).toLowerCase() === String(target).toLowerCase();
                    case '!=':
                        return isNumericComparison ? numVal !== numTarget : String(val).toLowerCase() !== String(target).toLowerCase();
                    case 'contains':
                        return String(val).toLowerCase().includes(String(target).toLowerCase());
                    case '>':
                        return isNumericComparison && numVal > numTarget;
                    case '>=':
                        return isNumericComparison && numVal >= numTarget;
                    case '<':
                        return isNumericComparison && numVal < numTarget;
                    case '<=':
                        return isNumericComparison && numVal <= numTarget;
                    default:
                        return true;
                }
            });
        }

        // Weighted Draw Engine
        function executeDraw() {
            let pool = state.candidates;
            
            // Terapkan Filter Kriteria jika aktif
            if (state.settings.useFiltering && state.settings.filterRules.length > 0) {
                pool = pool.filter(passesFilters);
            }

            if (!state.settings.allowDuplicateWinners && state.wonIds.size > 0) {
                pool = pool.filter(c => !state.wonIds.has(c._id));
            }
            
            if (pool.length === 0) return [];
            const k = Math.min(state.settings.winnerCount, pool.length);

            let selected = [];
            if (state.settings.useWeighting && state.settings.weightColumn) {
                const wCol = state.settings.weightColumn;
                const scored = pool.map(c => {
                    const rawW = Number(c[wCol]);
                    // Jika poin 0 atau kosong, beri nilai 0 (tidak punya tiket undian)
                    const w = isNaN(rawW) || rawW <= 0 ? 0 : rawW; 
                    
                    // Algoritma Weighted Efraimidis-Spirakis
                    return { c, score: w > 0 ? Math.pow(Math.random(), 1 / w) : -1, w };
                }).filter(item => item.score >= 0); // Eliminasi total peserta berpoin 0 dari undian

                scored.sort((a, b) => b.score - a.score);
                selected = scored.slice(0, k).map(s => s.c);
            } else {
                const copy = [...pool];
                for (let i = 0; i < k; i++) {
                    const j = i + Math.floor(Math.random() * (copy.length - i));
                    [copy[i], copy[j]] = [copy[j], copy[i]];
                }
                selected = copy.slice(0, k);
            }

            return selected.map((cand, idx) => {
                const selectedCols = state.settings.displayColumns;
                
                // Ambil hanya nilai dari kolom-kolom yang dicentang
                const parts = selectedCols.map(col => String(cand[col] ?? '')).filter(p => p.trim() !== '');
                
                // Jika tidak ada kolom dicentang, fallback ke kolom utama
                const formattedText = parts.length > 0 ? parts.join(' - ') : String(cand[state.settings.nameColumn] || '-');
                
                // Teks Utama Reels (Elemen pertama yang dicentang)
                const mainTitle = selectedCols.length > 0 ? String(cand[selectedCols[0]] ?? '-') : String(cand[state.settings.nameColumn] || '-');

                return {
                    id: cand._id,
                    rank: idx + 1,
                    name: mainTitle, // Digunakan untuk judul kartu/reel
                    displayFormatted: formattedText, // Format lengkap sesuai centang
                    data: cand,
                    group: state.settings.groupName,
                    drawTimestamp: new Date().toISOString()
                };
            });
        }

        // Render Function
        function updateUI() {
            $('info-active-group').textContent = state.settings.groupName;
            $('info-winner-count').textContent = `${state.settings.winnerCount} Pemenang`;
            $('info-format-preview').textContent = state.settings.displayColumns.length > 0 
                ? `[${state.settings.displayColumns.join(' - ')}]` 
                : '[Tidak Ada Kolom Dipilih]';

            // Hitung kandidat yang lolos filter
            let pool = state.candidates;
            if (state.settings.useFiltering && state.settings.filterRules.length > 0) {
                pool = pool.filter(passesFilters);
            }

            const available = state.settings.allowDuplicateWinners
                ? pool.length
                : Math.max(0, pool.filter(c => !state.wonIds.has(c._id)).length);

            $('info-candidate-stats').textContent = `${available.toLocaleString('id-ID')} / ${state.candidates.length.toLocaleString('id-ID')}`;
            $('bottom-total-candidates').textContent = state.candidates.length.toLocaleString('id-ID');
            $('config-available-count').textContent = available.toLocaleString('id-ID');
            $('data-active-counter-text').textContent = `${state.candidates.length.toLocaleString('id-ID')} Peserta Aktif`;

            // Stage category select
            const catSelect = $('stage-category-select');
            catSelect.innerHTML = state.settings.categories.map(c => `
        <option value="${c.name}" ${c.name === state.settings.groupName ? 'selected' : ''}>${c.name} (${c.winnerCount} Pemenang)</option>
    `).join('');
            $('stage-winner-count-input').value = state.settings.winnerCount;

            // Quick count chips styling (Light Theme)
            document.querySelectorAll('.btn-quick-count').forEach(btn => {
                const cnt = Number(btn.getAttribute('data-count'));
                if (cnt === state.settings.winnerCount) {
                    btn.className = 'btn-quick-count px-2.5 py-1 text-xs font-black rounded-lg bg-red-600 text-white shadow-2xs cursor-pointer border border-red-600';
                } else {
                    btn.className = 'btn-quick-count px-2.5 py-1 text-xs font-bold rounded-lg bg-white text-slate-700 hover:bg-red-50 hover:text-red-600 cursor-pointer border border-slate-200';
                }
            });

            // Last modal button
            if (state.lastDrawSession && state.lastDrawSession.winners.length > 0) {
                $('btn-view-last-modal').classList.remove('hidden');
                $('btn-bottom-last-modal').classList.remove('hidden');
                $('btn-bottom-last-modal-text').textContent = `Lihat Modal Terakhir (${state.lastDrawSession.winners.length})`;
            } else {
                $('btn-view-last-modal').classList.add('hidden');
                $('btn-bottom-last-modal').classList.add('hidden');
            }

            // History count
            if (state.drawHistory.length > 0) {
                $('history-badge-count').textContent = state.drawHistory.length;
                $('history-badge-count').classList.remove('hidden');
                $('history-badge-count').classList.add('flex');
            } else {
                $('history-badge-count').classList.add('hidden');
            }

            renderReels();
            renderConfig();
            renderDataPreview();
        }

        // Render Slot Reels (Identik Gambar 2)
        function renderReels() {
            const container = $('slot-reels-grid');
            const num = Math.min(3, Math.max(1, state.settings.winnerCount));
            container.className = `w-full grid gap-4 sm:gap-6 relative z-0 ${num === 1 ? 'grid-cols-1 max-w-xs mx-auto' : num === 2 ? 'grid-cols-2 max-w-xl mx-auto' : 'grid-cols-1 sm:grid-cols-3'}`;

            const isSlotWinner = state.recentWinners && state.recentWinners.length <= 3 && !state.isSpinning;
            container.innerHTML = '';

            const avatarSvg = `<svg class="w-12 h-12 text-slate-400 mb-1" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>`;

            for (let i = 0; i < num; i++) {
                const item = state.reelItems[i] || { name: 'ALFAMIDI', extra: 'SIAP UNDI' };
                const winner = isSlotWinner && state.recentWinners ? state.recentWinners[i] : null;

                const el = document.createElement('div');
                el.className = `h-36 sm:h-44 rounded-2xl border-2 flex flex-col items-center justify-center text-center p-3 transition-all relative overflow-hidden ${
                    winner 
                        ? 'bg-gradient-to-b from-red-50 via-white to-red-50 border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.3)]' 
                        : 'bg-white border-slate-200 text-slate-800 shadow-2xs'
                }`;
                el.innerHTML = `
        ${winner ? `<span class="absolute top-2 right-2 px-2.5 py-0.5 bg-red-600 text-white text-[10px] font-black rounded-full shadow-2xs">Pemenang #${i + 1}</span>` : ''}
        <div class="w-full flex flex-col items-center justify-center my-auto">
            ${winner ? '' : avatarSvg}
            <p class="font-extrabold text-sm sm:text-base md:text-lg tracking-tight uppercase line-clamp-2 px-1 ${winner ? 'text-red-600' : 'text-slate-800'}">
            ${winner ? winner.name : item.name}
            </p>
            <p class="text-xs font-semibold mt-1 line-clamp-2 px-1 ${winner ? 'text-slate-700' : 'text-slate-400'}">
            ${winner ? winner.displayFormatted : item.extra}
            </p>
        </div>
        `;
                container.appendChild(el);
            }

            if (isSlotWinner) $('btn-reset-draw').classList.remove('hidden');
            else $('btn-reset-draw').classList.add('hidden');

            renderBottomWinnerSlots();
        }

        // Render Bottom Winner Cards (Bagian Bawah Gambar 2)
        function renderBottomWinnerSlots() {
            const container = $('bottom-winner-slots');
            container.innerHTML = '';
            
            const winners = state.allSessionWinners.slice(0, 3);
            const countToShow = 3;
            const avatarSvgSmall = `<svg class="w-8 h-8 text-slate-400 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>`;

            for (let i = 0; i < countToShow; i++) {
                const w = winners[i] || null;
                const el = document.createElement('div');
                el.className = 'flex items-center gap-2.5 p-2 sm:p-2.5 rounded-full bg-slate-50 border border-slate-200 shadow-2xs';
                el.innerHTML = `
                    ${avatarSvgSmall}
                    <div class="flex-1 min-w-0 pr-2">
                        <p class="text-xs font-bold text-slate-800 truncate">${w ? w.name : '-'}</p>
                        <p class="text-[10px] text-slate-500 truncate">${w ? w.displayFormatted : '-'}</p>
                    </div>
                `;
                container.appendChild(el);
            }
        }
        
        function renderConfig() {
            $('input-event-title').value = state.settings.eventTitle;
            $('marquee-event-title').textContent = state.settings.eventTitle;
            $('textarea-bulk-categories').value = state.settings.categories.map(c => `${c.name} | ${c.winnerCount}`).join('\\n');
            $('config-categories-count').textContent = `${state.settings.categories.length} Kategori Aktif`;

            $('config-categories-chips').innerHTML = state.settings.categories.map(c => `
        <div class="flex items-center justify-between p-2 rounded-lg bg-white border border-slate-200 text-xs">
        <span class="font-semibold text-slate-800 truncate">${c.name} (${c.winnerCount} pemenang)</span>
        <button class="btn-del-cat text-slate-400 hover:text-red-600 font-bold" data-id="${c.id}">✕</button>
        </div>
    `).join('');

            $('select-name-column').innerHTML = state.columns.map(c => `
        <option value="${c.name}" ${c.name === state.settings.nameColumn ? 'selected' : ''}>${c.name}</option>
    `).join('');

            $('input-default-winner-count').value = state.settings.winnerCount;
            $('label-default-winner-count').textContent = `${state.settings.winnerCount} Orang`;

            const n = state.settings.winnerCount;
            $('animation-notice-text').textContent = n <= 3 ? 'Animasi yang ditampilkan : 🎰 Slot Machine' : n <= 10 ? 'Animasi yang ditampilkan : ✉️ Animasi Surat' : 'Animasi yang ditampilkan : 📊 Tabel Pemenang';

            $('select-weight-column').innerHTML = state.columns.map(c => `
        <option value="${c.name}" ${c.name === state.settings.weightColumn ? 'selected' : ''}>${c.name} ${c.isNumeric ? '⭐ (Angka)' : ''}</option>
    `).join('');

            $('config-format-sample-box').textContent = [state.settings.nameColumn, ...state.settings.displayColumns.filter(c => c !== state.settings.nameColumn)].join(' - ');
            
            // UBAH JUDUL SECTION DI PENGATURAN
            const labelHeader = document.querySelector('label[for="config-display-checkboxes-grid"]') || $('config-format-sample-box')?.previousElementSibling;
            
            // Render Checkbox untuk SELURUH Kolom Tanpa Pengecualian
            $('config-display-checkboxes-grid').innerHTML = state.columns.map(c => `
                <button type="button" class="btn-toggle-col flex items-center gap-2 p-2 rounded-lg text-xs border ${
                    state.settings.displayColumns.includes(c.name) 
                        ? 'bg-red-50 border-red-500 text-red-700 font-bold' 
                        : 'bg-white border-slate-200 text-slate-600'
                }" data-col="${c.name}">
                    <span>${state.settings.displayColumns.includes(c.name) ? '☑' : '☐'}</span>
                    <span class="truncate">${c.name}</span>
                </button>
            `).join('');

            // Update Sample Format sesuai kolom yang DICENTANG SAJA
            const selected = state.settings.displayColumns;
            $('config-format-sample-box').textContent = selected.length > 0 
                ? selected.join(' - ') 
                : '(Tidak ada kolom dipilih)';
                
        $('select-filter-column').innerHTML = state.columns.map(c => `
            <option value="${c.name}">${c.name}</option>
        `).join('');

        // Render daftar badge/chip filter yang aktif
        $('filter-chips-list').innerHTML = state.settings.filterRules.map(r => `
            <div class="flex items-center justify-between p-2 rounded-lg bg-white border border-slate-200 text-xs">
                <span class="font-semibold text-slate-800">
                    <strong class="text-red-600">${r.column}</strong> ${r.operator} "<span class="text-slate-900">${r.value}</span>"
                </span>
                <button class="btn-del-filter text-slate-400 hover:text-red-600 font-bold cursor-pointer" data-id="${r.id}">✕</button>
            </div>
        `).join('');

        }

        function renderDataPreview() {
            if (state.columns.length === 0) return;
            $('data-preview-thead').innerHTML = '<tr><th class="py-2 px-3">#</th>' + state.columns.map(c => `<th class="py-2 px-3">${c.name}</th>`).join('') + '</tr>';
            $('data-preview-tbody').innerHTML = state.candidates.slice(0, 5).map((row, idx) => `
        <tr><td class="py-2 px-3">${idx + 1}</td>${state.columns.map(c => `<td class="py-2 px-3 text-slate-700">${row[c.name] ?? ''}</td>`).join('')}</tr>
    `).join('');
        }

        // Modal Envelope Open
        function openEnvelope(winners, group, title) {
            $('modal-envelope').classList.remove('hidden');
            $('letter-category-name').textContent = group;
            $('letter-event-title').textContent = title;
            $('envelope-body-event-title').textContent = title;
            $('envelope-body-subtitle').textContent = `${group} • UNTUK ${winners.length} ORANG PEMENANG`;
            $('letter-subtitle').textContent = `Selamat kepada ${winners.length} rekan karyawan Alfamidi berikut:`;
            $('letter-total-winners-count').textContent = `TOTAL: ${winners.length} PEMENANG`;
            $('letter-current-date').textContent = new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });

            $('envelope-winners-list').innerHTML = winners.map((w, i) => `
        <div class="flex items-start gap-3 p-3 bg-red-50/80 rounded-lg border border-red-100">
        <div class="w-7 h-7 rounded-full bg-red-600 text-white font-extrabold text-xs flex items-center justify-center flex-shrink-0">${w.rank}</div>
        <div class="flex-1"><p class="text-sm font-bold text-slate-900">${w.displayFormatted}</p></div>
        <span class="text-emerald-600 font-bold text-xs">✓ Terpilih</span>
        </div>
    `).join('');

            sound.playFanfare();
            confetti({ particleCount: 80, spread: 70, origin: { y: 0.6 } });
        }

        // Modal Table Open
        function openTable(winners, group, title) {
            $('modal-table').classList.remove('hidden');
            $('table-modal-winner-count-badge').textContent = `${winners.length} PEMENANG`;
            $('table-modal-event-title').textContent = title;
            $('table-modal-category-name').textContent = group;

            // ================= TAMBAHKAN 3 BARIS INI =================
            state.tableCurrentPage = 1; // Reset halaman ke 1 tiap kali modal dibuka
            state.tableSearchTerm = ''; // Reset kata kunci pencarian
            $('input-search-table-modal').value = '';
            // =========================================================

            renderTableRows(winners);
            sound.playFanfare();
            confetti({ particleCount: 90, spread: 100, origin: { y: 0.4 } });
            updateStreamlitFrameHeight();
        }

        function renderTableRows(winners) {
            const term = state.tableSearchTerm.toLowerCase();
            const filtered = !term ? winners : winners.filter(w => w.name.toLowerCase().includes(term) || w.displayFormatted.toLowerCase().includes(term));
            const totalPages = Math.max(1, Math.ceil(filtered.length / state.tablePageSize));

            // ================= TAMBAHKAN SANITASI INI =================
            // Mencegah halaman melampaui batas total halaman yang ada
            if (state.tableCurrentPage > totalPages || state.tableCurrentPage < 1) {
                state.tableCurrentPage = 1;
            }
            // =========================================================

            const start = (state.tableCurrentPage - 1) * state.tablePageSize;
            const paginated = filtered.slice(start, start + state.tablePageSize);

            $('table-modal-thead').innerHTML = `
        <tr>
        <th class="py-3 px-4 w-14 text-center">No</th>
        <th class="py-3 px-4">Nama</th>
        <th class="py-3 px-4">Format Pengumuman</th>
        ${state.settings.displayColumns.map(c => `<th class="py-3 px-4">${c}</th>`).join('')}
        </tr>
    `;

            $('table-modal-tbody').innerHTML = paginated.map((w, idx) => `
        <tr class="hover:bg-slate-50">
        <td class="py-3 px-4 text-center font-bold text-red-600">${start + idx + 1}</td>
        <td class="py-3 px-4 font-bold text-slate-900">${w.name}</td>
        <td class="py-3 px-4 text-slate-700"><span class="px-2 py-1 rounded bg-slate-100 text-xs font-semibold">${w.displayFormatted}</span></td>
        ${state.settings.displayColumns.map(c => `<td class="py-3 px-4 text-slate-600 text-xs">${w.data[c] ?? '-'}</td>`).join('')}
        </tr>
    `).join('');

            $('table-modal-pagination-info').textContent = `Menampilkan ${start + 1} - ${Math.min(start + state.tablePageSize, filtered.length)} dari ${filtered.length} pemenang`;
            $('table-modal-page-num').textContent = `Halaman ${state.tableCurrentPage} / ${totalPages}`;
        }

        // Export Excel
        function exportExcel(winners, group, title) {
            const rows = winners.map(w => ({
                'No. Urut': w.rank,
                'Kategori Hadiah': group,
                'Nama Pemenang': w.name,
                'Format Lengkap': w.displayFormatted,
                ...w.data,
                'Waktu Undian': new Date(w.drawTimestamp).toLocaleString('id-ID')
            }));
            const ws = XLSX.utils.json_to_sheet(rows);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Pemenang Undian");
            XLSX.writeFile(wb, `Alfamidi_${group}_${Date.now()}.xlsx`);
        }

        // Export PDF
        function exportPDF(winners, group, title) {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.setFillColor(215, 25, 32);
            doc.rect(0, 0, 210, 8, 'F');
            doc.setFontSize(15);
            doc.setTextColor(30, 41, 59);
            doc.text("PT MIDI UTAMA INDONESIA TBK", 14, 20);
            doc.setFontSize(9);
            doc.text("Alfa Tower Alam Sutera, Tangerang, Banten", 14, 26);
            doc.setFontSize(13);
            doc.setTextColor(215, 25, 32);
            doc.text("BERITA ACARA RESMI PENGUNDIAN DOORPRIZE", 14, 38);
            doc.setFontSize(10);
            doc.setTextColor(51, 65, 85);
            doc.text(`Acara: ${title} | Kategori: ${group} | Total: ${winners.length} Pemenang`, 14, 46);

            const tableData = winners.map(w => [w.rank, w.name, w.displayFormatted]);
            doc.autoTable({
                startY: 52,
                head: [['No', 'Nama Pemenang', 'Format Lengkap']],
                body: tableData,
                headStyles: { fillColor: [215, 25, 32] }
            });
            doc.save(`Berita_Acara_Alfamidi_${Date.now()}.pdf`);
        }

        // Spin Start
        function startSpin() {
            if (state.isSpinning || state.candidates.length === 0) return;
            const winners = executeDraw();
            if (winners.length === 0) {
                alert('Tidak ada peserta yang tersisa untuk diundi.');
                return;
            }

            state.isSpinning = true;
            state.recentWinners = null;
            sound.playClick();

            $('btn-main-spin-text').textContent = 'MENGUNDI...';

            let count = 0;
            const interval = setInterval(() => {
                count++;
                if (count % 3 === 0) sound.playTick();
                state.reelItems = [1, 2, 3].map(() => {
                    const c = state.candidates[Math.floor(Math.random() * state.candidates.length)];
                    const selectedCols = state.settings.displayColumns;
                    
                    // Baris Atas Reel = Kolom Centang Pertama
                    const topCol = selectedCols[0] || state.settings.nameColumn;
                    // Baris Bawah Reel = Kolom-kolom Centang Sisanya
                    const subCols = selectedCols.slice(1);
                    
                    const rName = c[topCol] ?? 'Alfamidi';
                    const rExtra = subCols.length > 0 
                        ? subCols.map(col => c[col]).filter(Boolean).join(' - ') 
                        : (selectedCols.length === 1 ? '' : 'Peserta');

                    return { name: String(rName), extra: String(rExtra) };
                });
                renderReels();
            }, 50);

            setTimeout(() => {
                clearInterval(interval);
                state.isSpinning = false;
                state.recentWinners = winners;
                state.allSessionWinners.unshift(...winners);
                state.lastDrawSession = { winners, groupName: state.settings.groupName, eventTitle: state.settings.eventTitle };
                $('btn-main-spin-text').textContent = 'SPIN LAGI';

                // Add history
                state.drawHistory.unshift({
                    id: `draw-${Date.now()}`,
                    groupName: state.settings.groupName,
                    eventTitle: state.settings.eventTitle,
                    timestamp: new Date().toISOString(),
                    winners
                });

                if (!state.settings.allowDuplicateWinners) {
                    winners.forEach(w => state.wonIds.add(w.id));
                }

                updateUI();

                if (state.settings.winnerCount <= 3) {
                    sound.playFanfare();
                    confetti({ particleCount: 75, spread: 80, origin: { y: 0.55 } });
                } else if (state.settings.winnerCount <= 10) {
                    openEnvelope(winners, state.settings.groupName, state.settings.eventTitle);
                } else {
                    openTable(winners, state.settings.groupName, state.settings.eventTitle);
                }
            }, state.settings.winnerCount <= 3 ? 2400 : 2000);
        }

        // Events Setup
        function init() {
            // Load 1000 demo candidates
            const demo = generateAlfamidiData(1000);
            applyData(demo.headers, demo.rows);

            // Tab switcher
            $('tab-btn-stage').onclick = () => switchTab('stage');
            $('tab-btn-config').onclick = () => switchTab('config');
            $('tab-btn-data').onclick = () => switchTab('data');

            // Spin triggers
            $('btn-arcade-red-button').onclick = startSpin;
            $('btn-main-spin').onclick = startSpin;
            $('btn-reset-draw').onclick = () => {
                if (!state.lastDrawSession) return;

                // 1. Hapus ID pemenang sesi terakhir dari Set wonIds (mengembalikan ke pool peserta)
                state.lastDrawSession.winners.forEach(w => state.wonIds.delete(w.id));

                // 2. Hapus pemenang sesi terakhir dari daftar akumulasi Latest Winner
                const lastWinnerIds = new Set(state.lastDrawSession.winners.map(w => w.id));
                state.allSessionWinners = state.allSessionWinners.filter(w => !lastWinnerIds.has(w.id));

                // 3. Hapus entri putaran terakhir dari riwayat (drawHistory)
                if (state.drawHistory.length > 0) {
                    state.drawHistory.shift();
                }

                // 4. Perbarui rujukan sesi terakhir ke putaran sebelumnya (jika ada)
                state.lastDrawSession = state.drawHistory.length > 0 ? state.drawHistory[0] : null;

                // 5. Reset status pemenang reel saat ini
                state.recentWinners = null;

                // 6. Perbarui UI untuk menghitung ulang sisa peserta & memperbarui kartu pemenang
                updateUI();
            };

            // Category select
            $('stage-category-select').onchange = e => {
                state.settings.groupName = e.target.value;
                const matched = state.settings.categories.find(c => c.name === e.target.value);
                if (matched) state.settings.winnerCount = matched.winnerCount;
                updateUI();
            };

            // Winner count input
            $('stage-winner-count-input').oninput = e => {
                state.settings.winnerCount = Math.max(1, parseInt(e.target.value) || 1);
                updateUI();
            };
            
            // Quick count chips click event
            document.querySelectorAll('.btn-quick-count').forEach(btn => {
                btn.onclick = () => {
                    state.settings.winnerCount = Number(btn.getAttribute('data-count'));
                    updateUI();
                };
            });

            // Sound toggle
            $('btn-toggle-sound').onclick = () => {
                sound.enabled = !sound.enabled;
                $('sound-status-text').textContent = sound.enabled ? 'Suara ON' : 'Mute';
            };

            // Modals
            $('btn-close-envelope-modal').onclick = () => $('modal-envelope').classList.add('hidden');
            $('btn-envelope-finish').onclick = () => $('modal-envelope').classList.add('hidden');
            $('btn-close-table-modal').onclick = () => {
                $('modal-table').classList.add('hidden');
                updateStreamlitFrameHeight();
            };
            $('btn-table-bottom-close').onclick = () => {
                $('modal-table').classList.add('hidden');
                updateStreamlitFrameHeight();
            };

            $('btn-view-last-modal').onclick = reopenLast;
            $('btn-bottom-last-modal').onclick = reopenLast;

            function reopenLast() {
                if (!state.lastDrawSession) return;
                const { winners, groupName, eventTitle } = state.lastDrawSession;
                if (winners.length <= 10) openEnvelope(winners, groupName, eventTitle);
                else openTable(winners, groupName, eventTitle);
            }

            // History
            $('btn-open-history').onclick = () => {
                $('drawer-history').classList.remove('hidden');
                $('drawer-history-list').innerHTML = state.drawHistory.map(h => `
        <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1">
            <div class="flex justify-between items-center">
            <strong class="text-slate-900">${h.groupName} (${h.winners.length} Pemenang)</strong>
            <button class="btn-prev-h text-red-600 font-bold hover:underline" data-id="${h.id}">👁️ Buka</button>
            </div>
            <div class="text-slate-500 truncate">${h.winners.map(w => w.name).join(', ')}</div>
        </div>
        `).join('');

                document.querySelectorAll('.btn-prev-h').forEach(b => {
                    b.onclick = () => {
                        const h = state.drawHistory.find(x => x.id === b.getAttribute('data-id'));
                        if (h) {
                            $('drawer-history').classList.add('hidden');
                            if (h.winners.length <= 10) openEnvelope(h.winners, h.groupName, h.eventTitle);
                            else openTable(h.winners, h.groupName, h.eventTitle);
                        }
                    };
                });
            };
            $('btn-close-history-drawer').onclick = () => $('drawer-history').classList.add('hidden');
            $('btn-history-bottom-close').onclick = () => $('drawer-history').classList.add('hidden');
        $('btn-history-reset-all').onclick = () => {
            if (confirm('Hapus seluruh riwayat undian?')) {
                state.drawHistory = [];
                state.wonIds.clear();
                state.recentWinners = null;
                state.allSessionWinners = []; // <--- Reset akumulasi pemenang
                state.lastDrawSession = null;
                $('drawer-history').classList.add('hidden');
                updateUI();
            }
        };

            // Exports
            $('btn-envelope-export-excel').onclick = () => exportExcel(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle);
            $('btn-envelope-export-pdf').onclick = () => exportPDF(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle);
            $('btn-table-export-excel').onclick = () => exportExcel(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle);
            $('btn-table-export-pdf').onclick = () => exportPDF(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle);

            // Data sample buttons
            $('btn-load-sample-1k').onclick = () => { const d = generateAlfamidiData(1000); applyData(d.headers, d.rows); };
            $('btn-load-sample-10k').onclick = () => { const d = generateAlfamidiData(10000); applyData(d.headers, d.rows); };
            $('btn-load-sample-25k').onclick = () => { const d = generateAlfamidiData(25000); applyData(d.headers, d.rows); };

            // Config Bulk Apply
            $('btn-apply-bulk-categories').onclick = () => {
                const raw = $('textarea-bulk-categories').value;
                const lines = raw.split('\\n').map(l => l.trim()).filter(Boolean);
                state.settings.categories = lines.map((l, i) => {
                    const parts = l.split('|');
                    return { id: `cat-${i}`, name: parts[0].trim(), winnerCount: parseInt(parts[1]) || 1 };
                });
                if (state.settings.categories.length === 0) state.settings.categories = defaultCategories;
                state.settings.groupName = state.settings.categories[0].name;
                state.settings.winnerCount = state.settings.categories[0].winnerCount;
                updateUI();
            };
            $('btn-save-to-stage').onclick = () => switchTab('stage');

            // Subtabs
            document.querySelectorAll('.subtab-btn').forEach(btn => {
                btn.onclick = () => {
                    document.querySelectorAll('.subtab-btn').forEach(b => b.className = 'subtab-btn px-3.5 py-2 rounded-lg text-xs font-bold text-slate-600');
                    btn.className = 'subtab-btn active px-3.5 py-2 rounded-lg text-xs font-bold bg-red-600 text-white';
                    document.querySelectorAll('.data-subpanel').forEach(p => p.classList.add('hidden'));
                    $(btn.getAttribute('data-target')).classList.remove('hidden');
                };
            });

            // Excel upload
            $('input-file-excel').onchange = async e => {
                const file = e.target.files[0];
                if (!file) return;
                const buf = await file.arrayBuffer();
                const wb = XLSX.read(buf, { type: 'array' });
                const ws = wb.Sheets[wb.SheetNames[0]];
                const json = XLSX.utils.sheet_to_json(ws);
                if (json.length > 0) {
                    applyData(Object.keys(json[0]), json.map((r, i) => ({ _id: `row-${i}`, ...r })));
                    $('data-import-alert').className = 'p-3 rounded-xl text-xs font-bold bg-emerald-50 border border-emerald-300 text-emerald-800';
                    $('data-import-alert').textContent = `Berhasil memuat ${json.length} entri Excel!`;
                    $('data-import-alert').classList.remove('hidden');
                }
            };

            // Search Table
            $('input-search-table-modal').oninput = e => {
                state.tableSearchTerm = e.target.value;
                state.tableCurrentPage = 1;
                if (state.lastDrawSession) renderTableRows(state.lastDrawSession.winners);
            };
            $('btn-table-prev-page').onclick = () => {
                state.tableCurrentPage = Math.max(1, state.tableCurrentPage - 1);
                if (state.lastDrawSession) renderTableRows(state.lastDrawSession.winners);
            };
            $('btn-table-next-page').onclick = () => {
                if (!state.lastDrawSession) return;
                const term = state.tableSearchTerm.toLowerCase();
                const winners = state.lastDrawSession.winners;
                const filtered = !term ? winners : winners.filter(w => w.name.toLowerCase().includes(term) || w.displayFormatted.toLowerCase().includes(term));
                const totalPages = Math.max(1, Math.ceil(filtered.length / state.tablePageSize));

                if (state.tableCurrentPage < totalPages) {
                    state.tableCurrentPage++;
                    renderTableRows(winners);
                }
            };

            // --- 1. EVENT LISTENER TAB PENGATURAN ---
            $('input-event-title').oninput = e => {
                state.settings.eventTitle = e.target.value;
                $('marquee-event-title').textContent = e.target.value;
            };

            $('select-name-column').onchange = e => {
                state.settings.nameColumn = e.target.value;
                updateUI();
            };

            $('input-default-winner-count').oninput = e => {
                state.settings.winnerCount = Math.max(1, parseInt(e.target.value) || 1);
                updateUI();
            };

            document.querySelectorAll('.btn-config-quick-count').forEach(btn => {
                btn.onclick = () => {
                    state.settings.winnerCount = Number(btn.getAttribute('data-count'));
                    updateUI();
                };
            });

            $('checkbox-use-weighting').onchange = e => {
                state.settings.useWeighting = e.target.checked;
                $('weight-column-container').classList.toggle('hidden', !e.target.checked);
            };

            $('select-weight-column').onchange = e => {
                state.settings.weightColumn = e.target.value;
            };

            $('checkbox-prevent-duplicate').onchange = e => {
                state.settings.allowDuplicateWinners = !e.target.checked;
            };

            document.addEventListener('click', e => {
                if (e.target.closest('.btn-del-cat')) {
                    const id = e.target.closest('.btn-del-cat').getAttribute('data-id');
                    state.settings.categories = state.settings.categories.filter(c => c.id !== id);
                    if (state.settings.categories.length === 0) {
                        state.settings.categories = [{ id: 'cat-0', name: 'Default', winnerCount: 1 }];
                    }
                    state.settings.groupName = state.settings.categories[0].name;
                    state.settings.winnerCount = state.settings.categories[0].winnerCount;
                    updateUI();
                }

                if (e.target.closest('.btn-toggle-col')) {
                    const col = e.target.closest('.btn-toggle-col').getAttribute('data-col');
                    if (state.settings.displayColumns.includes(col)) {
                        state.settings.displayColumns = state.settings.displayColumns.filter(c => c !== col);
                    } else {
                        state.settings.displayColumns.push(col);
                    }
                    updateUI();
                }
                
                if (e.target.closest('.btn-del-filter')) {
                    const id = e.target.closest('.btn-del-filter').getAttribute('data-id');
                    state.settings.filterRules = state.settings.filterRules.filter(r => r.id !== id);
                    updateUI();
                }
            });

            // --- 2. EVENT LISTENER TAB DATA PESERTA ---
            $('input-file-csv').onchange = e => {
                const file = e.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = ev => {
                    const rows = ev.target.result.split('\\n').filter(r => r.trim());
                    if (rows.length > 1) {
                        const headers = rows[0].split(',').map(h => h.trim());
                        const data = rows.slice(1).map((r, i) => {
                            const vals = r.split(',');
                            let obj = { _id: `csv-${i}` };
                            headers.forEach((h, j) => obj[h] = vals[j] ? vals[j].trim() : '');
                            return obj;
                        });
                        applyData(headers, data);
                        $('data-import-alert').className = 'p-3 rounded-xl text-xs font-bold bg-emerald-50 border border-emerald-300 text-emerald-800';
                        $('data-import-alert').textContent = `Berhasil memuat ${data.length} entri CSV!`;
                        $('data-import-alert').classList.remove('hidden');
                    }
                };
                reader.readAsText(file);
            };

            $('btn-apply-manual-data').onclick = () => {
                const text = $('textarea-manual-data').value;
                const rows = text.split('\\n').filter(r => r.trim());
                if (rows.length > 1) {
                    const headers = rows[0].split(',').map(h => h.trim());
                    const data = rows.slice(1).map((r, i) => {
                        const vals = r.split(',');
                        let obj = { _id: `man-${i}` };
                        headers.forEach((h, j) => obj[h] = vals[j] ? vals[j].trim() : '');
                        return obj;
                    });
                    applyData(headers, data);
                    $('data-import-alert').className = 'p-3 rounded-xl text-xs font-bold bg-emerald-50 border border-emerald-300 text-emerald-800';
                    $('data-import-alert').textContent = `Berhasil memuat ${data.length} entri Manual!`;
                    $('data-import-alert').classList.remove('hidden');
                }
            };

            $('btn-fetch-gsheet').onclick = async () => {
                const url = $('input-gsheet-url').value.trim();
                if (!url) {
                    alert('Harap masukkan URL Google Spreadsheet terlebih dahulu.');
                    return;
                }

                // Ekstrak Spreadsheet ID dari URL Google Sheets
                const matches = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
                if (!matches || !matches[1]) {
                    alert('Format URL Google Spreadsheet tidak valid.');
                    return;
                }

                const sheetId = matches[1];
                // URL endpoint publik gviz untuk mengunduh CSV tanpa OAuth / API Key
                const fetchUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?tqx=out:csv`;

                try {
                    $('btn-fetch-gsheet').textContent = 'Memuat...';
                    $('btn-fetch-gsheet').disabled = true;

                    const response = await fetch(fetchUrl);
                    if (!response.ok) {
                        throw new Error('Gagal mengakses Google Spreadsheet. Pastikan akses file sudah diubah menjadi "Siapa saja yang memiliki link" (Anyone with the link).');
                    }

                    const csvText = await response.text();
                    
                    // Parse data CSV menggunakan library SheetJS (XLSX) yang sudah terpasang
                    const workbook = XLSX.read(csvText, { type: 'string' });
                    const sheetName = workbook.SheetNames[0];
                    const json = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);

                    if (json.length > 0) {
                        applyData(Object.keys(json[0]), json.map((r, i) => ({ _id: `gsheet-${i}`, ...r })));
                        
                        $('data-import-alert').className = 'p-3 rounded-xl text-xs font-bold bg-emerald-50 border border-emerald-300 text-emerald-800';
                        $('data-import-alert').textContent = `Berhasil menarik ${json.length.toLocaleString('id-ID')} entri dari Google Spreadsheet!`;
                        $('data-import-alert').classList.remove('hidden');
                    } else {
                        alert('Data di dalam Google Spreadsheet kosong.');
                    }
                } catch (err) {
                    alert(err.message || 'Terjadi kesalahan saat menarik data dari Google Spreadsheet.');
                } finally {
                    $('btn-fetch-gsheet').textContent = 'Tarik Data';
                    $('btn-fetch-gsheet').disabled = false;
                }
            };
            
            $('checkbox-use-filtering').onchange = e => {
                state.settings.useFiltering = e.target.checked;
                $('filter-rules-container').classList.toggle('hidden', !e.target.checked);
                updateUI();
            };

            $('btn-add-filter-rule').onclick = () => {
                const col = $('select-filter-column').value;
                const op = $('select-filter-operator').value;
                const val = $('input-filter-value').value.trim();

                if (!val) {
                    alert('Harap isi nilai filter terlebih dahulu.');
                    return;
                }

                state.settings.filterRules.push({
                    id: `filter-${Date.now()}`,
                    column: col,
                    operator: op,
                    value: val
                });

                $('input-filter-value').value = '';
                updateUI();
            };
        }

        function switchTab(tab) {
            state.activeTab = tab;
            $('section-stage').classList.toggle('hidden', tab !== 'stage');
            $('section-config').classList.toggle('hidden', tab !== 'config');
            $('section-data').classList.toggle('hidden', tab !== 'data');

            $('tab-btn-stage').className = `nav-tab flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${tab === 'stage' ? 'bg-red-600 text-white shadow-2xs' : 'text-slate-600 hover:bg-slate-200/60 hover:text-slate-900'}`;
            $('tab-btn-config').className = `nav-tab flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${tab === 'config' ? 'bg-red-600 text-white shadow-2xs' : 'text-slate-600 hover:bg-slate-200/60 hover:text-slate-900'}`;
            $('tab-btn-data').className = `nav-tab flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${tab === 'data' ? 'bg-red-600 text-white shadow-2xs' : 'text-slate-600 hover:bg-slate-200/60 hover:text-slate-900'}`;
        }

        document.addEventListener('DOMContentLoaded', init);
        
        // Fungsi untuk sinkronisasi tinggi iframe ke Streamlit secara nyata
        function updateStreamlitFrameHeight() {
            setTimeout(() => {
                const bodyHeight = document.body.scrollHeight;
                const viewportHeight = window.innerHeight;
                // Ambil nilai tertinggi antara isi konten dan tinggi viewport browser
                const targetHeight = Math.max(bodyHeight, viewportHeight);
                
                window.parent.postMessage({
                    type: 'streamlit:setFrameHeight',
                    height: targetHeight
                }, '*');
            }, 100);
        }

        // Jalankan pemantauan resize
        window.addEventListener('resize', updateStreamlitFrameHeight);
        window.addEventListener('load', updateStreamlitFrameHeight);
        
    </script>
</body>

</html>
"""

# Gabungkan (chaining) proses replacement string
ALFAMIDI_HTML_FINAL = ALFAMIDI_HTML.replace("%%LOGO_B64%%", logo_b64).replace("%%LOGO_PANJANG%%", logo_panjang_b64).replace("%%BG_B64%%", bg_b64)

# Render aplikasi langsung di Streamlit
components.html(ALFAMIDI_HTML_FINAL, height=1250, scrolling=True)
