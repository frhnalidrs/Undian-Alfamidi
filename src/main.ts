/**
 * Alfamidi Lucky Draw - Native Vanilla TypeScript Controller
 * Zero React dependencies. 100% Native HTML, CSS, and DOM APIs.
 */

import confetti from 'canvas-confetti';
import {
  CandidateRecord,
  ColumnMeta,
  DrawSettings,
  WinnerItem,
  DrawHistoryEntry,
  PrizeCategory,
} from './types';
import {
  parseCSV,
  parseExcel,
  fetchGoogleSheet,
  generateSampleAlfamidiData,
  buildCandidateRecords,
  analyzeColumns,
  guessBestColumns,
} from './utils/dataParser';
import { drawWinners } from './utils/drawEngine';
import { soundEffects } from './utils/soundEffects';
import { exportWinnersToExcel, exportWinnersToPDF } from './utils/exportUtils';

// =============================================================================
// STORAGE KEYS & DEFAULT CATEGORIES
// =============================================================================
const SETTINGS_STORAGE_KEY = 'alfamidi_lucky_draw_settings_v2';
const HISTORY_STORAGE_KEY = 'alfamidi_lucky_draw_history_v2';

const defaultCategories: PrizeCategory[] = [
  { id: 'cat-1', name: 'Grand Prize - Sepeda Motor Honda Beat', winnerCount: 1 },
  { id: 'cat-2', name: 'Hadiah Utama 1 - Smart TV 55 Inch & iPhone', winnerCount: 3 },
  { id: 'cat-3', name: 'Hadiah Utama 2 - Logam Mulia Emas 10 Gram', winnerCount: 5 },
  { id: 'cat-4', name: 'Hadiah Hiburan - Voucher Belanja Alfamidi Rp 1.000.000', winnerCount: 10 },
  { id: 'cat-5', name: 'Doorprize Akbar - Paket Elektronik Rumah Tangga', winnerCount: 20 },
];

// =============================================================================
// APPLICATION STATE
// =============================================================================
interface AppState {
  candidates: CandidateRecord[];
  columns: ColumnMeta[];
  settings: DrawSettings;
  drawHistory: DrawHistoryEntry[];
  wonIds: Set<string>;
  recentWinners: WinnerItem[] | null;
  lastDrawSession: {
    winners: WinnerItem[];
    groupName: string;
    eventTitle: string;
    displayColumns: string[];
  } | null;
  isSpinning: boolean;
  activeTab: 'stage' | 'config' | 'data';
  activeDataSubtab: string;
  tableSearchTerm: string;
  tableCurrentPage: number;
  tablePageSize: number;
  reelItems: { name: string; extra: string }[];
}

function loadInitialSettings(): DrawSettings {
  try {
    const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed && Array.isArray(parsed.categories) && parsed.categories.length > 0) {
        return parsed;
      }
    }
  } catch {
    // Ignore storage parse errors
  }
  return {
    nameColumn: 'NAMA_KARYAWAN',
    useWeighting: false,
    weightColumn: 'POIN_UNDIAN',
    winnerCount: 1,
    groupName: defaultCategories[0].name,
    displayColumns: ['NIK', 'JABATAN'],
    eventTitle: 'DOORPRIZE 20 TAHUN ALFAMIDI',
    allowDuplicateWinners: false,
    categories: defaultCategories,
  };
}

function loadInitialHistory(): DrawHistoryEntry[] {
  try {
    const saved = localStorage.getItem(HISTORY_STORAGE_KEY);
    if (saved) return JSON.parse(saved);
  } catch {
    // Ignore storage parse errors
  }
  return [];
}

const state: AppState = {
  candidates: [],
  columns: [],
  settings: loadInitialSettings(),
  drawHistory: loadInitialHistory(),
  wonIds: new Set<string>(),
  recentWinners: null,
  lastDrawSession: null,
  isSpinning: false,
  activeTab: 'stage',
  activeDataSubtab: 'panel-sample',
  tableSearchTerm: '',
  tableCurrentPage: 1,
  tablePageSize: 15,
  reelItems: [
    { name: 'ALFAMIDI', extra: 'SIAP UNDI' },
    { name: 'DOORPRIZE', extra: 'SIAP UNDI' },
    { name: '18 TAHUN', extra: 'SIAP UNDI' },
  ],
};

// Rebuild wonIds from history if duplicate prevention is enabled
state.drawHistory.forEach(h => {
  h.winners.forEach(w => state.wonIds.add(w.id));
});

if (state.drawHistory.length > 0) {
  const latest = state.drawHistory[0];
  state.lastDrawSession = {
    winners: latest.winners,
    groupName: latest.groupName,
    eventTitle: latest.eventTitle,
    displayColumns: latest.displayColumns,
  };
}

let spinInterval: number | null = null;

// =============================================================================
// DOM ELEMENT HELPERS
// =============================================================================
const $ = <T extends HTMLElement = HTMLElement>(id: string): T => {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Element #${id} not found in DOM`);
  return el as T;
};

// =============================================================================
// PERSISTENCE HELPERS
// =============================================================================
function saveSettings(): void {
  try {
    localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(state.settings));
  } catch {
    // Ignore storage quota
  }
}

function saveHistory(): void {
  try {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(state.drawHistory));
  } catch {
    // Ignore storage quota
  }
}

// =============================================================================
// UI RENDERING FUNCTIONS
// =============================================================================

