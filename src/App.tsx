/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useMemo, useCallback } from 'react';
import {
  CandidateRecord,
  ColumnMeta,
  DrawSettings,
  WinnerItem,
  DrawHistoryEntry,
  PrizeCategory,
} from './types';
import { generateSampleAlfamidiData, buildCandidateRecords, analyzeColumns, guessBestColumns } from './utils/dataParser';
import { drawWinners } from './utils/drawEngine';
import { SlotMachine } from './components/SlotMachine';
import { EnvelopeModal } from './components/EnvelopeModal';
import { WinnersTableModal } from './components/WinnersTableModal';
import { DataImportSection } from './components/DataImportSection';
import { DrawConfigPanel } from './components/DrawConfigPanel';
import { DrawHistoryDrawer } from './components/DrawHistoryDrawer';
import { StreamlitModal } from './components/StreamlitModal';
import {
  Sparkles,
  Database,
  Sliders,
  History,
  Maximize2,
  Minimize2,
  Gift,
  Eye,
} from 'lucide-react';

const SETTINGS_STORAGE_KEY = 'alfamidi_lucky_draw_settings_v2';
const HISTORY_STORAGE_KEY = 'alfamidi_lucky_draw_history_v2';

const defaultCategories: PrizeCategory[] = [
  { id: 'cat-1', name: 'Grand Prize - Sepeda Motor Honda Beat', winnerCount: 1 },
  { id: 'cat-2', name: 'Hadiah Utama 1 - Smart TV 55 Inch & iPhone', winnerCount: 3 },
  { id: 'cat-3', name: 'Hadiah Utama 2 - Logam Mulia Emas 10 Gram', winnerCount: 5 },
  { id: 'cat-4', name: 'Hadiah Hiburan - Voucher Belanja Alfamidi Rp 1.000.000', winnerCount: 10 },
  { id: 'cat-5', name: 'Doorprize Akbar - Paket Elektronik Rumah Tangga', winnerCount: 20 },
];

