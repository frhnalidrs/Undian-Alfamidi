"""
Alfamidi Lucky Draw - Sistem Undian Karyawan PT Midi Utama Indonesia Tbk
Aplikasi Undian Doorprize Berkapasitas Puluhan Ribu Peserta
Tampilan Arcade Slot Machine 100% Identik dengan Desain Google AI Studio

Cara Menjalankan:
1. pip install -r requirements.txt
2. streamlit run streamlit.py
"""

import streamlit as st
import streamlit.components.v1 as components
import json

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Alfamidi Lucky Draw - Undian Doorprize Karyawan",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Hilangkan padding default Streamlit agar tampilan pas dan immersive
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.25rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Full Self-Contained HTML, CSS & JavaScript Matching AI Studio Pixel-for-Pixel
ALFAMIDI_HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Alfamidi Lucky Draw</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,900;1,600;1,700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- SheetJS (Excel), jsPDF, AutoTable, and Canvas Confetti -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.4/dist/confetti.browser.min.js"></script>

  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #020617;
      color: #f8fafc;
      overflow-x: hidden;
    }
    .airmail-border {
      background: repeating-linear-gradient(
        135deg,
        #d71920 0,
        #d71920 18px,
        transparent 18px,
        transparent 24px,
        #1e40af 24px,
        #1e40af 42px,
        transparent 42px,
        transparent 48px
      );
    }
    .stamp-border {
      clip-path: polygon(
        0% 4%, 4% 0%, 8% 4%, 12% 0%, 16% 4%, 20% 0%, 24% 4%, 28% 0%, 32% 4%, 36% 0%, 
        40% 4%, 44% 0%, 48% 4%, 52% 0%, 56% 4%, 60% 0%, 64% 4%, 68% 0%, 72% 4%, 76% 0%, 
        80% 4%, 84% 0%, 88% 4%, 92% 0%, 96% 4%, 100% 0%, 100% 100%, 0% 100%
      );
    }
    .arcade-red-button {
      background: linear-gradient(180deg, #ef4444 0%, #dc2626 50%, #991b1b 100%);
      box-shadow: 0 8px 0 #7f1d1d, 0 14px 25px rgba(220, 38, 38, 0.6);
      transition: all 0.1s ease;
    }
    .arcade-red-button:hover {
      background: linear-gradient(180deg, #f87171 0%, #ef4444 50%, #b91c1c 100%);
      box-shadow: 0 10px 0 #7f1d1d, 0 18px 30px rgba(239, 68, 68, 0.8);
      transform: translateY(-2px);
    }
    .arcade-red-button:active, .arcade-red-button.is-pressed {
      transform: translateY(6px);
      box-shadow: 0 2px 0 #7f1d1d, 0 6px 12px rgba(220, 38, 38, 0.4);
    }
  </style>
</head>
<body class="min-h-screen antialiased flex flex-col pb-10">

  <!-- TOP HEADER -->
  <header class="sticky top-0 z-40 bg-slate-900/95 backdrop-blur-md border-b border-red-600/40 px-3 sm:px-6 py-2.5">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      <!-- Logo & Corporate Title -->
      <div class="flex items-center gap-3">
        <div id="brand-logo-container" class="relative flex items-center justify-center flex-shrink-0">
          <img id="header-brand-logo" 
               src="/assets/alfamidi-logo.svg" 
               alt="Logo Alfamidi" 
               class="h-9 sm:h-10 w-auto max-w-[130px] object-contain transition-all" 
               onerror="this.classList.add('hidden'); document.getElementById('header-brand-badge').classList.remove('hidden');" />
          <div id="header-brand-badge" class="hidden w-9 h-9 sm:w-10 sm:h-10 bg-red-600 rounded-xl flex items-center justify-center text-white font-black text-xl shadow-lg border border-red-400 flex-shrink-0" title="Badge Pengganti (Logo Error)">
            A
          </div>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-extrabold text-white text-sm sm:text-base tracking-tight uppercase">
              Alfamidi
            </span>
            <span class="text-[10px] text-amber-400 font-bold bg-amber-400/10 px-1.5 py-0.5 rounded border border-amber-400/20">
              LUCKY DRAW
            </span>
          </div>
          <p class="text-[10px] sm:text-xs text-slate-400 truncate max-w-[180px] sm:max-w-none">
            PT MIDI UTAMA INDONESIA TBK • Sistem Undian Karyawan
          </p>
        </div>
      </div>

      <!-- Navigation Pill Tabs -->
      <nav class="flex items-center gap-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800" role="tablist">
        <button id="tab-btn-stage" class="nav-tab active flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer bg-red-600 text-white shadow-sm">
          <span>✨</span>
          <span class="hidden sm:inline">Panggung Undian</span>
          <span class="sm:hidden">Undian</span>
        </button>
        <button id="tab-btn-config" class="nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer text-slate-400 hover:text-white hover:bg-slate-800">
          <span>⚙️</span>
          <span class="hidden sm:inline">Pengaturan Undian</span>
          <span class="sm:hidden">Setting</span>
        </button>
        <button id="tab-btn-data" class="nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer text-slate-400 hover:text-white hover:bg-slate-800">
          <span>📁</span>
          <span class="hidden sm:inline">Data Peserta</span>
          <span class="sm:hidden">Data</span>
        </button>
      </nav>

      <!-- Right Header Tools -->
      <div class="flex items-center gap-2">
        <button id="btn-view-last-modal" class="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-bold transition-all cursor-pointer shadow-xs" title="Buka kembali modal hasil undian terakhir">
          <span>👁️</span>
          <span>Modal Terakhir</span>
        </button>

        <button id="btn-open-history" class="relative p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors cursor-pointer flex items-center gap-1 text-xs font-medium" title="Lihat Riwayat Putaran Undian">
          <span class="text-amber-400">🕒</span>
          <span class="hidden md:inline">Riwayat</span>
          <span id="history-badge-count" class="w-5 h-5 rounded-full bg-red-600 text-white text-[10px] font-black hidden items-center justify-center">0</span>
        </button>

        <!-- Top Right Alfamidi Logo with Fallback Badge -->
        <div id="top-right-logo-container" class="flex items-center pl-1 sm:pl-2 border-l border-slate-800" title="Logo Alfamidi (Bisa diubah di Pengaturan)">
          <img id="top-right-logo-img" 
               src="/assets/alfamidi-logo.svg" 
               alt="Logo Alfamidi" 
               class="h-8 sm:h-9 w-auto max-w-[120px] object-contain rounded-lg transition-transform hover:scale-105 cursor-pointer shadow-xs"
               onerror="this.classList.add('hidden'); document.getElementById('top-right-logo-badge').classList.remove('hidden');" />
          <div id="top-right-logo-badge" class="hidden h-8 sm:h-9 px-2.5 bg-red-600 rounded-xl flex items-center justify-center text-white font-black text-xs shadow-md border border-red-400 flex-shrink-0 gap-1.5 cursor-pointer" title="Badge Pengganti (Logo Error/Tidak Dapat Diakses)">
            <span class="w-4 h-4 rounded bg-white text-red-600 flex items-center justify-center text-[10px] font-black">A</span>
            <span class="text-[10px] font-extrabold tracking-wider text-white hidden sm:inline">ALFAMIDI</span>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN APP CONTAINER -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 pt-4">

    <!-- QUICK INFO STRIP -->
    <div class="mb-4 flex flex-wrap items-center justify-between gap-3 p-3 bg-slate-900/60 rounded-xl border border-slate-800/80 text-xs">
      <div class="flex items-center gap-3 flex-wrap">
        <div class="flex items-center gap-1.5 text-slate-300">
          <span class="text-amber-400 text-sm">🎁</span>
          <span>Hadiah Aktif: <strong id="info-active-group" class="text-white">Grand Prize - Sepeda Motor Honda Beat</strong></span>
        </div>
        <span class="text-slate-600 hidden sm:inline">•</span>
        <div class="text-slate-300">
          Jumlah: <strong id="info-winner-count" class="text-amber-400 font-mono">1 Pemenang</strong>
        </div>
        <span class="text-slate-600 hidden sm:inline">•</span>
        <div class="text-slate-300">
          Format: <span id="info-format-preview" class="font-mono text-amber-300">[NAMA_KARYAWAN - NIK - JABATAN]</span>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <span class="text-slate-400">Peserta Memenuhi Syarat:</span>
        <span id="info-candidate-stats" class="px-2 py-0.5 rounded bg-red-600/20 text-red-400 border border-red-500/30 font-bold font-mono">
          1.000 / 1.000
        </span>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- SECTION 1: PANGGUNG UNDIAN (SLOT MACHINE ARENA) -->
    <!-- ============================================================== -->
    <section id="section-stage" class="space-y-4">
      <div class="relative w-full max-w-4xl mx-auto flex items-center justify-center py-2 px-2 sm:px-6">
        <div class="absolute inset-0 bg-radial from-red-600/20 via-amber-500/10 to-transparent blur-2xl pointer-events-none"></div>

        <!-- Main Slot Machine Chassis -->
        <div class="relative w-full bg-gradient-to-b from-red-800 via-red-900 to-red-950 p-4 sm:p-7 rounded-3xl border-4 border-amber-400 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.9)] flex flex-col items-center">
          
          <!-- Flashing Arcade Bulbs Top Bar -->
          <div class="w-full flex items-center justify-between px-3 py-1 mb-3 bg-red-950/70 rounded-full border border-amber-500/40">
            <div id="arcade-bulbs-left" class="flex items-center gap-1.5 sm:gap-2">
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-amber-400"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-amber-400"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-amber-400"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
            </div>

            <!-- Mute / Unmute Button -->
            <button id="btn-toggle-sound" class="flex items-center gap-1 text-[11px] font-semibold text-amber-300 hover:text-white bg-red-900/60 px-2.5 py-1 rounded-full border border-amber-400/30 transition-colors cursor-pointer" title="Nyalakan/Matikan Suara">
              <span>🔊</span>
              <span id="sound-status-text" class="hidden sm:inline">Suara ON</span>
            </button>

            <div id="arcade-bulbs-right" class="flex items-center gap-1.5 sm:gap-2">
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-amber-400"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-amber-400"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500"></span>
              <span class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-amber-400"></span>
            </div>
          </div>

          <!-- Marquee Banner Header -->
          <div class="w-full text-center py-2 px-4 mb-3 rounded-xl bg-gradient-to-r from-amber-600 via-amber-400 to-amber-600 text-slate-950 font-black shadow-lg border-2 border-amber-200">
            <div class="flex items-center justify-center gap-2">
              <span class="text-red-700 animate-spin text-sm">✦</span>
              <h2 id="marquee-event-title" class="text-base sm:text-xl md:text-2xl font-black tracking-wider uppercase font-serif drop-shadow-xs">
                SISTEM PENGUNDIAN KARYAWAN
              </h2>
              <span class="text-red-700 animate-spin text-sm">✦</span>
            </div>
          </div>

          <!-- KATEGORI HADIAH & JUMLAH PEMENANG CONTAINER -->
          <div class="w-full mb-4 p-3 sm:p-4 bg-red-950/85 rounded-2xl border border-amber-400/40 shadow-inner space-y-2.5">
            <!-- Baris 1: Kategori Hadiah Dropdown -->
            <div class="flex flex-col sm:flex-row sm:items-center gap-2">
              <div class="flex items-center gap-2 flex-shrink-0">
                <span class="text-amber-400">🎁</span>
                <label for="stage-category-select" class="text-xs font-bold text-amber-300 uppercase tracking-wider">
                  Kategori Hadiah:
                </label>
              </div>
              <select id="stage-category-select" class="flex-1 w-full bg-slate-900 border border-amber-400/60 rounded-xl px-3 py-2 text-xs sm:text-sm font-bold text-white focus:outline-none focus:border-amber-300 cursor-pointer shadow-inner truncate">
              </select>
            </div>

            <!-- Baris 2: Jumlah Pemenang (Dengan ikon 3 orang / Users) -->
            <div class="pt-2 border-t border-red-900/60 flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="text-amber-300">👥</span>
                <span class="text-xs font-bold text-amber-200 uppercase tracking-wider">
                  Jumlah Pemenang:
                </span>
              </div>

              <div class="flex items-center gap-2 flex-wrap">
                <!-- Quick Count Chips -->
                <div class="flex items-center gap-1">
                  <button type="button" class="btn-quick-count px-2 py-0.5 text-xs font-bold rounded-lg transition-colors cursor-pointer bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white" data-count="1">1</button>
                  <button type="button" class="btn-quick-count px-2 py-0.5 text-xs font-bold rounded-lg transition-colors cursor-pointer bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white" data-count="3">3</button>
                  <button type="button" class="btn-quick-count px-2 py-0.5 text-xs font-bold rounded-lg transition-colors cursor-pointer bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white" data-count="5">5</button>
                  <button type="button" class="btn-quick-count px-2 py-0.5 text-xs font-bold rounded-lg transition-colors cursor-pointer bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white" data-count="10">10</button>
                  <button type="button" class="btn-quick-count px-2 py-0.5 text-xs font-bold rounded-lg transition-colors cursor-pointer bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white" data-count="20">20</button>
                </div>

                <!-- Number Input Box -->
                <div class="flex items-center gap-1 bg-slate-900 px-2 py-1 rounded-lg border border-amber-400/50">
                  <input id="stage-winner-count-input" type="number" min="1" value="1" class="w-12 sm:w-16 bg-transparent text-xs sm:text-sm text-amber-300 font-mono font-black text-center focus:outline-none" />
                  <span class="text-[11px] text-slate-400 font-semibold">Orang</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Slot Reels Container & Arcade Big Red Button Row -->
          <div class="w-full flex flex-col md:flex-row items-center justify-between gap-4 sm:gap-6">
            <!-- Glass Reels Box -->
            <div class="flex-1 w-full bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 p-3 sm:p-5 rounded-2xl border-4 border-amber-500/80 shadow-[inset_0_10px_25px_rgba(0,0,0,0.8)] relative overflow-hidden">
              <div class="absolute top-0 inset-x-0 h-1/3 bg-gradient-to-b from-white/15 to-transparent pointer-events-none rounded-t-xl"></div>
              
              <div class="absolute inset-y-0 left-0 right-0 my-auto h-20 sm:h-24 border-y-2 border-amber-400/40 bg-amber-400/5 pointer-events-none z-10 flex items-center justify-between px-1">
                <span class="text-amber-400 text-xs font-black">▶</span>
                <span class="text-amber-400 text-xs font-black">◀</span>
              </div>

              <!-- Reels Grid -->
              <div id="slot-reels-grid" class="grid gap-3 sm:gap-4 relative z-0 grid-cols-1">
              </div>
            </div>

            <!-- ARCADE BIG RED BUTTON (Pusat Kendali Putaran) -->
            <div class="flex flex-col items-center justify-center flex-shrink-0 select-none py-1">
              <div class="relative group">
                <!-- Outer Golden Arcade Bezel Ring -->
                <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-full p-2 bg-gradient-to-b from-amber-300 via-amber-500 to-amber-700 shadow-[0_12px_28px_rgba(0,0,0,0.8),inset_0_2px_4px_rgba(255,255,255,0.6)] flex items-center justify-center">
                  <!-- Inner Metallic Bezel Ring -->
                  <div class="w-full h-full rounded-full p-2 bg-gradient-to-b from-slate-800 via-slate-900 to-black shadow-inner flex items-center justify-center">
                    <!-- Big 3D Red Push Button -->
                    <button id="btn-arcade-red-button" type="button" class="w-full h-full rounded-full cursor-pointer transition-all duration-150 flex flex-col items-center justify-center text-center relative overflow-hidden outline-none arcade-red-button" title="Tekan Tombol Merah untuk Mengundi!">
                      <div class="absolute top-1 inset-x-3 h-1/3 bg-gradient-to-b from-white/50 to-transparent rounded-full pointer-events-none"></div>
                      <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white drop-shadow-md mb-0.5 fill-white" viewBox="0 0 24 24">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                      </svg>
                      <span id="btn-arcade-red-text" class="text-[11px] sm:text-xs font-black tracking-wider uppercase text-white drop-shadow-md font-mono leading-none">
                        TEKAN
                      </span>
                      <span class="text-[9px] font-bold text-amber-200 tracking-widest uppercase leading-none mt-0.5">
                        UNDI
                      </span>
                    </button>
                  </div>
                </div>
                <div id="arcade-button-glow" class="absolute inset-0 rounded-full border-2 border-red-500/40 animate-ping pointer-events-none"></div>
              </div>
              <span class="text-[11px] font-black text-amber-300 uppercase tracking-widest mt-2">
                TOMBOL UNDI
              </span>
            </div>
          </div>

          <!-- Bottom Control Bar -->
          <div class="w-full mt-4 flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-red-700/60">
            <div class="flex items-center gap-2 text-xs text-red-200">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Total Kandidat: <strong id="bottom-total-candidates" class="text-white font-mono">1.000</strong> peserta</span>
            </div>

            <div class="flex items-center gap-2.5 flex-wrap">
              <!-- Re-open Last Modal Button -->
              <button id="btn-bottom-last-modal" class="hidden px-3 py-2 bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white text-xs font-bold rounded-xl border border-amber-400/40 flex items-center gap-1.5 transition-all cursor-pointer shadow-md hover:scale-105" title="Buka kembali modal hasil undian terakhir">
                <span>👁️</span>
                <span id="btn-bottom-last-modal-text">Lihat Modal Terakhir</span>
              </button>

              <!-- Undi Ulang Button -->
              <button id="btn-reset-draw" class="hidden px-3 py-2 bg-red-950/80 hover:bg-red-900 text-amber-300 text-xs font-semibold rounded-xl border border-amber-400/40 flex items-center gap-1.5 transition-colors cursor-pointer">
                <span>🔄</span>
                <span>Undi Ulang</span>
              </button>

              <!-- Big Action Spin Button -->
              <button id="btn-main-spin" class="px-6 sm:px-9 py-2.5 sm:py-3 rounded-xl font-black text-xs sm:text-sm uppercase tracking-wider transition-all duration-200 cursor-pointer shadow-xl bg-gradient-to-r from-red-600 via-red-500 to-amber-500 hover:from-red-500 hover:to-amber-400 text-white border-2 border-amber-300 hover:scale-105 active:scale-95 shadow-[0_0_25px_rgba(239,68,68,0.6)]">
                PUTAR UNDIAN SEKARANG
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 2: PENGATURAN PARAMETER UNDIAN (CONFIG) -->
    <!-- ============================================================== -->
    <section id="section-config" class="hidden max-w-4xl mx-auto space-y-5">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 shadow-xl space-y-6">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <h2 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <span>⚙️</span> Pengaturan Parameter Undian
          </h2>
          <span class="text-xs text-slate-400">
            Tersedia: <strong id="config-available-count" class="text-white">1.000</strong> peserta
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6">
          <div class="space-y-4">
            <div>
              <label for="input-event-title" class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
                Judul Acara / Header Undian
              </label>
              <input id="input-event-title" type="text" value="SISTEM PENGUNDIAN KARYAWAN" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:border-red-500 font-semibold" />
            </div>

            <!-- Bulk Kategori Hadiah -->
            <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
              <div class="flex items-center justify-between">
                <label for="textarea-bulk-categories" class="text-xs font-bold text-amber-300 uppercase tracking-wider">
                  Daftar Kategori / Grup Hadiah (Bulk)
                </label>
                <span id="config-categories-count" class="text-[10px] text-slate-400 font-mono">5 Kategori Aktif</span>
              </div>
              <p class="text-[11px] text-slate-400">
                Format: <span class="text-amber-300">Nama Hadiah | Jumlah Pemenang</span> (1 baris per kategori).
              </p>
              <textarea id="textarea-bulk-categories" rows="5" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 font-mono text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-red-500"></textarea>
              <div class="flex items-center justify-between pt-1">
                <span class="text-[10px] text-slate-400 italic">* Pilih kategori di panggung undian</span>
                <button id="btn-apply-bulk-categories" type="button" class="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-600 text-slate-950 text-xs font-bold rounded-lg transition-colors cursor-pointer shadow-sm">
                  Terapkan Kategori
                </button>
              </div>
              <div id="config-categories-chips" class="pt-2 border-t border-slate-800 space-y-1.5 max-h-36 overflow-y-auto pr-1"></div>
            </div>

            <div>
              <label for="select-name-column" class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
                Kolom Utama / Nama yang Diundi
              </label>
              <select id="select-name-column" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:border-red-500 cursor-pointer"></select>
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label for="input-default-winner-count" class="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  Jumlah Pemenang Default
                </label>
                <span id="label-default-winner-count" class="text-xs font-mono font-bold text-amber-400">1 Orang</span>
              </div>
              <div class="flex items-center gap-2 mb-2.5">
                <input id="input-default-winner-count" type="number" min="1" value="1" class="w-24 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono text-center focus:outline-none focus:border-red-500" />
                <div class="flex flex-wrap gap-1">
                  <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700" data-count="1">1</button>
                  <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700" data-count="3">3</button>
                  <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700" data-count="5">5</button>
                  <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700" data-count="10">10</button>
                  <button type="button" class="btn-config-quick-count px-2.5 py-1.5 text-xs font-bold rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700" data-count="20">20</button>
                </div>
              </div>
              <div id="animation-notice-badge" class="p-2.5 rounded-xl border flex items-center gap-2 text-xs font-bold text-amber-400 bg-amber-950/60 border-amber-500/40">
                <span id="animation-notice-text">🎰 Slot Machine</span>
              </div>
            </div>

            <!-- Weighted probability -->
            <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800">
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-white uppercase tracking-wider">Bobot Persentase Kemenangan</span>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input id="checkbox-use-weighting" type="checkbox" class="sr-only peer" />
                  <div class="w-9 h-5 bg-slate-700 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-amber-500"></div>
                </label>
              </div>
              <div id="weight-column-container" class="hidden space-y-2 pt-2 border-t border-slate-800">
                <select id="select-weight-column" class="w-full bg-slate-900 border border-amber-500/50 rounded-xl px-3 py-2 text-xs text-white focus:outline-none cursor-pointer"></select>
              </div>
            </div>

            <!-- Kolom Tampilan -->
            <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
              <span class="text-xs font-bold text-white uppercase tracking-wider block">Kolom Ditampilkan Selain Nama</span>
              <div id="config-display-checkboxes-grid" class="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto pr-1"></div>
              <div id="config-format-sample-box" class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 font-mono text-xs text-amber-300 font-bold truncate"></div>
            </div>

            <!-- Duplicate lock -->
            <div class="flex items-center justify-between p-3 rounded-xl bg-slate-950/50 border border-slate-800">
              <span class="text-xs font-bold text-white">Kunci Pemenang (Cegah Menang 2x)</span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input id="checkbox-prevent-duplicate" type="checkbox" checked class="sr-only peer" />
                <div class="w-9 h-5 bg-slate-700 rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-emerald-600"></div>
              </label>
            </div>
          </div>
        </div>

        <!-- Logo Perusahaan / Alfamidi Settings -->
        <div class="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
              <span>🖼️</span> Logo Perusahaan (Pojok Atas)
            </span>
            <span class="text-[10px] text-slate-400">Badge "A" aktif otomatis jika logo error / tidak dapat diakses</span>
          </div>
          <div class="flex flex-col sm:flex-row items-center gap-4">
            <div class="w-32 h-14 rounded-xl bg-slate-900 border border-slate-700 p-2 flex items-center justify-center flex-shrink-0 overflow-hidden shadow-inner">
              <img id="config-logo-preview" src="/assets/alfamidi-logo.svg" alt="Preview Logo" class="max-h-full max-w-full object-contain" />
            </div>
            <div class="flex-1 w-full space-y-2">
              <input id="input-logo-url" type="text" placeholder="URL Gambar Logo (atau unggah berkas)" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-red-500 font-mono" />
              <div class="flex flex-wrap items-center gap-2">
                <label class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg cursor-pointer transition-colors border border-slate-700 flex items-center gap-1">
                  <span>📁 Unggah File Logo</span>
                  <input id="input-logo-file" type="file" accept="image/*" class="hidden" />
                </label>
                <button type="button" id="btn-reset-logo-default" class="px-3 py-1.5 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-xs font-semibold rounded-lg border border-amber-500/40 transition-colors cursor-pointer">
                  Gunakan Logo Alfamidi
                </button>
                <button type="button" id="btn-test-logo-error" class="px-3 py-1.5 bg-red-950/80 hover:bg-red-900 text-red-300 text-xs font-semibold rounded-lg border border-red-500/40 transition-colors cursor-pointer" title="Simulasi link logo error / tidak dapat diakses">
                  Uji Badge Fallback
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end pt-3 border-t border-slate-800">
          <button id="btn-save-to-stage" type="button" class="px-6 py-2.5 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white font-bold text-xs rounded-xl shadow-lg transition-transform hover:scale-105 active:scale-95 cursor-pointer">
            <span id="btn-save-to-stage-text">Simpan & Menuju Panggung Undian</span>
          </button>
        </div>
      </div>
    </section>

    <!-- ============================================================== -->
    <!-- SECTION 3: SUMBER DATA PESERTA -->
    <!-- ============================================================== -->
    <section id="section-data" class="hidden max-w-4xl mx-auto space-y-5">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 shadow-xl">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-5 border-b border-slate-800 pb-4">
          <h2 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <span>📁</span> Sumber Data Peserta Undian
          </h2>
          <div class="px-3 py-1.5 rounded-lg bg-emerald-950/60 border border-emerald-600/40 text-emerald-400 text-xs font-semibold">
            <span id="data-active-counter-text">1.000 Peserta Aktif</span>
          </div>
        </div>

        <div class="flex flex-wrap gap-1.5 p-1 bg-slate-950/80 rounded-xl mb-5 border border-slate-800">
          <button class="subtab-btn active px-3.5 py-2 rounded-lg text-xs font-semibold bg-red-600 text-white" data-target="panel-sample">Sampel Alfamidi</button>
          <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-400" data-target="panel-excel">Upload Excel (.xlsx)</button>
          <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-400" data-target="panel-csv">Upload CSV</button>
          <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-400" data-target="panel-gsheet">Google Spreadsheet</button>
          <button class="subtab-btn px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-400" data-target="panel-manual">Ketik Manual</button>
        </div>

        <div class="space-y-4">
          <div id="panel-sample" class="data-subpanel bg-slate-950/60 p-4 sm:p-5 rounded-xl border border-slate-800/80">
            <p class="text-xs text-slate-400 mb-4">Gunakan data simulasi resmi lengkap dengan NIK, Nama Karyawan, Jabatan, Cabang se-Indonesia, dan Poin Kinerja.</p>
            <div class="flex flex-wrap gap-3">
              <button type="button" id="btn-load-sample-1k" class="px-4 py-2.5 bg-gradient-to-r from-red-600 to-red-700 text-white text-xs font-bold rounded-xl cursor-pointer">Muat 1.000 Karyawan</button>
              <button type="button" id="btn-load-sample-10k" class="px-4 py-2.5 bg-slate-800 text-amber-300 border border-amber-500/30 text-xs font-bold rounded-xl cursor-pointer">Muat 10.000 Karyawan</button>
              <button type="button" id="btn-load-sample-25k" class="px-4 py-2.5 bg-slate-800 text-emerald-400 border border-emerald-500/30 text-xs font-bold rounded-xl cursor-pointer">Muat 25.000 Karyawan</button>
            </div>
          </div>

          <div id="panel-excel" class="data-subpanel hidden border-2 border-dashed border-slate-700 rounded-xl p-6 text-center bg-slate-950/40">
            <p class="text-sm font-bold text-white mb-2">Pilih File Excel (.xlsx, .xls)</p>
            <label class="inline-block px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl cursor-pointer">
              Pilih Berkas Excel
              <input id="input-file-excel" type="file" accept=".xlsx, .xls" class="hidden" />
            </label>
          </div>

          <div id="panel-csv" class="data-subpanel hidden border-2 border-dashed border-slate-700 rounded-xl p-6 text-center bg-slate-950/40">
            <p class="text-sm font-bold text-white mb-2">Pilih File CSV (.csv)</p>
            <label class="inline-block px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl cursor-pointer">
              Pilih Berkas CSV
              <input id="input-file-csv" type="file" accept=".csv, text/csv" class="hidden" />
            </label>
          </div>

          <div id="panel-gsheet" class="data-subpanel hidden bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 space-y-3">
            <div class="flex gap-2">
              <input id="input-gsheet-url" type="url" placeholder="https://docs.google.com/spreadsheets/d/.../edit" class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
              <button id="btn-fetch-gsheet" type="button" class="px-4 py-2 bg-red-600 text-white text-xs font-bold rounded-xl">Tarik Data</button>
            </div>
          </div>

          <div id="panel-manual" class="data-subpanel hidden bg-slate-950/60 p-4 sm:p-5 rounded-xl border border-slate-800/80 space-y-3">
            <div>
              <label for="textarea-manual-data" class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Ketik atau Tempel Data Manual
              </label>
              <p class="text-[11px] text-slate-400 mb-2">
                Format: koma (,) untuk memisahkan kolom, dan ENTER untuk baris baru. Baris 1 = Judul kolom.
              </p>
              <textarea id="textarea-manual-data" rows="6" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 font-mono text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-red-500">NIK,NAMA_KARYAWAN,JABATAN,CABANG,POIN_UNDIAN
MIDI-202401,Budi Santoso,Store Leader,Makassar,150
MIDI-202402,Siti Nurhaliza,Cashier Staff,Bekasi,90
MIDI-202403,Ahmad Pratama,Store Crew,Tangerang,120
MIDI-202404,Dewi Lestari,Assistant Store Leader,Medan,110
MIDI-202405,Eko Wijaya,Store Crew,Manado,85</textarea>
            </div>
            <div class="flex items-center justify-between gap-2 pt-1">
              <div id="manual-data-feedback" class="text-xs font-bold text-emerald-400 hidden flex items-center gap-1.5 bg-emerald-950/70 border border-emerald-600/50 px-3 py-1.5 rounded-lg">
                <span>✓</span>
                <span id="manual-data-feedback-text">Berhasil memuat 5 data manual!</span>
              </div>
              <button id="btn-apply-manual-data" type="button" class="ml-auto px-5 py-2.5 bg-red-600 hover:bg-red-700 active:scale-95 text-white text-xs font-bold rounded-xl transition-all cursor-pointer shadow-md flex items-center gap-1.5">
                <span id="btn-apply-manual-text">Terapkan Data Manual</span>
              </button>
            </div>
          </div>

          <div id="data-import-alert" class="hidden p-3 rounded-xl text-xs"></div>

          <div class="mt-4 pt-4 border-t border-slate-800">
            <span class="text-xs font-bold text-slate-300 block mb-2">Pratinjau Data (5 Baris Pertama):</span>
            <div class="overflow-x-auto rounded-lg border border-slate-800 bg-slate-950/80">
              <table class="w-full text-left text-xs">
                <thead id="data-preview-thead" class="bg-slate-800 text-slate-300"></thead>
                <tbody id="data-preview-tbody" class="divide-y divide-slate-800/60"></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ============================================================== -->
  <!-- MODAL 1: SURAT AMPLOP VINTAGE (4-10 PEMENANG) -->
  <!-- ============================================================== -->
  <div id="modal-envelope" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-slate-950/85 backdrop-blur-md">
    <div class="relative w-full max-w-3xl flex flex-col items-center my-auto">
      <button id="btn-close-envelope-modal" class="absolute -top-12 right-0 p-2 text-white bg-slate-900/80 rounded-full border border-white/20">✕</button>

      <div class="relative w-full flex flex-col items-center">
        <!-- Letter -->
        <div id="envelope-letter" class="w-full max-w-2xl bg-[#fffef9] text-slate-800 rounded-xl shadow-2xl border border-amber-200/80 p-5 sm:p-8 z-20">
          <div class="flex items-center justify-between border-b-2 border-red-600 pb-4 mb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white font-black text-xl shadow-md">A</div>
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
            <h2 id="letter-event-title" class="text-xl sm:text-2xl font-black text-red-700 uppercase font-serif">SISTEM PENGUNDIAN KARYAWAN</h2>
            <p id="letter-subtitle" class="text-xs text-slate-600 mt-1"></p>
          </div>

          <div id="envelope-winners-list" class="space-y-2.5 max-h-[42vh] overflow-y-auto pr-1"></div>

          <div class="mt-5 pt-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
            <span class="italic">Sah & Terverifikasi oleh Sistem Pengundian Alfamidi</span>
            <span id="letter-total-winners-count" class="font-mono text-[11px] text-slate-400"></span>
          </div>

          <div class="mt-5 flex items-center justify-end gap-2.5">
            <button id="btn-envelope-export-excel" class="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg shadow-sm">Unduh Excel</button>
            <button id="btn-envelope-export-pdf" class="px-3.5 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg shadow-sm">Cetak PDF</button>
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
                  <p class="text-[9px] sm:text-[11px] text-slate-600 font-serif mt-1">Alfa Tower Alam Sutera, Jl. Jalur Sutera Bar. No.Kav. 7-9, Kota Tangerang, Banten, 15143</p>
                </div>
                <div class="w-16 h-20 bg-[#a35e38] p-1.5 rounded-sm shadow-md stamp-border flex items-center justify-center">
                  <div class="w-full h-full bg-white flex flex-col items-center justify-center p-1">
                    <div class="w-8 h-8 bg-red-600 rounded-lg text-white font-black text-xl flex items-center justify-center">A</div>
                    <span class="text-[10px] font-black text-red-600 mt-1">Alfamidi</span>
                  </div>
                </div>
              </div>

              <div class="my-auto pl-4 py-2">
                <div class="text-xs font-serif font-black text-red-800">TO : THE WINNER OF</div>
                <div id="envelope-body-event-title" class="text-base sm:text-2xl font-serif font-black text-red-700 uppercase">SISTEM PENGUNDIAN KARYAWAN</div>
                <div id="envelope-body-subtitle" class="text-[10px] sm:text-xs font-semibold text-slate-600 uppercase mt-1">HADIAH UTAMA • PEMENANG RESMI</div>
              </div>

              <div class="flex justify-between text-[9px] text-slate-400 font-mono">
                <span>AIR MAIL / PAR AVION</span>
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
  <div id="modal-table" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/85 backdrop-blur-md">
    <div class="relative w-full max-w-5xl h-[92vh] flex flex-col bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden">
      <div class="bg-gradient-to-r from-red-700 via-red-600 to-red-800 p-4 text-white flex items-center justify-between">
        <div>
          <span id="table-modal-winner-count-badge" class="text-xs font-bold text-amber-300">0 PEMENANG</span>
          <h2 id="table-modal-event-title" class="text-lg font-black uppercase">SISTEM PENGUNDIAN KARYAWAN</h2>
          <p id="table-modal-category-name" class="text-xs text-red-100"></p>
        </div>
        <button id="btn-close-table-modal" class="p-2 text-white bg-white/10 rounded-full">✕</button>
      </div>

      <div class="p-3 bg-slate-800/80 border-b border-slate-700 flex items-center justify-between gap-3">
        <input id="input-search-table-modal" type="text" placeholder="Cari pemenang..." class="flex-1 max-w-md px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white" />
        <div class="flex gap-2">
          <button id="btn-table-copy-list" class="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white text-xs font-semibold rounded-lg">Salin Teks</button>
          <button id="btn-table-export-excel" class="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg">Unduh Excel</button>
          <button id="btn-table-export-pdf" class="px-3 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg">Cetak PDF</button>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto">
        <table class="w-full text-left text-sm">
          <thead id="table-modal-thead" class="sticky top-0 bg-slate-800 text-slate-300 text-xs uppercase"></thead>
          <tbody id="table-modal-tbody" class="divide-y divide-slate-800"></tbody>
        </table>
      </div>

      <div class="p-3 bg-slate-800 border-t border-slate-700 flex items-center justify-between text-xs text-slate-400">
        <div id="table-modal-pagination-info"></div>
        <div class="flex items-center gap-2">
          <button id="btn-table-prev-page" class="p-1.5 rounded bg-slate-700 text-white">◀</button>
          <span id="table-modal-page-num" class="text-white px-2"></span>
          <button id="btn-table-next-page" class="p-1.5 rounded bg-slate-700 text-white">▶</button>
          <button id="btn-table-bottom-close" class="ml-3 px-4 py-1.5 bg-slate-700 hover:bg-slate-600 text-white rounded-lg">Tutup</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- DRAWER: RIWAYAT UNDIAN -->
  <!-- ============================================================== -->
  <div id="drawer-history" class="hidden fixed inset-0 z-50 flex items-center justify-end bg-slate-950/70">
    <div class="w-full max-w-lg h-full bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col">
      <div class="p-4 border-b border-slate-800 flex items-center justify-between">
        <h3 class="font-bold text-white text-base">Riwayat Putaran Undian</h3>
        <button id="btn-close-history-drawer" class="p-1.5 text-slate-400 hover:text-white">✕</button>
      </div>
      <div id="drawer-history-list" class="flex-1 overflow-y-auto p-4 space-y-3"></div>
      <div class="p-3.5 border-t border-slate-800 bg-slate-950 flex justify-between">
        <button id="btn-history-reset-all" class="text-xs text-red-400 hover:text-red-300">Reset Riwayat</button>
        <button id="btn-history-bottom-close" class="px-4 py-1.5 bg-slate-800 text-white text-xs rounded-lg">Tutup</button>
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
      { id: 'cat-2', name: 'Hadiah Utama 1 - Smart TV 55 Inch & iPhone', winnerCount: 3 },
      { id: 'cat-3', name: 'Hadiah Utama 2 - Logam Mulia Emas 10 Gram', winnerCount: 5 },
      { id: 'cat-4', name: 'Hadiah Hiburan - Voucher Belanja Alfamidi Rp 1.000.000', winnerCount: 10 },
      { id: 'cat-5', name: 'Doorprize Akbar - Paket Elektronik Rumah Tangga', winnerCount: 20 },
    ];

    // State
    const state = {
      candidates: [],
      columns: [],
      settings: {
        nameColumn: 'NAMA_KARYAWAN',
        useWeighting: false,
        weightColumn: 'POIN_UNDIAN',
        winnerCount: 1,
        groupName: defaultCategories[0].name,
        displayColumns: ['NIK', 'JABATAN'],
        eventTitle: 'SISTEM PENGUNDIAN KARYAWAN',
        allowDuplicateWinners: false,
        categories: defaultCategories,
        logoUrl: '/assets/alfamidi-logo.svg',
      },
      wonIds: new Set(),
      drawHistory: [],
      recentWinners: null,
      lastDrawSession: null,
      isSpinning: false,
      activeTab: 'stage',
      tableSearchTerm: '',
      tableCurrentPage: 1,
      tablePageSize: 15,
      reelItems: [
        { name: 'SISTEM', extra: 'SIAP UNDI' },
        { name: 'UNDIAN', extra: 'SIAP UNDI' },
        { name: 'ALFAMIDI', extra: 'SIAP UNDI' },
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
      state.columns = headers.map(h => ({
        name: h,
        isNumeric: rows.slice(0, 50).every(r => typeof r[h] === 'number' || (!isNaN(Number(r[h])) && r[h] !== ''))
      }));
      const foundName = headers.find(h => /nama|name/i.test(h)) || headers[0];
      if (foundName) state.settings.nameColumn = foundName;
      const otherCols = headers.filter(h => h !== state.settings.nameColumn).slice(0, 2);
      if (otherCols.length > 0) state.settings.displayColumns = otherCols;
      updateUI();
    }

    // Weighted Draw Engine (A-Res)
    function executeDraw() {
      let pool = state.candidates;
      if (!state.settings.allowDuplicateWinners && state.wonIds.size > 0) {
        pool = pool.filter(c => !state.wonIds.has(c._id));
      }
      if (pool.length === 0) return [];
      const k = Math.min(state.settings.winnerCount, pool.length);

      let selected = [];
      if (state.settings.useWeighting && state.settings.weightColumn) {
        const wCol = state.settings.weightColumn;
        const scored = pool.map(c => {
          const w = Math.max(0.1, Number(c[wCol]) || 1);
          return { c, score: Math.pow(Math.random(), 1 / w), w };
        });
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
        const name = String(cand[state.settings.nameColumn] || 'Tanpa Nama');
        const extras = state.settings.displayColumns
          .filter(c => c !== state.settings.nameColumn && cand[c] !== undefined)
          .map(c => String(cand[c]));
        return {
          id: cand._id,
          rank: idx + 1,
          name,
          displayFormatted: [name, ...extras].join(' - '),
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
      $('info-format-preview').textContent = `[${[state.settings.nameColumn, ...state.settings.displayColumns.filter(c => c !== state.settings.nameColumn)].join(' - ')}]`;

      const available = state.settings.allowDuplicateWinners
        ? state.candidates.length
        : Math.max(0, state.candidates.length - state.wonIds.size);
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

      // Quick count chips active state
      document.querySelectorAll('.btn-quick-count').forEach(btn => {
        const cnt = Number(btn.getAttribute('data-count'));
        if (cnt === state.settings.winnerCount) {
          btn.className = 'btn-quick-count px-2 py-0.5 text-xs font-black rounded-lg bg-amber-400 text-slate-950 shadow-xs cursor-pointer';
        } else {
          btn.className = 'btn-quick-count px-2 py-0.5 text-xs font-bold rounded-lg bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white cursor-pointer';
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

    function renderReels() {
      const container = $('slot-reels-grid');
      const isSlotWinner = Boolean(state.recentWinners && state.recentWinners.length > 0 && state.recentWinners.length <= 3 && !state.isSpinning);
      const num = isSlotWinner ? state.recentWinners.length : 3;
      container.className = `grid gap-3 sm:gap-4 relative z-0 ${num === 1 ? 'grid-cols-1' : num === 2 ? 'grid-cols-2' : 'grid-cols-1 sm:grid-cols-3'}`;

      container.innerHTML = '';

      for (let i = 0; i < num; i++) {
        const item = state.reelItems[i] || { name: 'Alfamidi', extra: 'Siap Undi' };
        const winner = isSlotWinner && state.recentWinners ? state.recentWinners[i] : null;

        const el = document.createElement('div');
        el.className = `h-28 sm:h-36 rounded-xl border-2 flex flex-col items-center justify-center text-center p-2.5 transition-all relative overflow-hidden ${
          winner ? 'bg-gradient-to-b from-amber-100 via-white to-amber-50 border-amber-400 shadow-[0_0_20px_#f59e0b]' : 'bg-gradient-to-b from-slate-800 to-slate-900 border-slate-700 text-slate-100 shadow-inner'
        }`;
        el.innerHTML = `
          ${winner ? `<span class="absolute top-1.5 right-1.5 px-2 py-0.5 bg-red-600 text-white text-[10px] font-black rounded-full">Pemenang #${i+1}</span>` : ''}
          <div class="w-full my-auto">
            <p class="font-black text-sm sm:text-base md:text-lg tracking-tight uppercase line-clamp-2 px-1 ${winner ? 'text-red-700' : 'text-amber-300'}">
              ${winner ? winner.name : item.name}
            </p>
            <p class="text-[11px] sm:text-xs font-medium mt-1 line-clamp-2 px-1 ${winner ? 'text-slate-700 font-semibold' : 'text-slate-400'}">
              ${winner ? winner.displayFormatted : item.extra}
            </p>
          </div>
        `;
        container.appendChild(el);
      }

      if (isSlotWinner) $('btn-reset-draw').classList.remove('hidden');
      else $('btn-reset-draw').classList.add('hidden');
    }

    function renderConfig() {
      if (document.activeElement !== $('input-event-title')) {
        $('input-event-title').value = state.settings.eventTitle;
      }
      $('marquee-event-title').textContent = state.settings.eventTitle;
      $('envelope-body-event-title').textContent = state.settings.eventTitle;
      $('letter-event-title').textContent = state.settings.eventTitle;
      $('table-modal-event-title').textContent = state.settings.eventTitle;
      $('textarea-bulk-categories').value = state.settings.categories.map(c => `${c.name} | ${c.winnerCount}`).join('\\n');
      $('config-categories-count').textContent = `${state.settings.categories.length} Kategori Aktif`;

      $('config-categories-chips').innerHTML = state.settings.categories.map(c => `
        <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900 border border-slate-800 text-xs">
          <span class="font-semibold text-white truncate">${c.name} (${c.winnerCount} pemenang)</span>
          <button class="btn-del-cat text-slate-500 hover:text-red-400" data-id="${c.id}">✕</button>
        </div>
      `).join('');

      $('select-name-column').innerHTML = state.columns.map(c => `
        <option value="${c.name}" ${c.name === state.settings.nameColumn ? 'selected' : ''}>${c.name}</option>
      `).join('');

      $('input-default-winner-count').value = state.settings.winnerCount;
      $('label-default-winner-count').textContent = `${state.settings.winnerCount} Orang`;

      // Notice
      const n = state.settings.winnerCount;
      $('animation-notice-text').textContent = n <= 3 ? '🎰 Slot Machine' : n <= 10 ? '✉️ Animasi Surat' : '📊 Tabel Pemenang Komprehensif';

      $('select-weight-column').innerHTML = state.columns.map(c => `
        <option value="${c.name}" ${c.name === state.settings.weightColumn ? 'selected' : ''}>${c.name} ${c.isNumeric ? '⭐ (Angka)' : ''}</option>
      `).join('');

      $('config-display-checkboxes-grid').innerHTML = state.columns.map(c => `
        <button type="button" class="btn-toggle-col flex items-center gap-2 p-2 rounded-lg text-xs border ${
          state.settings.displayColumns.includes(c.name) ? 'bg-red-950/60 border-red-500/60 text-white font-semibold' : 'bg-slate-900 border-slate-800 text-slate-400'
        }" data-col="${c.name}">
          <span>${state.settings.displayColumns.includes(c.name) ? '☑' : '☐'}</span>
          <span class="truncate">${c.name}</span>
        </button>
      `).join('');

      $('config-format-sample-box').textContent = [state.settings.nameColumn, ...state.settings.displayColumns.filter(c => c !== state.settings.nameColumn)].join(' - ');
    }

    function renderDataPreview() {
      if (state.columns.length === 0) return;
      $('data-preview-thead').innerHTML = '<tr><th class="py-2 px-3">#</th>' + state.columns.map(c => `<th class="py-2 px-3">${c.name}</th>`).join('') + '</tr>';
      $('data-preview-tbody').innerHTML = state.candidates.slice(0, 5).map((row, idx) => `
        <tr><td class="py-2 px-3">${idx+1}</td>${state.columns.map(c => `<td class="py-2 px-3 text-slate-300">${row[c.name] ?? ''}</td>`).join('')}</tr>
      `).join('');
    }

    // Modal Envelope Open
    function openEnvelope(winners, group, title) {
      $('modal-envelope').classList.remove('hidden');
      $('letter-category-name').textContent = group;
      $('letter-event-title').textContent = title;
      $('envelope-body-event-title').textContent = title;
      $('envelope-body-subtitle').textContent = `${group} • ${winners.length} PEMENANG RESMI`;
      $('letter-subtitle').textContent = `Selamat kepada ${winners.length} rekan karyawan Alfamidi berikut:`;
      $('letter-total-winners-count').textContent = `TOTAL: ${winners.length} PEMENANG`;
      $('letter-current-date').textContent = new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });

      $('envelope-winners-list').innerHTML = winners.map((w, i) => `
        <div class="flex items-start gap-3 p-3 bg-red-50/70 rounded-lg border border-red-100">
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

      renderTableRows(winners);
      sound.playFanfare();
      confetti({ particleCount: 90, spread: 100, origin: { y: 0.4 } });
    }

    function renderTableRows(winners) {
      const term = state.tableSearchTerm.toLowerCase();
      const filtered = !term ? winners : winners.filter(w => w.name.toLowerCase().includes(term) || w.displayFormatted.toLowerCase().includes(term));
      const totalPages = Math.max(1, Math.ceil(filtered.length / state.tablePageSize));
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
        <tr class="hover:bg-slate-800">
          <td class="py-3 px-4 text-center font-bold text-amber-400">${start + idx + 1}</td>
          <td class="py-3 px-4 font-bold text-white">${w.name}</td>
          <td class="py-3 px-4 text-slate-200"><span class="px-2 py-1 rounded bg-slate-800 text-xs">${w.displayFormatted}</span></td>
          ${state.settings.displayColumns.map(c => `<td class="py-3 px-4 text-slate-300 text-xs">${w.data[c] ?? '-'}</td>`).join('')}
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

      const btnArcade = $('btn-arcade-red-button');
      btnArcade.classList.add('is-pressed');
      setTimeout(() => btnArcade.classList.remove('is-pressed'), 250);
      $('btn-main-spin').textContent = 'SEDANG MEMUTAR...';

      let count = 0;
      const interval = setInterval(() => {
        count++;
        if (count % 3 === 0) sound.playTick();
        state.reelItems = [1, 2, 3].map(() => {
          const c = state.candidates[Math.floor(Math.random() * state.candidates.length)];
          return { name: c.NAMA_KARYAWAN || 'Alfamidi', extra: c.JABATAN || 'Peserta' };
        });
        renderReels();
      }, 50);

      setTimeout(() => {
        clearInterval(interval);
        state.isSpinning = false;
        state.recentWinners = winners;
        state.lastDrawSession = { winners, groupName: state.settings.groupName, eventTitle: state.settings.eventTitle };
        $('btn-main-spin').textContent = 'PUTAR UNDIAN SEKARANG';

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
        state.recentWinners = null;
        state.reelItems = [
          { name: 'SISTEM', extra: 'SIAP UNDI' },
          { name: 'UNDIAN', extra: 'SIAP UNDI' },
          { name: 'ALFAMIDI', extra: 'SIAP UNDI' },
        ];
        renderReels();
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

      // Quick chips
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
      $('btn-close-table-modal').onclick = () => $('modal-table').classList.add('hidden');
      $('btn-table-bottom-close').onclick = () => $('modal-table').classList.add('hidden');

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
          <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
            <div class="flex justify-between items-center mb-1">
              <strong class="text-white">${h.groupName} (${h.winners.length} Pemenang)</strong>
              <button class="btn-prev-h text-amber-400" data-id="${h.id}">👁️ Buka</button>
            </div>
            <div class="text-slate-400 truncate">${h.winners.map(w => w.name).join(', ')}</div>
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
      // Event Title sync & persistence
      const updateTitle = val => {
        state.settings.eventTitle = val || 'SISTEM PENGUNDIAN KARYAWAN';
        $('marquee-event-title').textContent = state.settings.eventTitle;
        $('envelope-body-event-title').textContent = state.settings.eventTitle;
        $('letter-event-title').textContent = state.settings.eventTitle;
        $('table-modal-event-title').textContent = state.settings.eventTitle;
      };
      $('input-event-title').oninput = e => updateTitle(e.target.value);
      $('input-event-title').onchange = e => updateTitle(e.target.value);

      $('btn-save-to-stage').onclick = () => {
        const val = $('input-event-title').value.trim();
        updateTitle(val);
        const saveText = $('btn-save-to-stage-text');
        if (saveText) saveText.textContent = '✓ Pengaturan Tersimpan!';
        setTimeout(() => {
          if (saveText) saveText.textContent = 'Simpan & Menuju Panggung Undian';
          switchTab('stage');
        }, 350);
      };

      // Logo Handler
      function applyLogo(url) {
        const finalUrl = url ? url.trim() : '/assets/alfamidi-logo.svg';
        state.settings.logoUrl = finalUrl;

        const bind = (imgId, badgeId) => {
          const img = $(imgId);
          const badge = $(badgeId);
          if (!img || !badge) return;
          img.classList.remove('hidden');
          badge.classList.add('hidden');
          img.onerror = () => {
            img.classList.add('hidden');
            badge.classList.remove('hidden');
          };
          img.src = finalUrl;
        };

        bind('header-brand-logo', 'header-brand-badge');
        bind('top-right-logo-img', 'top-right-logo-badge');

        const preview = $('config-logo-preview');
        if (preview) {
          preview.onerror = () => { preview.src = ''; };
          preview.src = finalUrl;
        }

        const inputUrl = $('input-logo-url');
        if (inputUrl && inputUrl.value !== finalUrl) inputUrl.value = finalUrl;
      }

      applyLogo('/assets/alfamidi-logo.svg');

      $('input-logo-url').oninput = e => applyLogo(e.target.value);
      $('input-logo-file').onchange = e => {
        const file = e.target.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = ev => {
          const dataUrl = ev.target?.result;
          if (dataUrl) applyLogo(dataUrl);
        };
        reader.readAsDataURL(file);
      };
      $('btn-reset-logo-default').onclick = () => applyLogo('/assets/alfamidi-logo.svg');
      $('btn-test-logo-error').onclick = () => applyLogo('https://gambar-logo-tidak-ditemukan-404.test/error.png');
      $('top-right-logo-container').onclick = () => switchTab('config');

      // Manual Data Apply
      $('btn-apply-manual-data').onclick = () => {
        const btn = $('btn-apply-manual-data');
        btn.classList.add('scale-95');
        setTimeout(() => btn.classList.remove('scale-95'), 150);

        const txt = $('textarea-manual-data').value.trim();
        if (!txt) {
          alert('Silakan ketik atau tempel data terlebih dahulu.');
          return;
        }

        const lines = txt.split(/\r?\n/).filter(l => l.trim().length > 0);
        if (lines.length < 2) {
          alert('Data harus memiliki minimal 1 baris judul kolom dan 1 baris peserta.');
          return;
        }

        const headers = lines[0].split(',').map((h, i) => h.trim() || `Kolom_${i+1}`);
        const rows = [];
        for (let i = 1; i < lines.length; i++) {
          const vals = lines[i].split(',').map(v => v.trim());
          if (vals.every(v => v === '')) continue;
          const r = { _id: `manual-${i}` };
          headers.forEach((h, idx) => {
            const v = vals[idx] !== undefined ? vals[idx] : '';
            const num = Number(v);
            r[h] = (!isNaN(num) && v !== '') ? num : v;
          });
          rows.push(r);
        }

        state.wonIds.clear();
        state.recentWinners = null;
        applyData(headers, rows);

        const msg = `Berhasil memuat ${rows.length} data manual!`;
        const alertEl = $('data-import-alert');
        alertEl.className = 'p-3 rounded-xl text-xs bg-emerald-950 border border-emerald-700 text-emerald-200 font-semibold';
        alertEl.textContent = `✓ ${msg}`;
        alertEl.classList.remove('hidden');

        const feedback = $('manual-data-feedback');
        const feedbackText = $('manual-data-feedback-text');
        if (feedback && feedbackText) {
          feedbackText.textContent = msg;
          feedback.classList.remove('hidden');
        }

        const btnText = $('btn-apply-manual-text');
        if (btnText) btnText.textContent = `✓ Berhasil Memuat ${rows.length} Data!`;
        btn.classList.add('bg-emerald-600');
        setTimeout(() => {
          if (btnText) btnText.textContent = 'Terapkan Data Manual';
          btn.classList.remove('bg-emerald-600');
        }, 2500);
      };

      // Subtabs
      document.querySelectorAll('.subtab-btn').forEach(btn => {
        btn.onclick = () => {
          document.querySelectorAll('.subtab-btn').forEach(b => b.className = 'subtab-btn px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-400');
          btn.className = 'subtab-btn active px-3.5 py-2 rounded-lg text-xs font-semibold bg-red-600 text-white';
          document.querySelectorAll('.data-subpanel').forEach(p => p.classList.add('hidden'));
          $(btn.getAttribute('data-target')).classList.remove('hidden');
        };
      });

      // CSV upload
      $('input-file-csv').onchange = async e => {
        const file = e.target.files[0];
        if (!file) return;
        const txt = await file.text();
        const lines = txt.split(/\r?\n/).filter(l => l.trim().length > 0);
        if (lines.length > 1) {
          const headers = lines[0].split(',').map((h, i) => h.trim() || `Kolom_${i+1}`);
          const rows = [];
          for (let i = 1; i < lines.length; i++) {
            const vals = lines[i].split(',').map(v => v.trim());
            const r = { _id: `csv-${i}` };
            headers.forEach((h, idx) => { r[h] = vals[idx] ?? ''; });
            rows.push(r);
          }
          applyData(headers, rows);
          $('data-import-alert').className = 'p-3 rounded-xl text-xs bg-emerald-950 border border-emerald-700 text-emerald-200';
          $('data-import-alert').textContent = `Berhasil memuat ${rows.length} entri CSV!`;
          $('data-import-alert').classList.remove('hidden');
        }
      };

      // GSheet Fetch
      $('btn-fetch-gsheet').onclick = async () => {
        const url = $('input-gsheet-url').value.trim();
        if (!url) { alert('Masukkan link Google Spreadsheet'); return; }
        try {
          $('btn-fetch-gsheet').textContent = 'Mengambil...';
          const match = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
          if (!match) throw new Error('Format link Google Spreadsheet tidak valid.');
          const csvUrl = `https://docs.google.com/spreadsheets/d/${match[1]}/export?format=csv`;
          const res = await fetch(csvUrl);
          if (!res.ok) throw new Error('Gagal menarik data. Pastikan spreadsheet disetel publik.');
          const txt = await res.text();
          const lines = txt.split(/\r?\n/).filter(l => l.trim().length > 0);
          if (lines.length > 1) {
            const headers = lines[0].split(',').map((h, i) => h.trim() || `Kolom_${i+1}`);
            const rows = [];
            for (let i = 1; i < lines.length; i++) {
              const vals = lines[i].split(',').map(v => v.trim());
              const r = { _id: `gsheet-${i}` };
              headers.forEach((h, idx) => { r[h] = vals[idx] ?? ''; });
              rows.push(r);
            }
            applyData(headers, rows);
            $('data-import-alert').className = 'p-3 rounded-xl text-xs bg-emerald-950 border border-emerald-700 text-emerald-200';
            $('data-import-alert').textContent = `Berhasil memuat ${rows.length} data Google Spreadsheet!`;
            $('data-import-alert').classList.remove('hidden');
          }
        } catch (err) {
          alert(err.message || 'Gagal memuat Google Spreadsheet.');
        } finally {
          $('btn-fetch-gsheet').textContent = 'Tarik Data';
        }
      };

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
          $('data-import-alert').className = 'p-3 rounded-xl text-xs bg-emerald-950 border border-emerald-700 text-emerald-200';
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
        state.tableCurrentPage++;
        if (state.lastDrawSession) renderTableRows(state.lastDrawSession.winners);
      };
    }

    function switchTab(tab) {
      state.activeTab = tab;
      $('section-stage').classList.toggle('hidden', tab !== 'stage');
      $('section-config').classList.toggle('hidden', tab !== 'config');
      $('section-data').classList.toggle('hidden', tab !== 'data');

      $('tab-btn-stage').className = `nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold ${tab === 'stage' ? 'bg-red-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}`;
      $('tab-btn-config').className = `nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold ${tab === 'config' ? 'bg-red-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}`;
      $('tab-btn-data').className = `nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold ${tab === 'data' ? 'bg-red-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}`;
    }

    document.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""

# Render full standalone web app directly inside Streamlit
components.html(ALFAMIDI_HTML, height=1000, scrolling=True)