function updateQuickInfoStrip(): void {
  const activeGroupEl = $('info-active-group');
  const winnerCountEl = $('info-winner-count');
  const formatPreviewEl = $('info-format-preview');
  const candidateStatsEl = $('info-candidate-stats');

  activeGroupEl.textContent = state.settings.groupName || '-';
  winnerCountEl.textContent = `${state.settings.winnerCount} Pemenang`;

  const previewCols = [state.settings.nameColumn];
  state.settings.displayColumns.forEach(c => {
    if (c !== state.settings.nameColumn) previewCols.push(c);
  });
  formatPreviewEl.textContent = `[${previewCols.join(' - ')}]`;

  const available = state.settings.allowDuplicateWinners
    ? state.candidates.length
    : Math.max(0, state.candidates.length - state.wonIds.size);

  candidateStatsEl.textContent = `${available.toLocaleString('id-ID')} / ${state.candidates.length.toLocaleString('id-ID')}`;

  $('bottom-total-candidates').textContent = state.candidates.length.toLocaleString('id-ID');
  $('config-available-count').textContent = available.toLocaleString('id-ID');
  $('data-active-counter-text').textContent = `${state.candidates.length.toLocaleString('id-ID')} Peserta Aktif`;

  // Update Re-open Last Modal Buttons visibility
  const btnTopLast = $('btn-view-last-modal');
  const btnBottomLast = $('btn-bottom-last-modal');
  if (state.lastDrawSession && state.lastDrawSession.winners.length > 0) {
    btnTopLast.classList.remove('hidden');
    btnTopLast.classList.add('flex');
    btnBottomLast.classList.remove('hidden');
    btnBottomLast.classList.add('flex');
    $('btn-bottom-last-modal-text').textContent = `Lihat Modal Terakhir (${state.lastDrawSession.winners.length})`;
  } else {
    btnTopLast.classList.add('hidden');
    btnTopLast.classList.remove('flex');
    btnBottomLast.classList.add('hidden');
    btnBottomLast.classList.remove('flex');
  }

  // Update History Badge
  const badgeCountEl = $('history-badge-count');
  if (state.drawHistory.length > 0) {
    badgeCountEl.textContent = String(state.drawHistory.length);
    badgeCountEl.classList.remove('hidden');
    badgeCountEl.classList.add('flex');
  } else {
    badgeCountEl.classList.add('hidden');
    badgeCountEl.classList.remove('flex');
  }
}

function renderStageReels(): void {
  const container = $('slot-reels-grid');
  const numReels = Math.min(3, Math.max(1, state.settings.winnerCount));

  container.className = `grid gap-3 sm:gap-4 relative z-0 ${
    numReels === 1 ? 'grid-cols-1' : numReels === 2 ? 'grid-cols-2' : 'grid-cols-1 sm:grid-cols-3'
  }`;

  const isSlotWinner =
    state.recentWinners &&
    state.recentWinners.length > 0 &&
    state.recentWinners.length <= 3 &&
    !state.isSpinning;

  container.innerHTML = '';

  for (let idx = 0; idx < numReels; idx++) {
    const item = state.reelItems[idx] || { name: 'Alfamidi', extra: 'Siap Undi' };
    const winner = isSlotWinner && state.recentWinners ? state.recentWinners[idx] : null;

    const reelEl = document.createElement('div');
    reelEl.className = `h-28 sm:h-36 rounded-xl border-2 flex flex-col items-center justify-center text-center p-2.5 transition-all relative overflow-hidden ${
      winner
        ? 'bg-gradient-to-b from-amber-100 via-white to-amber-50 border-amber-400 shadow-[0_0_20px_#f59e0b]'
        : 'bg-gradient-to-b from-slate-800 to-slate-900 border-slate-700 text-slate-100 shadow-inner'
    } ${state.isSpinning ? 'blur-[0.5px] scale-[0.99]' : ''}`;

    let badgeHtml = '';
    if (winner) {
      badgeHtml = `<span class="absolute top-1.5 right-1.5 px-2 py-0.5 bg-red-600 text-white text-[10px] font-black rounded-full uppercase shadow-xs">Pemenang #${idx + 1}</span>`;
    }

    const titleColor = winner ? 'text-red-700' : 'text-amber-300';
    const subColor = winner ? 'text-slate-700 font-semibold' : 'text-slate-400';

    reelEl.innerHTML = `
      ${badgeHtml}
      <div class="w-full my-auto">
        <p class="font-black text-sm sm:text-base md:text-lg tracking-tight uppercase line-clamp-2 px-1 ${titleColor}">
          ${winner ? winner.name : item.name}
        </p>
        <p class="text-[11px] sm:text-xs font-medium mt-1 line-clamp-2 px-1 ${subColor}">
          ${winner ? (winner.displayFormatted || winner.group) : item.extra}
        </p>
      </div>
    `;

    container.appendChild(reelEl);
  }

  // Toggle "Undi Ulang" button on stage if <= 3 winners
  const btnReset = $('btn-reset-draw');
  if (isSlotWinner) {
    btnReset.classList.remove('hidden');
  } else {
    btnReset.classList.add('hidden');
  }
}

function renderStageCategoriesDropdown(): void {
  const select = $<HTMLSelectElement>('stage-category-select');
  select.innerHTML = '';

  state.settings.categories.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat.name;
    opt.textContent = `${cat.name} (${cat.winnerCount} Pemenang)`;
    if (cat.name === state.settings.groupName) {
      opt.selected = true;
    }
    select.appendChild(opt);
  });

  $<HTMLInputElement>('stage-winner-count-input').value = String(state.settings.winnerCount);
}