export default function App() {
  // Candidate pool & metadata
  const [candidates, setCandidates] = useState<CandidateRecord[]>([]);
  const [columns, setColumns] = useState<ColumnMeta[]>([]);

  // Draw configuration (restored from LocalStorage so it never reverts to default)
  const [settings, setSettings] = useState<DrawSettings>(() => {
    try {
      const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && Array.isArray(parsed.categories) && parsed.categories.length > 0) {
          return parsed;
        }
      }
    } catch {
      // ignore
    }
    return {
      nameColumn: 'NAMA_KARYAWAN',
      useWeighting: false,
      weightColumn: 'POIN_UNDIAN',
      winnerCount: 1,
      groupName: defaultCategories[0].name,
      displayColumns: ['JABATAN', 'CABANG'],
      eventTitle: 'DOORPRIZE 18 TAHUN ALFAMIDI',
      allowDuplicateWinners: false,
      categories: defaultCategories,
    };
  });

  // Current draw session state
  const [isSpinning, setIsSpinning] = useState(false);
  const [recentWinners, setRecentWinners] = useState<WinnerItem[] | null>(null);

  // Last draw session reference for quick re-opening if accidentally closed
  const [lastDrawSession, setLastDrawSession] = useState<{
    winners: WinnerItem[];
    groupName: string;
    eventTitle: string;
    displayColumns: string[];
  } | null>(null);

  // Modals visibility
  const [showEnvelopeModal, setShowEnvelopeModal] = useState(false);
  const [showTableModal, setShowTableModal] = useState(false);
  const [showHistoryDrawer, setShowHistoryDrawer] = useState(false);
  const [showStreamlitModal, setShowStreamlitModal] = useState(false);

  // History & duplicate exclusion
  const [drawHistory, setDrawHistory] = useState<DrawHistoryEntry[]>(() => {
    try {
      const saved = localStorage.getItem(HISTORY_STORAGE_KEY);
      if (saved) return JSON.parse(saved);
    } catch {
      // ignore
    }
    return [];
  });

  const [alreadyWonIds, setAlreadyWonIds] = useState<Set<string>>(() => {
    try {
      const saved = localStorage.getItem(HISTORY_STORAGE_KEY);
      if (saved) {
        const history: DrawHistoryEntry[] = JSON.parse(saved);
        const ids = new Set<string>();
        history.forEach(h => h.winners.forEach(w => ids.add(w.id)));
        return ids;
      }
    } catch {
      // ignore
    }
    return new Set<string>();
  });

  // Active view tab for easy navigation
  const [activeTab, setActiveTab] = useState<'stage' | 'config' | 'data'>('stage');
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Save settings to LocalStorage whenever modified so it stays at the user's settings
  const handleUpdateSettings = (newSettings: DrawSettings) => {
    setSettings(newSettings);
    try {
      localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(newSettings));
    } catch {
      // ignore
    }
  };

  // Switch category on stage
  const handleSelectCategory = (categoryName: string) => {
    const selected = settings.categories?.find(c => c.name === categoryName);
    const newSettings: DrawSettings = {
      ...settings,
      groupName: categoryName,
      winnerCount: selected ? selected.winnerCount : settings.winnerCount,
    };
    handleUpdateSettings(newSettings);
  };

  // Update winner count on stage
  const handleUpdateWinnerCount = (count: number) => {
    const newSettings: DrawSettings = {
      ...settings,
      winnerCount: count,
    };
    handleUpdateSettings(newSettings);
  };

  // Initialize with realistic Alfamidi sample data on first launch
  useEffect(() => {
    const { headers, rows } = generateSampleAlfamidiData(1000);
    const recs = buildCandidateRecords(rows);
    const cols = analyzeColumns(headers, recs);
    const { nameCol, weightCol } = guessBestColumns(cols);

    setCandidates(recs);
    setColumns(cols);

    setSettings(prev => {
      const updated = {
        ...prev,
        nameColumn: prev.nameColumn || nameCol || 'NAMA_KARYAWAN',
        weightColumn: prev.weightColumn || weightCol || 'POIN_UNDIAN',
        displayColumns: prev.displayColumns.length > 0 ? prev.displayColumns : ['JABATAN', 'CABANG'],
      };
      return updated;
    });

    // Restore last session if history exists
    if (drawHistory.length > 0) {
      const latest = drawHistory[0];
      setLastDrawSession({
        winners: latest.winners,
        groupName: latest.groupName,
        eventTitle: latest.eventTitle,
        displayColumns: latest.displayColumns,
      });
      setRecentWinners(latest.winners);
    }
  }, []);

  // Save history to LocalStorage
  useEffect(() => {
    try {
      localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(drawHistory));
    } catch {
      // ignore
    }
  }, [drawHistory]);

  // Handle data load from file / sheet / manual
  const handleDataLoaded = (
    newCandidates: CandidateRecord[],
    newColumns: ColumnMeta[],
    nameCol: string,
    weightCol: string
  ) => {
    setCandidates(newCandidates);
    setColumns(newColumns);
    setRecentWinners(null);

    // Pick top 2 non-name columns as default displayColumns
    const defaultExtras = newColumns
      .filter(c => c.name !== nameCol)
      .slice(0, 2)
      .map(c => c.name);

    const nextSettings: DrawSettings = {
      ...settings,
      nameColumn: nameCol,
      weightColumn: weightCol || settings.weightColumn,
      displayColumns: defaultExtras.length > 0 ? defaultExtras : settings.displayColumns,
    };
    handleUpdateSettings(nextSettings);
  };

  // Trigger draw action when lever is pulled
  const handlePullLever = useCallback(() => {
    if (isSpinning || candidates.length === 0) return;

    // Execute draw algorithm immediately in memory
    const winners = drawWinners(candidates, settings, alreadyWonIds);
    if (winners.length === 0) {
      alert('Tidak ada peserta yang tersisa untuk diundi.');
      return;
    }

    setIsSpinning(true);
    setRecentWinners(null);

    const winnerCount = settings.winnerCount;
    const sessionData = {
      winners,
      groupName: settings.groupName,
      eventTitle: settings.eventTitle,
      displayColumns: settings.displayColumns,
    };

    if (winnerCount <= 3) {
      // Direct slot machine reveal for <= 3 winners
      setTimeout(() => {
        setIsSpinning(false);
        setRecentWinners(winners);
        setLastDrawSession(sessionData);

        // Record in history & mark as won
        const newHistoryEntry: DrawHistoryEntry = {
          id: `draw-${Date.now()}`,
          groupName: settings.groupName,
          eventTitle: settings.eventTitle,
          timestamp: new Date().toISOString(),
          winnerCount: winners.length,
          displayColumns: settings.displayColumns,
          winners,
        };
        setDrawHistory(prev => [newHistoryEntry, ...prev]);

        if (!settings.allowDuplicateWinners) {
          setAlreadyWonIds(prev => {
            const next = new Set(prev);
            winners.forEach(w => next.add(w.id));
            return next;
          });
        }
      }, 2600);
    } else if (winnerCount <= 10) {
      // Envelope Modal reveal for 4 - 10 winners
      setTimeout(() => {
        setIsSpinning(false);
        setRecentWinners(winners);
        setLastDrawSession(sessionData);
        setShowEnvelopeModal(true);

        const newHistoryEntry: DrawHistoryEntry = {
          id: `draw-${Date.now()}`,
          groupName: settings.groupName,
          eventTitle: settings.eventTitle,
          timestamp: new Date().toISOString(),
          winnerCount: winners.length,
          displayColumns: settings.displayColumns,
          winners,
        };
        setDrawHistory(prev => [newHistoryEntry, ...prev]);

        if (!settings.allowDuplicateWinners) {
          setAlreadyWonIds(prev => {
            const next = new Set(prev);
            winners.forEach(w => next.add(w.id));
            return next;
          });
        }
      }, 2200);
    } else {
      // Table Modal reveal for > 10 winners
      setTimeout(() => {
        setIsSpinning(false);
        setRecentWinners(winners);
        setLastDrawSession(sessionData);
        setShowTableModal(true);

        const newHistoryEntry: DrawHistoryEntry = {
          id: `draw-${Date.now()}`,
          groupName: settings.groupName,
          eventTitle: settings.eventTitle,
          timestamp: new Date().toISOString(),
          winnerCount: winners.length,
          displayColumns: settings.displayColumns,
          winners,
        };
        setDrawHistory(prev => [newHistoryEntry, ...prev]);

        if (!settings.allowDuplicateWinners) {
          setAlreadyWonIds(prev => {
            const next = new Set(prev);
            winners.forEach(w => next.add(w.id));
            return next;
          });
        }
      }, 2200);
    }
  }, [isSpinning, candidates, settings, alreadyWonIds]);

  const handleResetDraw = () => {
    setRecentWinners(null);
  };

  // Re-open last draw modal if user accidentally closed it
  const handleOpenLastResultModal = () => {
    if (!lastDrawSession || lastDrawSession.winners.length === 0) return;
    setRecentWinners(lastDrawSession.winners);

    if (lastDrawSession.winners.length <= 10) {
      setShowEnvelopeModal(true);
    } else {
      setShowTableModal(true);
    }
  };

  // Re-open modal from history drawer
  const handleOpenHistoryEntryModal = (entry: DrawHistoryEntry) => {
    setShowHistoryDrawer(false);
    setLastDrawSession({
      winners: entry.winners,
      groupName: entry.groupName,
      eventTitle: entry.eventTitle,
      displayColumns: entry.displayColumns,
    });
    setRecentWinners(entry.winners);

    if (entry.winners.length <= 10) {
      setShowEnvelopeModal(true);
    } else {
      setShowTableModal(true);
    }
  };

  const handleClearHistory = () => {
    if (window.confirm('Hapus seluruh riwayat undian dan reset status pemenang?')) {
      setDrawHistory([]);
      setAlreadyWonIds(new Set());
      setLastDrawSession(null);
      try {
        localStorage.removeItem(HISTORY_STORAGE_KEY);
      } catch {
        // ignore
      }
    }
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
        setIsFullscreen(false);
      }
    }
  };

  const remainingCandidatesCount = useMemo(() => {
    if (settings.allowDuplicateWinners) return candidates.length;
    return Math.max(0, candidates.length - alreadyWonIds.size);
  }, [candidates.length, alreadyWonIds.size, settings.allowDuplicateWinners]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-red-600 selection:text-white pb-12">
      {/* Top Corporate Alfamidi Header */}
      <header className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-red-600/40 px-3 sm:px-6 py-2.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
          {/* Brand Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 sm:w-10 sm:h-10 bg-red-600 rounded-xl flex items-center justify-center text-white font-black text-xl shadow-lg border border-red-400">
              A
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-white text-sm sm:text-base tracking-tight uppercase">
                  Alfamidi
                </span>
                <span className="text-[10px] text-amber-400 font-bold bg-amber-400/10 px-1.5 py-0.5 rounded border border-amber-400/20">
                  LUCKY DRAW
                </span>
              </div>
              <p className="text-[10px] sm:text-xs text-slate-400 truncate max-w-[200px] sm:max-w-none">
                PT MIDI UTAMA INDONESIA TBK • Sistem Undian Karyawan
              </p>
            </div>
          </div>

          {/* Navigation Pill Bar */}
          <div className="flex items-center gap-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab('stage')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                activeTab === 'stage'
                  ? 'bg-red-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Panggung Undian</span>
              <span className="sm:hidden">Undian</span>
            </button>
            <button
              onClick={() => setActiveTab('config')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                activeTab === 'config'
                  ? 'bg-red-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Sliders className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Pengaturan Undian</span>
              <span className="sm:hidden">Setting</span>
            </button>
            <button
              onClick={() => setActiveTab('data')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                activeTab === 'data'
                  ? 'bg-red-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Database className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Data Peserta</span>
              <span className="sm:hidden">Data</span>
            </button>
          </div>

          {/* Right Action Tools: History & Fullscreen */}
          <div className="flex items-center gap-2">
            {/* Quick button to reopen last draw modal if user closed it */}
            {lastDrawSession && (
              <button
                onClick={handleOpenLastResultModal}
                className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-bold transition-all cursor-pointer shadow-xs"
                title="Buka kembali modal hasil undian terakhir"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Modal Terakhir</span>
              </button>
            )}

            <button
              onClick={() => setShowHistoryDrawer(true)}
              className="relative p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors cursor-pointer flex items-center gap-1 text-xs font-medium"
              title="Lihat Riwayat Putaran Undian"
            >
              <History className="w-4 h-4 text-amber-400" />
              <span className="hidden md:inline">Riwayat</span>
              {drawHistory.length > 0 && (
                <span className="w-5 h-5 rounded-full bg-red-600 text-white text-[10px] font-black flex items-center justify-center">
                  {drawHistory.length}
                </span>
              )}
            </button>

            <button
              onClick={() => setShowStreamlitModal(true)}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700 transition-colors cursor-pointer flex items-center gap-1.5 text-xs font-bold"
              title="Deploy ke Streamlit (streamlit.py)"
            >
              <span className="font-mono text-amber-400">🐍</span>
              <span className="hidden sm:inline">Streamlit.py</span>
            </button>

            <button
              onClick={toggleFullscreen}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors cursor-pointer"
              title={isFullscreen ? 'Keluar Layar Penuh' : 'Mode Layar Penuh (Panggung)'}
            >
              {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 pt-4">
        {/* Quick Info Strip */}
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3 p-3 bg-slate-900/60 rounded-xl border border-slate-800/80 text-xs">
          <div className="flex items-center gap-3 flex-wrap">
            <div className="flex items-center gap-1.5 text-slate-300">
              <Gift className="w-4 h-4 text-amber-400" />
              <span>Hadiah Aktif: <strong className="text-white">{settings.groupName}</strong></span>
            </div>
            <span className="text-slate-600 hidden sm:inline">•</span>
            <div className="text-slate-300">
              Jumlah: <strong className="text-amber-400 font-mono">{settings.winnerCount} Pemenang</strong>
            </div>
            <span className="text-slate-600 hidden sm:inline">•</span>
            <div className="text-slate-300">
              Format: <span className="font-mono text-amber-300">[{settings.nameColumn} - {settings.displayColumns.filter(c => c !== settings.nameColumn).join(' - ')}]</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-400">Peserta Memenuhi Syarat:</span>
            <span className="px-2 py-0.5 rounded bg-red-600/20 text-red-400 border border-red-500/30 font-bold font-mono">
              {remainingCandidatesCount.toLocaleString('id-ID')} / {candidates.length.toLocaleString('id-ID')}
            </span>
          </div>
        </div>

        {/* View Tab 1: Stage (Slot Machine Arena) */}
        {activeTab === 'stage' && (
          <div className="space-y-4">
            {/* Slot Machine with Category Selection & View Last Modal buttons */}
            <SlotMachine
              candidates={candidates}
              settings={settings}
              isSpinning={isSpinning}
              onPullLever={handlePullLever}
              recentWinners={recentWinners}
              onResetDraw={handleResetDraw}
              onSelectCategory={handleSelectCategory}
              onUpdateWinnerCount={handleUpdateWinnerCount}
              onViewLastResultModal={handleOpenLastResultModal}
              hasLastResult={Boolean(lastDrawSession)}
              lastResultCount={lastDrawSession?.winners.length || 0}
            />
          </div>
        )}

        {/* View Tab 2: Parameter Configuration */}
        {activeTab === 'config' && (
          <div className="max-w-4xl mx-auto space-y-5">
            <DrawConfigPanel
              columns={columns}
              settings={settings}
              onUpdateSettings={handleUpdateSettings}
              poolCount={candidates.length}
              excludedCount={alreadyWonIds.size}
            />

            <div className="flex justify-end">
              <button
                onClick={() => setActiveTab('stage')}
                className="px-6 py-2.5 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white font-bold text-xs rounded-xl shadow-lg transition-transform hover:scale-105 active:scale-95 cursor-pointer flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                Simpan & Menuju Panggung Undian
              </button>
            </div>
          </div>
        )}

        {/* View Tab 3: Data Management & Source */}
        {activeTab === 'data' && (
          <div className="max-w-4xl mx-auto space-y-5">
            <DataImportSection
              candidates={candidates}
              columns={columns}
              onDataLoaded={handleDataLoaded}
            />
          </div>
        )}
      </main>

      {/* MODAL 1: Envelope Modal (for 4 to 10 winners, or re-opened modal) */}
      <EnvelopeModal
        isOpen={showEnvelopeModal}
        onClose={() => setShowEnvelopeModal(false)}
        winners={recentWinners || lastDrawSession?.winners || []}
        eventTitle={lastDrawSession?.eventTitle || settings.eventTitle}
        groupName={lastDrawSession?.groupName || settings.groupName}
        displayColumns={lastDrawSession?.displayColumns || settings.displayColumns}
      />

      {/* MODAL 2: Table Modal (for > 10 winners) */}
      <WinnersTableModal
        isOpen={showTableModal}
        onClose={() => setShowTableModal(false)}
        winners={recentWinners || lastDrawSession?.winners || []}
        eventTitle={lastDrawSession?.eventTitle || settings.eventTitle}
        groupName={lastDrawSession?.groupName || settings.groupName}
        displayColumns={lastDrawSession?.displayColumns || settings.displayColumns}
      />

      {/* DRAWER: History of All Draw Rounds */}
      <DrawHistoryDrawer
        isOpen={showHistoryDrawer}
        onClose={() => setShowHistoryDrawer(false)}
        history={drawHistory}
        onClearHistory={handleClearHistory}
        onOpenEntryModal={handleOpenHistoryEntryModal}
      />

      {/* MODAL 3: Streamlit deployment helper */}
      <StreamlitModal
        isOpen={showStreamlitModal}
        onClose={() => setShowStreamlitModal(false)}
      />
    </div>
  );
}
