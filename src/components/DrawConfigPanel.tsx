import React, { useState } from 'react';
import { ColumnMeta, DrawSettings, PrizeCategory } from '../types';
import {
  SlidersHorizontal,
  Award,
  Eye,
  CheckSquare,
  Square,
  ShieldCheck,
  TrendingUp,
  Mail,
  Grid,
  ListPlus,
  Trash2,
  Check,
} from 'lucide-react';

interface DrawConfigPanelProps {
  columns: ColumnMeta[];
  settings: DrawSettings;
  onUpdateSettings: (newSettings: DrawSettings) => void;
  poolCount: number;
  excludedCount: number;
}

export const DrawConfigPanel: React.FC<DrawConfigPanelProps> = ({
  columns,
  settings,
  onUpdateSettings,
  poolCount,
  excludedCount,
}) => {
  // Bulk text state for category entry
  const [bulkText, setBulkText] = useState(() =>
    (settings.categories || [])
      .map(c => `${c.name} | ${c.winnerCount}`)
      .join('\n')
  );
  const [bulkSaved, setBulkSaved] = useState(false);

  const handleToggleDisplayColumn = (colName: string) => {
    let nextCols = [...settings.displayColumns];
    if (nextCols.includes(colName)) {
      nextCols = nextCols.filter(c => c !== colName);
    } else {
      nextCols.push(colName);
    }
    onUpdateSettings({ ...settings, displayColumns: nextCols });
  };

  const samplePreviewString = () => {
    const parts = [settings.nameColumn || 'NAMA_KARYAWAN'];
    settings.displayColumns.forEach(c => {
      if (c !== settings.nameColumn) parts.push(c);
    });
    return parts.join(' - ');
  };

  // Concise animation indicator per user instruction
  const getAnimationNotice = (count: number) => {
    if (count <= 3) {
      return {
        badge: '🎰 Slot Machine',
        color: 'text-amber-400 bg-amber-950/60 border-amber-500/40',
        icon: Award,
      };
    } else if (count <= 10) {
      return {
        badge: '✉️ Animasi Surat',
        color: 'text-red-400 bg-red-950/60 border-red-500/40',
        icon: Mail,
      };
    } else {
      return {
        badge: '📊 Tabel Pemenang Komprehensif',
        color: 'text-blue-400 bg-blue-950/60 border-blue-500/40',
        icon: Grid,
      };
    }
  };

  const notice = getAnimationNotice(settings.winnerCount);
  const NoticeIcon = notice.icon;

  // Save bulk categories and persist
  const handleSaveBulkCategories = () => {
    const lines = bulkText.split('\n').map(l => l.trim()).filter(Boolean);
    const newCategories: PrizeCategory[] = [];

    lines.forEach((line, idx) => {
      if (line.includes('|')) {
        const [namePart, countPart] = line.split('|');
        const name = namePart.trim();
        const cnt = parseInt(countPart.trim()) || 1;
        if (name) {
          newCategories.push({ id: `cat-${Date.now()}-${idx}`, name, winnerCount: cnt });
        }
      } else {
        if (line) {
          newCategories.push({ id: `cat-${Date.now()}-${idx}`, name: line, winnerCount: 1 });
        }
      }
    });

    if (newCategories.length === 0) {
      newCategories.push({
        id: 'cat-default',
        name: 'Grand Prize - Sepeda Motor Honda Beat',
        winnerCount: 1,
      });
    }

    // Keep active groupName if it exists in new categories, otherwise pick first
    const match = newCategories.find(c => c.name === settings.groupName);
    const activeGroup = match ? match.name : newCategories[0].name;
    const activeCount = match ? match.winnerCount : newCategories[0].winnerCount;

    onUpdateSettings({
      ...settings,
      categories: newCategories,
      groupName: activeGroup,
      winnerCount: activeCount || settings.winnerCount,
    });

    setBulkSaved(true);
    setTimeout(() => setBulkSaved(false), 2500);
  };

  const handleDeleteCategory = (catId: string) => {
    const remaining = settings.categories.filter(c => c.id !== catId);
    if (remaining.length === 0) return;
    const nextGroup = remaining.some(c => c.name === settings.groupName)
      ? settings.groupName
      : remaining[0].name;
    onUpdateSettings({
      ...settings,
      categories: remaining,
      groupName: nextGroup,
    });
    setBulkText(remaining.map(c => `${c.name} | ${c.winnerCount}`).join('\n'));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 shadow-xl space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
          <SlidersHorizontal className="w-5 h-5 text-amber-400" />
          Pengaturan Parameter Undian
        </h2>
        <span className="text-xs text-slate-400">
          Tersedia: <strong className="text-white">{(poolCount - (settings.allowDuplicateWinners ? 0 : excludedCount)).toLocaleString('id-ID')}</strong> peserta
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6">
        {/* Left Column: Event Title, Bulk Categories, Column Selection */}
        <div className="space-y-4">
          {/* Judul Acara / Event */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
              Judul Acara / Header Undian
            </label>
            <input
              type="text"
              value={settings.eventTitle}
              onChange={e => onUpdateSettings({ ...settings, eventTitle: e.target.value })}
              placeholder="DOORPRIZE 18 TAHUN ALFAMIDI"
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:border-red-500"
            />
          </div>

          {/* BULK Kategori / Grup Hadiah Management */}
          <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                <ListPlus className="w-4 h-4 text-amber-400" />
                Daftar Kategori / Grup Hadiah (Bulk)
              </label>
              <span className="text-[10px] text-slate-400 font-mono">
                {settings.categories?.length || 0} Kategori Aktif
              </span>
            </div>

            <p className="text-[11px] text-slate-400">
              Ketik banyak kategori sekaligus (1 baris per kategori). Format: <span className="text-amber-300">Nama Hadiah | Jumlah Pemenang</span>
            </p>

            <textarea
              rows={5}
              value={bulkText}
              onChange={e => setBulkText(e.target.value)}
              placeholder="Grand Prize - Sepeda Motor Honda Beat | 1&#10;Hadiah Utama 1 - Smart TV 55 Inch | 3&#10;Hadiah Utama 2 - Logam Mulia Emas 10 Gram | 5&#10;Hadiah Hiburan - Voucher Belanja Alfamidi Rp 1.000.000 | 10"
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 font-mono text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-red-500"
            />

            <div className="flex items-center justify-between pt-1">
              <span className="text-[10px] text-slate-400 italic">
                * Pemilihan kategori undian dilakukan di Panggung Undian
              </span>
              <button
                type="button"
                onClick={handleSaveBulkCategories}
                className="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-600 text-slate-950 text-xs font-bold rounded-lg transition-colors cursor-pointer flex items-center gap-1.5 shadow-sm"
              >
                {bulkSaved ? <Check className="w-3.5 h-3.5 text-slate-950" /> : <ListPlus className="w-3.5 h-3.5" />}
                {bulkSaved ? 'Tersimpan!' : 'Terapkan Kategori'}
              </button>
            </div>

            {/* Configured categories list chip view */}
            <div className="pt-2 border-t border-slate-800 space-y-1.5 max-h-36 overflow-y-auto pr-1">
              {settings.categories?.map((cat) => (
                <div
                  key={cat.id}
                  className="flex items-center justify-between p-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-200"
                >
                  <div className="flex items-center gap-2 truncate pr-2">
                    <span className="font-semibold text-white truncate">{cat.name}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold flex-shrink-0">
                      {cat.winnerCount} pemenang
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleDeleteCategory(cat.id)}
                    className="text-slate-500 hover:text-red-400 p-1 rounded transition-colors cursor-pointer"
                    title="Hapus Kategori"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Kolom Identitas / Nama Pemenang */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
              Kolom Utama / Nama yang Diundi
            </label>
            <select
              value={settings.nameColumn}
              onChange={e => onUpdateSettings({ ...settings, nameColumn: e.target.value })}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-white focus:outline-none focus:border-red-500 cursor-pointer"
            >
              {columns.map(col => (
                <option key={col.name} value={col.name}>
                  {col.name} {col.sampleValues[0] ? `(misal: ${col.sampleValues[0]})` : ''}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Right Column: Weighting & Display Columns & Animation Notice */}
        <div className="space-y-4">
          {/* Jumlah Pemenang & Concise Animation Badge */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Jumlah Pemenang Default
              </label>
              <span className="text-xs font-mono font-bold text-amber-400">
                {settings.winnerCount} Orang
              </span>
            </div>

            <div className="flex items-center gap-2 mb-2.5">
              <input
                type="number"
                min={1}
                max={Math.max(1, poolCount)}
                value={settings.winnerCount}
                onChange={e =>
                  onUpdateSettings({
                    ...settings,
                    winnerCount: Math.max(1, parseInt(e.target.value) || 1),
                  })
                }
                className="w-24 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white font-mono text-center focus:outline-none focus:border-red-500"
              />

              {/* Quick count chips */}
              <div className="flex flex-wrap gap-1">
                {[1, 3, 5, 10, 20, 50, 100].map(cnt => (
                  <button
                    key={cnt}
                    type="button"
                    onClick={() => onUpdateSettings({ ...settings, winnerCount: cnt })}
                    className={`px-2.5 py-1.5 text-xs font-bold rounded-lg transition-colors cursor-pointer ${
                      settings.winnerCount === cnt
                        ? 'bg-red-600 text-white shadow-xs'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    {cnt}
                  </button>
                ))}
              </div>
            </div>

            {/* Concise Animation Indicator: Just Title without redundant text */}
            <div className={`p-2.5 rounded-xl border flex items-center gap-2 text-xs font-bold ${notice.color}`}>
              <NoticeIcon className="w-4 h-4 flex-shrink-0" />
              <span>{notice.badge}</span>
            </div>
          </div>

          {/* Weighted Probability Configuration */}
          <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-amber-400" />
                <span className="text-xs font-bold text-white uppercase tracking-wider">
                  Bobot Persentase Kemenangan
                </span>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.useWeighting}
                  onChange={e => onUpdateSettings({ ...settings, useWeighting: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-9 h-5 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-amber-500" />
              </label>
            </div>

            <p className="text-[11px] text-slate-400 mb-3">
              Makin besar poin/skor kandidat, makin tinggi peluang menang (Weighted Random Sampling).
            </p>

            {settings.useWeighting && (
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <label className="block text-[11px] font-bold text-amber-300 uppercase">
                  Pilih Kolom Penentu Bobot / Poin:
                </label>
                <select
                  value={settings.weightColumn}
                  onChange={e => onUpdateSettings({ ...settings, weightColumn: e.target.value })}
                  className="w-full bg-slate-900 border border-amber-500/50 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-400 cursor-pointer"
                >
                  {columns.map(col => (
                    <option key={col.name} value={col.name}>
                      {col.name} {col.isNumeric ? '⭐ (Kolom Angka Terdeteksi)' : ''}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* Kolom Tampilan Tambahan (NAMA - JABATAN - CABANG, etc.) */}
          <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Eye className="w-4 h-4 text-red-500" />
                Kolom Ditampilkan Selain Nama
              </label>
              <span className="text-[10px] text-slate-400 font-mono">
                {settings.displayColumns.length} terpilih
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto pr-1">
              {columns.map(col => {
                const isSelected = settings.displayColumns.includes(col.name);
                const isPrimary = col.name === settings.nameColumn;

                return (
                  <button
                    key={col.name}
                    type="button"
                    onClick={() => handleToggleDisplayColumn(col.name)}
                    className={`flex items-center gap-2 p-2 rounded-lg text-left text-xs transition-colors cursor-pointer border ${
                      isSelected
                        ? 'bg-red-950/60 border-red-500/60 text-white font-semibold'
                        : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {isSelected ? (
                      <CheckSquare className="w-3.5 h-3.5 text-red-400 flex-shrink-0" />
                    ) : (
                      <Square className="w-3.5 h-3.5 text-slate-600 flex-shrink-0" />
                    )}
                    <span className="truncate">
                      {col.name} {isPrimary ? '(Nama)' : ''}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Live Format String Preview */}
            <div className="pt-2 border-t border-slate-800">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-1">
                Contoh Format Keluaran:
              </span>
              <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 font-mono text-xs text-amber-300 font-bold truncate">
                {samplePreviewString()}
              </div>
            </div>
          </div>

          {/* Duplicate Winner Prevention Option */}
          <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/50 border border-slate-800">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <div>
                <span className="text-xs font-bold text-white block">
                  Kunci Pemenang (Cegah Menang 2x)
                </span>
                <span className="text-[10px] text-slate-400">
                  Karyawan yang sudah menang otomatis tidak diundi lagi di putaran berikutnya.
                </span>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={!settings.allowDuplicateWinners}
                onChange={e =>
                  onUpdateSettings({ ...settings, allowDuplicateWinners: !e.target.checked })
                }
                className="sr-only peer"
              />
              <div className="w-9 h-5 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-emerald-600" />
            </label>
          </div>
        </div>
      </div>
    </div>
  );
};