function renderConfigPanel(): void {
  $<HTMLInputElement>('input-event-title').value = state.settings.eventTitle;
  $('marquee-event-title').textContent = state.settings.eventTitle;
  $('envelope-body-event-title').textContent = state.settings.eventTitle;
  $('letter-event-title').textContent = state.settings.eventTitle;
  $('table-modal-event-title').textContent = state.settings.eventTitle;

  // Bulk textarea
  const lines = state.settings.categories.map(c => `${c.name} | ${c.winnerCount}`).join('\n');
  $<HTMLTextAreaElement>('textarea-bulk-categories').value = lines;
  $('config-categories-count').textContent = `${state.settings.categories.length} Kategori Aktif`;

  // Categories chips
  const chipsContainer = $('config-categories-chips');
  chipsContainer.innerHTML = '';
  state.settings.categories.forEach(cat => {
    const chip = document.createElement('div');
    chip.className = 'flex items-center justify-between p-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-200';
    chip.innerHTML = `
      <div class="flex items-center gap-2 truncate pr-2">
        <span class="font-semibold text-white truncate">${cat.name}</span>
        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold flex-shrink-0">${cat.winnerCount} pemenang</span>
      </div>
      <button type="button" class="btn-delete-category text-slate-500 hover:text-red-400 p-1 rounded transition-colors cursor-pointer" data-id="${cat.id}" title="Hapus Kategori">
        ✕
      </button>
    `;
    chipsContainer.appendChild(chip);
  });

  // Name column dropdown
  const nameSelect = $<HTMLSelectElement>('select-name-column');
  nameSelect.innerHTML = '';
  state.columns.forEach(col => {
    const opt = document.createElement('option');
    opt.value = col.name;
    opt.textContent = `${col.name} ${col.sampleValues[0] ? `(misal: ${col.sampleValues[0]})` : ''}`;
    if (col.name === state.settings.nameColumn) opt.selected = true;
    nameSelect.appendChild(opt);
  });

  // Default winner count & notice
  $<HTMLInputElement>('input-default-winner-count').value = String(state.settings.winnerCount);
  $('label-default-winner-count').textContent = `${state.settings.winnerCount} Orang`;
  updateAnimationNotice(state.settings.winnerCount);

  // Weight toggle
  const checkWeight = $<HTMLInputElement>('checkbox-use-weighting');
  checkWeight.checked = state.settings.useWeighting;
  const weightContainer = $('weight-column-container');
  if (state.settings.useWeighting) {
    weightContainer.classList.remove('hidden');
  } else {
    weightContainer.classList.add('hidden');
  }

  // Weight column selector
  const weightSelect = $<HTMLSelectElement>('select-weight-column');
  weightSelect.innerHTML = '';
  state.columns.forEach(col => {
    const opt = document.createElement('option');
    opt.value = col.name;
    opt.textContent = `${col.name} ${col.isNumeric ? '⭐ (Kolom Angka Terdeteksi)' : ''}`;
    if (col.name === state.settings.weightColumn) opt.selected = true;
    weightSelect.appendChild(opt);
  });

  // Display columns checkboxes
  const displayGrid = $('config-display-checkboxes-grid');
  displayGrid.innerHTML = '';
  state.columns.forEach(col => {
    const isSelected = state.settings.displayColumns.includes(col.name);
    const isPrimary = col.name === state.settings.nameColumn;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `btn-toggle-display-col flex items-center gap-2 p-2 rounded-lg text-left text-xs transition-colors cursor-pointer border ${
      isSelected
        ? 'bg-red-950/60 border-red-500/60 text-white font-semibold'
        : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
    }`;
    btn.dataset.col = col.name;
    btn.innerHTML = `
      <span class="w-3.5 h-3.5 flex items-center justify-center font-bold text-xs ${isSelected ? 'text-red-400' : 'text-slate-600'}">
        ${isSelected ? '☑' : '☐'}
      </span>
      <span class="truncate">${col.name} ${isPrimary ? '(Nama)' : ''}</span>
    `;
    displayGrid.appendChild(btn);
  });

  $('config-display-selected-count').textContent = `${state.settings.displayColumns.length} terpilih`;

  // Output format box
  const previewParts = [state.settings.nameColumn];
  state.settings.displayColumns.forEach(c => {
    if (c !== state.settings.nameColumn) previewParts.push(c);
  });
  $('config-format-sample-box').textContent = previewParts.join(' - ');

  // Duplicate lock
  $<HTMLInputElement>('checkbox-prevent-duplicate').checked = !state.settings.allowDuplicateWinners;
}

function updateAnimationNotice(count: number): void {
  const badgeEl = $('animation-notice-badge');
  const textEl = $('animation-notice-text');

  if (count <= 3) {
    badgeEl.className = 'p-2.5 rounded-xl border flex items-center gap-2 text-xs font-bold text-amber-400 bg-amber-950/60 border-amber-500/40';
    textEl.textContent = '🎰 Slot Machine';
  } else if (count <= 10) {
    badgeEl.className = 'p-2.5 rounded-xl border flex items-center gap-2 text-xs font-bold text-red-400 bg-red-950/60 border-red-500/40';
    textEl.textContent = '✉️ Animasi Surat';
  } else {
    badgeEl.className = 'p-2.5 rounded-xl border flex items-center gap-2 text-xs font-bold text-blue-400 bg-blue-950/60 border-blue-500/40';
    textEl.textContent = '📊 Tabel Pemenang Komprehensif';
  }
}

function renderDataPreview(): void {
  const thead = $('data-preview-thead');
  const tbody = $('data-preview-tbody');
  $('data-columns-detected-text').textContent = `${state.columns.length} Kolom Terdeteksi: ${state.columns.map(c => c.name).join(', ')}`;

  thead.innerHTML = '';
  tbody.innerHTML = '';

  if (state.columns.length === 0 || state.candidates.length === 0) return;

  const headerRow = document.createElement('tr');
  headerRow.innerHTML = `<th class="py-2 px-3 w-10 text-center">#</th>` +
    state.columns.map(col => `
      <th class="py-2 px-3 whitespace-nowrap">
        ${col.name} ${col.isNumeric ? '<span class="ml-1 text-[10px] text-amber-400 font-normal">(angka)</span>' : ''}
      </th>
    `).join('');
  thead.appendChild(headerRow);

  state.candidates.slice(0, 5).forEach((cand, idx) => {
    const row = document.createElement('tr');
    row.className = 'hover:bg-slate-800/40';
    row.innerHTML = `<td class="py-2 px-3 text-center text-slate-500 font-mono">${idx + 1}</td>` +
      state.columns.map(col => `<td class="py-2 px-3 text-slate-300 whitespace-nowrap">${String(cand[col.name] ?? '')}</td>`).join('');
    tbody.appendChild(row);
  });
}

function showDataAlert(msg: string, type: 'success' | 'error'): void {
  const alertEl = $('data-import-alert');
  alertEl.className = `p-3 rounded-xl text-xs flex items-center gap-2 ${
    type === 'success' ? 'bg-emerald-950/70 border border-emerald-700/60 text-emerald-200' : 'bg-red-950/70 border border-red-700/60 text-red-200'
  }`;
  alertEl.textContent = msg;
  alertEl.classList.remove('hidden');
}

function switchTab(tab: 'stage' | 'config' | 'data'): void {
  state.activeTab = tab;

  // Toggle tab buttons visual
  $('tab-btn-stage').className = `nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
    tab === 'stage' ? 'bg-red-600 text-white shadow-sm' : 'text-slate-400 hover:text-white hover:bg-slate-800'
  }`;
  $('tab-btn-config').className = `nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
    tab === 'config' ? 'bg-red-600 text-white shadow-sm' : 'text-slate-400 hover:text-white hover:bg-slate-800'
  }`;
  $('tab-btn-data').className = `nav-tab flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
    tab === 'data' ? 'bg-red-600 text-white shadow-sm' : 'text-slate-400 hover:text-white hover:bg-slate-800'
  }`;

  // Toggle sections
  $('section-stage').classList.toggle('hidden', tab !== 'stage');
  $('section-config').classList.toggle('hidden', tab !== 'config');
  $('section-data').classList.toggle('hidden', tab !== 'data');

  if (tab === 'stage') {
    renderStageReels();
    renderStageCategoriesDropdown();
  } else if (tab === 'config') {
    renderConfigPanel();
  } else if (tab === 'data') {
    renderDataPreview();
  }

  updateQuickInfoStrip();
}

