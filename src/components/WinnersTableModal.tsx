import React, { useState, useEffect, useMemo } from 'react';
import confetti from 'canvas-confetti';
import { WinnerItem } from '../types';
import { exportWinnersToExcel, exportWinnersToPDF } from '../utils/exportUtils';
import {
  FileSpreadsheet,
  FileText,
  X,
  Search,
  Trophy,
  Copy,
  Check,
  ChevronLeft,
  ChevronRight,
  Filter,
} from 'lucide-react';

interface WinnersTableModalProps {
  isOpen: boolean;
  onClose: () => void;
  winners: WinnerItem[];
  eventTitle: string;
  groupName: string;
  displayColumns: string[];
}

export const WinnersTableModal: React.FC<WinnersTableModalProps> = ({
  isOpen,
  onClose,
  winners,
  eventTitle,
  groupName,
  displayColumns,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [copied, setCopied] = useState(false);
  const [page, setPage] = useState(1);
  const pageSize = 15;

  useEffect(() => {
    if (isOpen) {
      setPage(1);
      setSearchTerm('');

      // Confetti burst for big draw!
      confetti({
        particleCount: 90,
        spread: 100,
        origin: { y: 0.4 },
        colors: ['#d71920', '#ffcc00', '#1e40af', '#ffffff'],
      });
    }
  }, [isOpen]);

  const filteredWinners = useMemo(() => {
    if (!searchTerm.trim()) return winners;
    const term = searchTerm.toLowerCase();
    return winners.filter(w => {
      if (w.name.toLowerCase().includes(term)) return true;
      if (w.displayFormatted.toLowerCase().includes(term)) return true;
      return Object.values(w.data).some(val =>
        String(val).toLowerCase().includes(term)
      );
    });
  }, [winners, searchTerm]);

  const totalPages = Math.max(1, Math.ceil(filteredWinners.length / pageSize));
  const paginatedWinners = useMemo(() => {
    const start = (page - 1) * pageSize;
    return filteredWinners.slice(start, start + pageSize);
  }, [filteredWinners, page, pageSize]);

  const handleCopyList = () => {
    const text = winners
      .map((w, idx) => `${idx + 1}. ${w.displayFormatted}`)
      .join('\n');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/85 backdrop-blur-md overflow-hidden">
      <div className="relative w-full max-w-5xl h-[92vh] flex flex-col bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Top Header Banner */}
        <div className="flex-shrink-0 bg-gradient-to-r from-red-700 via-red-600 to-red-800 p-4 sm:p-5 text-white flex items-center justify-between shadow-md">
          <div className="flex items-center gap-3 sm:gap-4">
            <div className="w-12 h-12 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center text-amber-300 shadow-inner">
              <Trophy className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-bold uppercase tracking-widest text-amber-300">
                  HASIL RESMI UNDIAN BESAR
                </span>
                <span className="text-white/40">·</span>
                <span className="text-[11px] font-bold text-white/90">
                  {winners.length} PEMENANG
                </span>
              </div>
              <h2 className="text-lg sm:text-2xl font-black tracking-tight text-white uppercase">
                {eventTitle || 'DOORPRIZE 18 TAHUN ALFAMIDI'}
              </h2>
              <p className="text-xs text-red-100 font-medium mt-0.5">
                Kategori: <strong className="text-white">{groupName || 'Hadiah Utama'}</strong>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-white/80 hover:text-white bg-white/10 hover:bg-white/20 rounded-full transition-colors cursor-pointer"
            title="Tutup"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Action Toolbar & Search */}
        <div className="flex-shrink-0 p-3 sm:p-4 bg-slate-800/80 border-b border-slate-700 flex flex-wrap items-center justify-between gap-3">
          {/* Search bar */}
          <div className="relative flex-1 min-w-[220px] max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Cari pemenang, NIK, jabatan, cabang..."
              value={searchTerm}
              onChange={e => {
                setSearchTerm(e.target.value);
                setPage(1);
              }}
              className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500"
            />
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyList}
              className="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-colors cursor-pointer"
              title="Salin semua pemenang ke papan klip"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Tersalin!' : 'Salin Teks'}
            </button>
            <button
              onClick={() => exportWinnersToExcel(winners, groupName, eventTitle, displayColumns)}
              className="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-colors cursor-pointer shadow-xs"
            >
              <FileSpreadsheet className="w-3.5 h-3.5" />
              Unduh Excel
            </button>
            <button
              onClick={() => exportWinnersToPDF(winners, groupName, eventTitle, displayColumns)}
              className="px-3 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-colors cursor-pointer shadow-xs"
            >
              <FileText className="w-3.5 h-3.5" />
              Cetak PDF
            </button>
          </div>
        </div>

        {/* Scrollable Table Area */}
        <div className="flex-1 overflow-y-auto">
          <table className="w-full text-left text-sm border-collapse">
            <thead className="sticky top-0 z-10 bg-slate-800 text-slate-300 text-xs uppercase tracking-wider font-semibold border-b border-slate-700 shadow-xs">
              <tr>
                <th className="py-3 px-4 w-14 text-center">No</th>
                <th className="py-3 px-4">Nama Pemenang</th>
                <th className="py-3 px-4">Format Pengumuman</th>
                {displayColumns.map(col => (
                  <th key={col} className="py-3 px-4">
                    {col}
                  </th>
                ))}
                <th className="py-3 px-4 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {paginatedWinners.length === 0 ? (
                <tr>
                  <td
                    colSpan={4 + displayColumns.length}
                    className="py-12 text-center text-slate-400 text-sm"
                  >
                    Tidak ditemukan pemenang yang sesuai dengan kata kunci pencarian.
                  </td>
                </tr>
              ) : (
                paginatedWinners.map((w, idx) => {
                  const absoluteIndex = (page - 1) * pageSize + idx + 1;
                  return (
                    <tr
                      key={w.id || idx}
                      className="hover:bg-slate-800/60 transition-colors group"
                    >
                      <td className="py-3 px-4 text-center font-mono text-xs text-slate-400 font-bold group-hover:text-amber-400">
                        {absoluteIndex}
                      </td>
                      <td className="py-3 px-4">
                        <div className="font-bold text-white text-sm">
                          {w.name}
                        </div>
                        {w.weightScore !== undefined && (
                          <div className="text-[11px] text-amber-400/90 font-mono">
                            Skor Poin: {w.weightScore}
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-4 text-slate-200 font-medium">
                        <span className="inline-block px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-xs">
                          {w.displayFormatted}
                        </span>
                      </td>
                      {displayColumns.map(col => (
                        <td key={col} className="py-3 px-4 text-slate-300 text-xs">
                          {String(w.data[col] ?? '-')}
                        </td>
                      ))}
                      <td className="py-3 px-4 text-right">
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-400">
                          <Check className="w-3 h-3" /> Terpilih
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Footer Pagination */}
        <div className="flex-shrink-0 p-3 sm:p-4 bg-slate-800/90 border-t border-slate-700 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400">
          <div>
            Menampilkan{' '}
            <strong className="text-slate-200">
              {filteredWinners.length > 0 ? (page - 1) * pageSize + 1 : 0}
            </strong>{' '}
            -{' '}
            <strong className="text-slate-200">
              {Math.min(page * pageSize, filteredWinners.length)}
            </strong>{' '}
            dari <strong className="text-slate-200">{filteredWinners.length}</strong> pemenang
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="p-1.5 rounded bg-slate-700 text-slate-200 hover:bg-slate-600 disabled:opacity-30 disabled:pointer-events-none transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-slate-200 font-semibold px-2">
              Halaman {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="p-1.5 rounded bg-slate-700 text-slate-200 hover:bg-slate-600 disabled:opacity-30 disabled:pointer-events-none transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>

            <button
              onClick={onClose}
              className="ml-3 px-4 py-1.5 bg-slate-700 hover:bg-slate-600 text-white font-medium rounded-lg transition-colors cursor-pointer"
            >
              Tutup
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
