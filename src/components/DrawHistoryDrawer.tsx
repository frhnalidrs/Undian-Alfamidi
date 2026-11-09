import React from 'react';
import { DrawHistoryEntry } from '../types';
import { exportWinnersToExcel, exportWinnersToPDF } from '../utils/exportUtils';
import {
  History,
  FileSpreadsheet,
  FileText,
  Trash2,
  X,
  Trophy,
  Eye,
} from 'lucide-react';

interface DrawHistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  history: DrawHistoryEntry[];
  onClearHistory: () => void;
  onOpenEntryModal?: (entry: DrawHistoryEntry) => void;
}

export const DrawHistoryDrawer: React.FC<DrawHistoryDrawerProps> = ({
  isOpen,
  onClose,
  history,
  onClearHistory,
  onOpenEntryModal,
}) => {
  if (!isOpen) return null;

  const totalWinnersAllRounds = history.reduce((sum, h) => sum + h.winners.length, 0);

  const handleExportAllExcel = () => {
    const allWinners = history.flatMap(h => h.winners);
    exportWinnersToExcel(allWinners, 'Semua_Putaran', 'SEMUA PEMENANG UNDIAN ALFAMIDI', [
      'JABATAN',
      'CABANG',
      'NIK',
    ]);
  };

  const handleExportAllPDF = () => {
    const allWinners = history.flatMap(h => h.winners);
    exportWinnersToPDF(allWinners, 'Semua_Putaran', 'SEMUA PEMENANG UNDIAN ALFAMIDI', [
      'JABATAN',
      'CABANG',
      'NIK',
    ]);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end bg-slate-950/70 backdrop-blur-xs">
      <div className="w-full max-w-lg h-full bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col animate-in slide-in-from-right duration-200">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-lg bg-red-600/20 text-red-500 flex items-center justify-center">
              <History className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base text-white">Riwayat Undian</h3>
              <p className="text-xs text-slate-400">
                {history.length} Putaran Selesai · {totalWinnersAllRounds} Total Pemenang
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Global Action Bar */}
        {history.length > 0 && (
          <div className="p-3 bg-slate-950/50 border-b border-slate-800 flex items-center justify-between gap-2">
            <span className="text-xs text-slate-400 font-medium">Ekspor Gabungan:</span>
            <div className="flex items-center gap-2">
              <button
                onClick={handleExportAllExcel}
                className="px-2.5 py-1.5 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <FileSpreadsheet className="w-3.5 h-3.5" />
                Semua Excel
              </button>
              <button
                onClick={handleExportAllPDF}
                className="px-2.5 py-1.5 rounded-lg bg-red-600/20 hover:bg-red-600/30 text-red-300 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <FileText className="w-3.5 h-3.5" />
                Semua PDF
              </button>
            </div>
          </div>
        )}

        {/* History List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {history.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500">
              <Trophy className="w-12 h-12 mb-3 stroke-[1.2] text-slate-600" />
              <p className="font-semibold text-sm text-slate-400">Belum Ada Putaran Undian</p>
              <p className="text-xs mt-1">
                Tarik tuas slot machine untuk memulai undian dan riwayat akan tercatat di sini.
              </p>
            </div>
          ) : (
            history.map((entry, idx) => (
              <div
                key={entry.id}
                className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2.5 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-red-400">
                      Putaran #{history.length - idx}
                    </span>
                    <h4 className="text-sm font-bold text-white leading-tight">
                      {entry.groupName}
                    </h4>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {new Date(entry.timestamp).toLocaleTimeString('id-ID', {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}{' '}
                      WIB · {entry.winners.length} Pemenang
                    </p>
                  </div>

                  <div className="flex items-center gap-1">
                    {onOpenEntryModal && (
                      <button
                        onClick={() => onOpenEntryModal(entry)}
                        title="Buka Modal Tampilan Hasil Ini"
                        className="p-1.5 rounded-md hover:bg-slate-800 text-amber-400 cursor-pointer"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() =>
                        exportWinnersToExcel(
                          entry.winners,
                          entry.groupName,
                          entry.eventTitle,
                          entry.displayColumns
                        )
                      }
                      title="Unduh Excel Putaran Ini"
                      className="p-1.5 rounded-md hover:bg-slate-800 text-emerald-400 cursor-pointer"
                    >
                      <FileSpreadsheet className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() =>
                        exportWinnersToPDF(
                          entry.winners,
                          entry.groupName,
                          entry.eventTitle,
                          entry.displayColumns
                        )
                      }
                      title="Cetak PDF Putaran Ini"
                      className="p-1.5 rounded-md hover:bg-slate-800 text-red-400 cursor-pointer"
                    >
                      <FileText className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Winners snippet */}
                <div className="space-y-1 pt-1 border-t border-slate-800/80">
                  {entry.winners.map((w, wIdx) => (
                    <div
                      key={w.id || wIdx}
                      className="text-xs text-slate-300 flex items-center justify-between"
                    >
                      <span className="truncate pr-2">
                        <strong className="text-slate-400 mr-1.5">#{w.rank}</strong>
                        {w.displayFormatted}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        {history.length > 0 && (
          <div className="p-3.5 border-t border-slate-800 bg-slate-950/70 flex items-center justify-between">
            <button
              onClick={onClearHistory}
              className="text-xs text-red-400 hover:text-red-300 flex items-center gap-1.5 cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5" />
              Reset Riwayat
            </button>
            <button
              onClick={onClose}
              className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white text-xs font-medium rounded-lg cursor-pointer transition-colors"
            >
              Tutup
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