// =============================================================================
// MODAL POPUPS (ENVELOPE, TABLE, HISTORY, STREAMLIT)
// =============================================================================

function openEnvelopeModal(winners: WinnerItem[], groupName: string, eventTitle: string): void {
  const modal = $('modal-envelope');
  modal.classList.remove('hidden');
  soundEffects.playWhoosh();

  $('letter-category-name').textContent = groupName || 'Doorprize';
  $('letter-event-title').textContent = eventTitle || state.settings.eventTitle;
  $('envelope-body-event-title').textContent = eventTitle || state.settings.eventTitle;
  $('envelope-body-subtitle').textContent = `${groupName} • ${winners.length} PEMENANG RESMI`;
  $('letter-subtitle').textContent = `Selamat kepada ${winners.length} rekan karyawan Alfamidi berikut yang beruntung:`;
  $('letter-total-winners-count').textContent = `TOTAL: ${winners.length} PEMENANG`;
  $('letter-current-date').textContent = new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' });

  const listContainer = $('envelope-winners-list');
  listContainer.innerHTML = '';

  winners.forEach((winner, idx) => {
    const itemEl = document.createElement('div');
    itemEl.className = 'flex items-start gap-3 p-3 sm:p-3.5 bg-gradient-to-r from-red-50/70 via-white to-amber-50/50 rounded-lg border border-red-100 shadow-xs';
    itemEl.innerHTML = `
      <div class="flex-shrink-0 w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-red-600 text-white font-extrabold text-xs sm:text-sm flex items-center justify-center shadow-xs">
        ${winner.rank || idx + 1}
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm sm:text-base font-bold text-slate-900 tracking-tight leading-snug">
          ${winner.displayFormatted}
        </p>
        ${winner.weightScore !== undefined ? `<p class="text-[11px] text-slate-500 mt-0.5">Bobot Poin: <span class="font-semibold text-slate-700">${winner.weightScore}</span></p>` : ''}
      </div>
      <span class="text-emerald-600 font-bold text-xs flex-shrink-0 mt-1">✓ Terpilih</span>
    `;
    listContainer.appendChild(itemEl);
  });

  // Confetti fanfare
  setTimeout(() => {
    soundEffects.playFanfare();
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#d71920', '#ffcc00', '#1e40af', '#ffffff'],
    });
  }, 400);
}

function closeEnvelopeModal(): void {
  $('modal-envelope').classList.add('hidden');
}

function openTableModal(winners: WinnerItem[], groupName: string, eventTitle: string): void {
  const modal = $('modal-table');
  modal.classList.remove('hidden');

  $('table-modal-winner-count-badge').textContent = `${winners.length} PEMENANG`;
  $('table-modal-event-title').textContent = eventTitle || state.settings.eventTitle;
  $('table-modal-category-name').textContent = groupName || 'Hadiah Utama';
  $<HTMLInputElement>('input-search-table-modal').value = '';
  state.tableSearchTerm = '';
  state.tableCurrentPage = 1;

  renderTableModalRows(winners);

  soundEffects.playFanfare();
  confetti({
    particleCount: 90,
    spread: 100,
    origin: { y: 0.4 },
    colors: ['#d71920', '#ffcc00', '#1e40af', '#ffffff'],
  });
}

function renderTableModalRows(winners: WinnerItem[]): void {
  const thead = $('table-modal-thead');
  const tbody = $('table-modal-tbody');

  // Filter
  const term = state.tableSearchTerm.toLowerCase();
  const filtered = !term
    ? winners
    : winners.filter(w => {
        if (w.name.toLowerCase().includes(term)) return true;
        if (w.displayFormatted.toLowerCase().includes(term)) return true;
        return Object.values(w.data).some(v => String(v).toLowerCase().includes(term));
      });

  const totalPages = Math.max(1, Math.ceil(filtered.length / state.tablePageSize));
  state.tableCurrentPage = Math.min(state.tableCurrentPage, totalPages);

  const startIdx = (state.tableCurrentPage - 1) * state.tablePageSize;
  const paginated = filtered.slice(startIdx, startIdx + state.tablePageSize);

  // Table Headers
  thead.innerHTML = `
    <tr>
      <th class="py-3 px-4 w-14 text-center">No</th>
      <th class="py-3 px-4">Nama Pemenang</th>
      <th class="py-3 px-4">Format Pengumuman</th>
      ${state.settings.displayColumns.map(col => `<th class="py-3 px-4">${col}</th>`).join('')}
      <th class="py-3 px-4 text-right">Status</th>
    </tr>
  `;

  // Table Body
  tbody.innerHTML = '';
  if (paginated.length === 0) {
    tbody.innerHTML = `<tr><td colspan="${4 + state.settings.displayColumns.length}" class="py-12 text-center text-slate-400 text-sm">Tidak ditemukan pemenang yang sesuai kata kunci.</td></tr>`;
  } else {
    paginated.forEach((w, idx) => {
      const absNo = startIdx + idx + 1;
      const tr = document.createElement('tr');
      tr.className = 'hover:bg-slate-800/60 transition-colors group';
      tr.innerHTML = `
        <td class="py-3 px-4 text-center font-mono text-xs text-slate-400 font-bold group-hover:text-amber-400">${absNo}</td>
        <td class="py-3 px-4">
          <div class="font-bold text-white text-sm">${w.name}</div>
          ${w.weightScore !== undefined ? `<div class="text-[11px] text-amber-400/90 font-mono">Skor: ${w.weightScore}</div>` : ''}
        </td>
        <td class="py-3 px-4 text-slate-200 font-medium">
          <span class="inline-block px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-xs">${w.displayFormatted}</span>
        </td>
        ${state.settings.displayColumns.map(col => `<td class="py-3 px-4 text-slate-300 text-xs">${String(w.data[col] ?? '-')}</td>`).join('')}
        <td class="py-3 px-4 text-right">
          <span class="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-400">✓ Terpilih</span>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }

  // Pagination info
  $('table-modal-pagination-info').textContent = `Menampilkan ${filtered.length > 0 ? startIdx + 1 : 0} - ${Math.min(startIdx + state.tablePageSize, filtered.length)} dari ${filtered.length} pemenang`;
  $('table-modal-page-num').textContent = `Halaman ${state.tableCurrentPage} / ${totalPages}`;

  ($('btn-table-prev-page') as HTMLButtonElement).disabled = state.tableCurrentPage <= 1;
  ($('btn-table-next-page') as HTMLButtonElement).disabled = state.tableCurrentPage >= totalPages;
}

function closeTableModal(): void {
  $('modal-table').classList.add('hidden');
}

function openHistoryDrawer(): void {
  const drawer = $('drawer-history');
  drawer.classList.remove('hidden');

  $('drawer-history-stats').textContent = `${state.drawHistory.length} Putaran Selesai · ${state.drawHistory.reduce((s, h) => s + h.winners.length, 0)} Total Pemenang`;

  const globalActions = $('drawer-history-global-actions');
  const listContainer = $('drawer-history-list');

  if (state.drawHistory.length > 0) {
    globalActions.classList.remove('hidden');
    globalActions.classList.add('flex');
  } else {
    globalActions.classList.add('hidden');
    globalActions.classList.remove('flex');
  }

  listContainer.innerHTML = '';
  if (state.drawHistory.length === 0) {
    listContainer.innerHTML = `
      <div class="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500">
        <p class="font-semibold text-sm text-slate-400">Belum Ada Putaran Undian</p>
        <p class="text-xs mt-1">Tekan tombol undi pada panggung untuk memulai putaran undian.</p>
      </div>
    `;
    return;
  }

  state.drawHistory.forEach((entry, idx) => {
    const itemEl = document.createElement('div');
    itemEl.className = 'p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2.5 hover:border-slate-700 transition-colors';
    itemEl.innerHTML = `
      <div class="flex items-start justify-between gap-2">
        <div>
          <span class="text-[10px] font-bold uppercase tracking-wider text-red-400">Putaran #${state.drawHistory.length - idx}</span>
          <h4 class="text-sm font-bold text-white leading-tight">${entry.groupName}</h4>
          <p class="text-[11px] text-slate-400 mt-0.5">
            ${new Date(entry.timestamp).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })} WIB · ${entry.winners.length} Pemenang
          </p>
        </div>
        <div class="flex items-center gap-1">
          <button type="button" class="btn-history-preview p-1.5 rounded-md hover:bg-slate-800 text-amber-400 cursor-pointer" data-id="${entry.id}" title="Buka Modal Tampilan Hasil Ini">
            👁️
          </button>
          <button type="button" class="btn-history-excel p-1.5 rounded-md hover:bg-slate-800 text-emerald-400 cursor-pointer" data-id="${entry.id}" title="Unduh Excel">
            📊
          </button>
          <button type="button" class="btn-history-pdf p-1.5 rounded-md hover:bg-slate-800 text-red-400 cursor-pointer" data-id="${entry.id}" title="Cetak PDF">
            📄
          </button>
        </div>
      </div>
      <div class="space-y-1 pt-1 border-t border-slate-800/80">
        ${entry.winners.slice(0, 3).map(w => `
          <div class="text-xs text-slate-300 truncate">
            <strong class="text-slate-400 mr-1.5">#${w.rank}</strong>${w.displayFormatted}
          </div>
        `).join('')}
        ${entry.winners.length > 3 ? `<div class="text-[11px] text-amber-400 italic">+${entry.winners.length - 3} pemenang lainnya</div>` : ''}
      </div>
    `;
    listContainer.appendChild(itemEl);
  });
}

function closeHistoryDrawer(): void {
  $('drawer-history').classList.add('hidden');
}

// =============================================================================
// CORE DRAW EXECUTION
// =============================================================================

function triggerDraw(): void {
  if (state.isSpinning || state.candidates.length === 0) return;

  const winners = drawWinners(state.candidates, state.settings, state.wonIds);
  if (winners.length === 0) {
    alert('Tidak ada peserta yang tersisa untuk diundi.');
    return;
  }

  state.isSpinning = true;
  state.recentWinners = null;

  soundEffects.playLeverPull();

  const buttonArcade = $('btn-arcade-red-button');
  buttonArcade.classList.add('is-pressed');
  setTimeout(() => buttonArcade.classList.remove('is-pressed'), 250);

  $('btn-main-spin').textContent = 'SEDANG MEMUTAR...';
  ($('btn-main-spin') as HTMLButtonElement).disabled = true;

  const winnerCount = state.settings.winnerCount;
  const sessionData = {
    winners,
    groupName: state.settings.groupName,
    eventTitle: state.settings.eventTitle,
    displayColumns: state.settings.displayColumns,
  };

  // Spinning loop
  const nameCol = state.settings.nameColumn;
  const extraCols = state.settings.displayColumns.filter(c => c !== nameCol);
  let tickCounter = 0;

  spinInterval = window.setInterval(() => {
    tickCounter++;
    if (tickCounter % 3 === 0) {
      soundEffects.playReelTick(Math.random() * 40 - 20);
    }
    const numReels = Math.min(3, Math.max(1, state.settings.winnerCount));
    const newItems: { name: string; extra: string }[] = [];
    for (let i = 0; i < numReels; i++) {
      const randIdx = Math.floor(Math.random() * state.candidates.length);
      const cand = state.candidates[randIdx];
      const name = cand ? String(cand[nameCol] || 'Kandidat') : 'Alfamidi';
      const extra = extraCols.length > 0 && cand
        ? extraCols.map(c => String(cand[c] || '')).filter(Boolean).join(' • ')
        : 'Peserta Undian';
      newItems.push({ name, extra });
    }
    state.reelItems = newItems;
    renderStageReels();
  }, 50);

  // Stop duration based on count
  const spinDuration = winnerCount <= 3 ? 2400 : 2000;

  setTimeout(() => {
    if (spinInterval) {
      clearInterval(spinInterval);
      spinInterval = null;
    }

    state.isSpinning = false;
    state.recentWinners = winners;
    state.lastDrawSession = sessionData;

    $('btn-main-spin').textContent = 'PUTAR UNDIAN SEKARANG';
    ($('btn-main-spin') as HTMLButtonElement).disabled = false;

    // Record History
    const historyEntry: DrawHistoryEntry = {
      id: `draw-${Date.now()}`,
      groupName: state.settings.groupName,
      eventTitle: state.settings.eventTitle,
      timestamp: new Date().toISOString(),
      winnerCount: winners.length,
      displayColumns: state.settings.displayColumns,
      winners,
    };
    state.drawHistory.unshift(historyEntry);
    saveHistory();

    if (!state.settings.allowDuplicateWinners) {
      winners.forEach(w => state.wonIds.add(w.id));
    }

    updateQuickInfoStrip();

    // 3 TIER REVEAL:
    // <= 3 : Direct Slot Machine
    // 4-10 : Vintage Airmail Envelope Modal
    // > 10 : Comprehensive Table Modal
    if (winnerCount <= 3) {
      renderStageReels();
      soundEffects.playReelStop(659.25);
      soundEffects.playFanfare();
      confetti({
        particleCount: 75,
        spread: 80,
        origin: { y: 0.55 },
        colors: ['#d71920', '#ffcc00', '#ffffff'],
      });
    } else if (winnerCount <= 10) {
      openEnvelopeModal(winners, state.settings.groupName, state.settings.eventTitle);
    } else {
      openTableModal(winners, state.settings.groupName, state.settings.eventTitle);
    }
  }, spinDuration);
}

// =============================================================================
// INITIALIZATION & EVENT LISTENERS BINDING
// =============================================================================

function setupEventListeners(): void {
  // Navigation Tabs
  $('tab-btn-stage').addEventListener('click', () => switchTab('stage'));
  $('tab-btn-config').addEventListener('click', () => switchTab('config'));
  $('tab-btn-data').addEventListener('click', () => switchTab('data'));

  // Sound toggle
  $('btn-toggle-sound').addEventListener('click', () => {
    soundEffects.enabled = !soundEffects.enabled;
    $('sound-status-text').textContent = soundEffects.enabled ? 'Suara ON' : 'Mute';
    $('btn-toggle-sound').classList.toggle('opacity-60', !soundEffects.enabled);
  });

  // Stage Category dropdown
  $('stage-category-select').addEventListener('change', (e) => {
    const val = (e.target as HTMLSelectElement).value;
    state.settings.groupName = val;
    const matched = state.settings.categories.find(c => c.name === val);
    if (matched) {
      state.settings.winnerCount = matched.winnerCount;
      $<HTMLInputElement>('stage-winner-count-input').value = String(matched.winnerCount);
    }
    saveSettings();
    updateQuickInfoStrip();
    renderStageReels();
  });

  // Stage Winner count input
  $('stage-winner-count-input').addEventListener('input', (e) => {
    const val = Math.max(1, parseInt((e.target as HTMLInputElement).value) || 1);
    state.settings.winnerCount = val;
    saveSettings();
    updateQuickInfoStrip();
    renderStageReels();
  });

  // Quick count chips on stage
  document.querySelectorAll('.btn-quick-count').forEach(btn => {
    btn.addEventListener('click', () => {
      const cnt = parseInt(btn.getAttribute('data-count') || '1');
      state.settings.winnerCount = cnt;
      $<HTMLInputElement>('stage-winner-count-input').value = String(cnt);
      saveSettings();
      updateQuickInfoStrip();
      renderStageReels();
    });
  });

  // Arcade Big Red Button + Bottom Spin Button
  $('btn-arcade-red-button').addEventListener('click', triggerDraw);
  $('btn-main-spin').addEventListener('click', triggerDraw);

  // Undi Ulang Button
  $('btn-reset-draw').addEventListener('click', () => {
    state.recentWinners = null;
    renderStageReels();
  });

  // Re-open Last Modal Buttons
  const handleOpenLastModal = () => {
    if (!state.lastDrawSession) return;
    const { winners, groupName, eventTitle } = state.lastDrawSession;
    if (winners.length <= 10) {
      openEnvelopeModal(winners, groupName, eventTitle);
    } else {
      openTableModal(winners, groupName, eventTitle);
    }
  };
  $('btn-view-last-modal').addEventListener('click', handleOpenLastModal);
  $('btn-bottom-last-modal').addEventListener('click', handleOpenLastModal);

  // History Drawer Open / Close
  $('btn-open-history').addEventListener('click', openHistoryDrawer);
  $('btn-close-history-drawer').addEventListener('click', closeHistoryDrawer);
  $('btn-history-bottom-close').addEventListener('click', closeHistoryDrawer);

  // History Reset
  $('btn-history-reset-all').addEventListener('click', () => {
    if (confirm('Hapus seluruh riwayat undian dan reset status pemenang?')) {
      state.drawHistory = [];
      state.wonIds.clear();
      state.lastDrawSession = null;
      state.recentWinners = null;
      saveHistory();
      openHistoryDrawer();
      updateQuickInfoStrip();
      renderStageReels();
    }
  });

  // History Global Exports
  $('btn-history-export-all-excel').addEventListener('click', () => {
    const all = state.drawHistory.flatMap(h => h.winners);
    exportWinnersToExcel(all, 'Semua_Putaran', state.settings.eventTitle, state.settings.displayColumns);
  });
  $('btn-history-export-all-pdf').addEventListener('click', () => {
    const all = state.drawHistory.flatMap(h => h.winners);
    exportWinnersToPDF(all, 'Semua_Putaran', state.settings.eventTitle, state.settings.displayColumns);
  });

  // Delegate history list clicks (preview, excel, pdf)
  $('drawer-history-list').addEventListener('click', (e) => {
    const target = (e.target as HTMLElement).closest('button');
    if (!target) return;
    const id = target.getAttribute('data-id');
    const entry = state.drawHistory.find(h => h.id === id);
    if (!entry) return;

    if (target.classList.contains('btn-history-preview')) {
      closeHistoryDrawer();
      if (entry.winners.length <= 10) {
        openEnvelopeModal(entry.winners, entry.groupName, entry.eventTitle);
      } else {
        openTableModal(entry.winners, entry.groupName, entry.eventTitle);
      }
    } else if (target.classList.contains('btn-history-excel')) {
      exportWinnersToExcel(entry.winners, entry.groupName, entry.eventTitle, entry.displayColumns);
    } else if (target.classList.contains('btn-history-pdf')) {
      exportWinnersToPDF(entry.winners, entry.groupName, entry.eventTitle, entry.displayColumns);
    }
  });

  // Envelope Modal Action Buttons
  $('btn-close-envelope-modal').addEventListener('click', closeEnvelopeModal);
  $('btn-envelope-finish').addEventListener('click', closeEnvelopeModal);
  $('btn-envelope-export-excel').addEventListener('click', () => {
    if (state.lastDrawSession) {
      exportWinnersToExcel(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle, state.lastDrawSession.displayColumns);
    }
  });
  $('btn-envelope-export-pdf').addEventListener('click', () => {
    if (state.lastDrawSession) {
      exportWinnersToPDF(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle, state.lastDrawSession.displayColumns);
    }
  });

  // Table Modal Action Buttons
  $('btn-close-table-modal').addEventListener('click', closeTableModal);
  $('btn-table-bottom-close').addEventListener('click', closeTableModal);
  $('input-search-table-modal').addEventListener('input', (e) => {
    state.tableSearchTerm = (e.target as HTMLInputElement).value;
    state.tableCurrentPage = 1;
    if (state.lastDrawSession) renderTableModalRows(state.lastDrawSession.winners);
  });
  $('btn-table-prev-page').addEventListener('click', () => {
    state.tableCurrentPage = Math.max(1, state.tableCurrentPage - 1);
    if (state.lastDrawSession) renderTableModalRows(state.lastDrawSession.winners);
  });
  $('btn-table-next-page').addEventListener('click', () => {
    state.tableCurrentPage++;
    if (state.lastDrawSession) renderTableModalRows(state.lastDrawSession.winners);
  });
  $('btn-table-copy-list').addEventListener('click', () => {
    if (!state.lastDrawSession) return;
    const text = state.lastDrawSession.winners.map((w, idx) => `${idx + 1}. ${w.displayFormatted}`).join('\n');
    navigator.clipboard.writeText(text);
    $('btn-table-copy-list').textContent = '✓ Tersalin!';
    setTimeout(() => {
      $('btn-table-copy-list').textContent = 'Salin Teks';
    }, 2000);
  });
  $('btn-table-export-excel').addEventListener('click', () => {
    if (state.lastDrawSession) {
      exportWinnersToExcel(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle, state.lastDrawSession.displayColumns);
    }
  });
  $('btn-table-export-pdf').addEventListener('click', () => {
    if (state.lastDrawSession) {
      exportWinnersToPDF(state.lastDrawSession.winners, state.lastDrawSession.groupName, state.lastDrawSession.eventTitle, state.lastDrawSession.displayColumns);
    }
  });

  // Streamlit Modal
  $('btn-open-streamlit').addEventListener('click', () => $('modal-streamlit').classList.remove('hidden'));
  $('btn-close-streamlit-modal').addEventListener('click', () => $('modal-streamlit').classList.add('hidden'));
  $('btn-bottom-close-streamlit-modal').addEventListener('click', () => $('modal-streamlit').classList.add('hidden'));
  $('btn-copy-streamlit-cmd').addEventListener('click', () => {
    navigator.clipboard.writeText('pip install -r requirements.txt\nstreamlit run streamlit.py');
    $('btn-copy-streamlit-cmd').textContent = '✓ Tersalin!';
    setTimeout(() => {
      $('btn-copy-streamlit-cmd').textContent = 'Salin Perintah';
    }, 2000);
  });
  $('btn-download-streamlit-py').addEventListener('click', () => {
    fetch('/streamlit.py')
      .then(res => res.text())
      .then(txt => {
        const blob = new Blob([txt], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'streamlit.py';
        a.click();
        URL.revokeObjectURL(url);
      })
      .catch(() => alert('File streamlit.py tersedia di direktori project'));
  });

  // Fullscreen Toggle
  $('btn-toggle-fullscreen').addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  });

  // CONFIG PANEL LISTENERS
  $('input-event-title').addEventListener('input', (e) => {
    state.settings.eventTitle = (e.target as HTMLInputElement).value;
    saveSettings();
    updateQuickInfoStrip();
  });

  // Bulk Categories Apply
  $('btn-apply-bulk-categories').addEventListener('click', () => {
    const raw = $<HTMLTextAreaElement>('textarea-bulk-categories').value;
    const lines = raw.split('\n').map(l => l.trim()).filter(Boolean);
    const newCats: PrizeCategory[] = [];

    lines.forEach((line, idx) => {
      if (line.includes('|')) {
        const [n, c] = line.split('|');
        const name = n.trim();
        const cnt = parseInt(c.trim()) || 1;
        if (name) newCats.push({ id: `cat-${Date.now()}-${idx}`, name, winnerCount: cnt });
      } else if (line) {
        newCats.push({ id: `cat-${Date.now()}-${idx}`, name: line, winnerCount: 1 });
      }
    });

    if (newCats.length === 0) {
      newCats.push(defaultCategories[0]);
    }

    state.settings.categories = newCats;
    const match = newCats.find(c => c.name === state.settings.groupName);
    state.settings.groupName = match ? match.name : newCats[0].name;
    state.settings.winnerCount = match ? match.winnerCount : newCats[0].winnerCount;

    saveSettings();
    renderConfigPanel();
    updateQuickInfoStrip();
    renderStageCategoriesDropdown();

    $('btn-apply-bulk-categories').textContent = '✓ Tersimpan!';
    setTimeout(() => {
      $('btn-apply-bulk-categories').textContent = 'Terapkan Kategori';
    }, 2000);
  });

  // Delete Category Chips Delegate
  $('config-categories-chips').addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest('.btn-delete-category');
    if (!btn) return;
    const id = btn.getAttribute('data-id');
    const remaining = state.settings.categories.filter(c => c.id !== id);
    if (remaining.length === 0) return;
    state.settings.categories = remaining;
    if (!remaining.some(c => c.name === state.settings.groupName)) {
      state.settings.groupName = remaining[0].name;
      state.settings.winnerCount = remaining[0].winnerCount;
    }
    saveSettings();
    renderConfigPanel();
    updateQuickInfoStrip();
    renderStageCategoriesDropdown();
  });

  // Name column change
  $('select-name-column').addEventListener('change', (e) => {
    state.settings.nameColumn = (e.target as HTMLSelectElement).value;
    saveSettings();
    updateQuickInfoStrip();
    renderConfigPanel();
  });

  // Default Winner Count input
  $('input-default-winner-count').addEventListener('input', (e) => {
    const val = Math.max(1, parseInt((e.target as HTMLInputElement).value) || 1);
    state.settings.winnerCount = val;
    $('label-default-winner-count').textContent = `${val} Orang`;
    updateAnimationNotice(val);
    saveSettings();
    updateQuickInfoStrip();
  });

  // Config quick count chips
  document.querySelectorAll('.btn-config-quick-count').forEach(btn => {
    btn.addEventListener('click', () => {
      const cnt = parseInt(btn.getAttribute('data-count') || '1');
      state.settings.winnerCount = cnt;
      $<HTMLInputElement>('input-default-winner-count').value = String(cnt);
      $('label-default-winner-count').textContent = `${cnt} Orang`;
      updateAnimationNotice(cnt);
      saveSettings();
      updateQuickInfoStrip();
    });
  });

  // Weight toggle & select
  $('checkbox-use-weighting').addEventListener('change', (e) => {
    state.settings.useWeighting = (e.target as HTMLInputElement).checked;
    $('weight-column-container').classList.toggle('hidden', !state.settings.useWeighting);
    saveSettings();
  });

  $('select-weight-column').addEventListener('change', (e) => {
    state.settings.weightColumn = (e.target as HTMLSelectElement).value;
    saveSettings();
  });

  // Display columns checkboxes delegate
  $('config-display-checkboxes-grid').addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest('.btn-toggle-display-col');
    if (!btn) return;
    const col = btn.getAttribute('data-col');
    if (!col) return;

    if (state.settings.displayColumns.includes(col)) {
      state.settings.displayColumns = state.settings.displayColumns.filter(c => c !== col);
    } else {
      state.settings.displayColumns.push(col);
    }
    saveSettings();
    renderConfigPanel();
    updateQuickInfoStrip();
  });

  // Duplicate prevention checkbox
  $('checkbox-prevent-duplicate').addEventListener('change', (e) => {
    state.settings.allowDuplicateWinners = !(e.target as HTMLInputElement).checked;
    saveSettings();
    updateQuickInfoStrip();
  });

  $('btn-save-to-stage').addEventListener('click', () => switchTab('stage'));

  // DATA IMPORT SUB-TABS
  document.querySelectorAll('.subtab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.subtab-btn').forEach(b => {
        b.className = 'subtab-btn px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer text-slate-400 hover:text-white hover:bg-slate-800';
      });
      btn.className = 'subtab-btn active px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer bg-red-600 text-white shadow-md';

      const target = btn.getAttribute('data-target');
      document.querySelectorAll('.data-subpanel').forEach(p => p.classList.add('hidden'));
      if (target) $(target).classList.remove('hidden');
    });
  });

  // Sample Loaders
  const loadSample = (count: number) => {
    const { headers, rows } = generateSampleAlfamidiData(count);
    applyImportedRows(headers, rows);
    showDataAlert(`Berhasil memuat ${count.toLocaleString('id-ID')} karyawan simulasi Alfamidi!`, 'success');
  };
  $('btn-load-sample-1k').addEventListener('click', () => loadSample(1000));
  $('btn-load-sample-10k').addEventListener('click', () => loadSample(10000));
  $('btn-load-sample-25k').addEventListener('click', () => loadSample(25000));

  // File Upload Excel
  $('input-file-excel').addEventListener('change', async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    try {
      const { headers, rows } = await parseExcel(file);
      applyImportedRows(headers, rows);
      showDataAlert(`Berhasil memuat ${rows.length.toLocaleString('id-ID')} entri dari berkas Excel!`, 'success');
    } catch (err: unknown) {
      showDataAlert((err as Error)?.message || 'Gagal memproses berkas Excel.', 'error');
    }
  });

  // File Upload CSV
  $('input-file-csv').addEventListener('change', async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    try {
      const txt = await file.text();
      const { headers, rows } = parseCSV(txt);
      applyImportedRows(headers, rows);
      showDataAlert(`Berhasil memuat ${rows.length.toLocaleString('id-ID')} entri dari berkas CSV!`, 'success');
    } catch (err: unknown) {
      showDataAlert((err as Error)?.message || 'Gagal memproses berkas CSV.', 'error');
    }
  });

  // Google Spreadsheet Fetch
  $('btn-fetch-gsheet').addEventListener('click', async () => {
    const url = $<HTMLInputElement>('input-gsheet-url').value.trim();
    if (!url) {
      showDataAlert('Masukkan tautan Google Spreadsheet terlebih dahulu.', 'error');
      return;
    }
    try {
      $('btn-fetch-gsheet').textContent = 'Mengambil...';
      const { headers, rows } = await fetchGoogleSheet(url);
      applyImportedRows(headers, rows);
      showDataAlert(`Berhasil menarik ${rows.length.toLocaleString('id-ID')} data dari Google Spreadsheet!`, 'success');
    } catch (err: unknown) {
      showDataAlert((err as Error)?.message || 'Gagal mengambil data dari Google Spreadsheet. Pastikan link disetel publik.', 'error');
    } finally {
      $('btn-fetch-gsheet').textContent = 'Tarik Data';
    }
  });

  // Manual Data Apply
  $('btn-apply-manual-data').addEventListener('click', () => {
    const txt = $<HTMLTextAreaElement>('textarea-manual-data').value.trim();
    try {
      const { headers, rows } = parseCSV(txt);
      applyImportedRows(headers, rows);
      showDataAlert(`Berhasil memuat ${rows.length} data manual!`, 'success');
    } catch (err: unknown) {
      showDataAlert((err as Error)?.message || 'Format teks manual tidak valid.', 'error');
    }
  });
}

function applyImportedRows(headers: string[], rows: Record<string, string | number>[]): void {
  const records = buildCandidateRecords(rows);
  const columns = analyzeColumns(headers, records);
  const { nameCol, weightCol } = guessBestColumns(columns);

  state.candidates = records;
  state.columns = columns;

  if (nameCol) state.settings.nameColumn = nameCol;
  if (weightCol) state.settings.weightColumn = weightCol;

  const extraCols = columns.filter(c => c.name !== nameCol).slice(0, 2).map(c => c.name);
  if (extraCols.length > 0) {
    state.settings.displayColumns = extraCols;
  }

  saveSettings();
  updateQuickInfoStrip();
  renderStageCategoriesDropdown();
  renderStageReels();
  renderConfigPanel();
  renderDataPreview();
}

// =============================================================================
// APP BOOTSTRAP
// =============================================================================
function initApp(): void {
  // Load 1,000 initial sample Alfamidi employees
  const { headers, rows } = generateSampleAlfamidiData(1000);
  applyImportedRows(headers, rows);

  setupEventListeners();
  switchTab('stage');
}

// Initialize when DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
