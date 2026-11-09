import React, { useState } from 'react';
import {
  parseCSV,
  parseExcel,
  fetchGoogleSheet,
  buildCandidateRecords,
  analyzeColumns,
  guessBestColumns,
  generateSampleAlfamidiData,
} from '../utils/dataParser';
import { CandidateRecord, ColumnMeta } from '../types';
import {
  FileSpreadsheet,
  UploadCloud,
  FileText,
  Link2,
  Database,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Layers,
} from 'lucide-react';

interface DataImportSectionProps {
  candidates: CandidateRecord[];
  columns: ColumnMeta[];
  onDataLoaded: (
    candidates: CandidateRecord[],
    columns: ColumnMeta[],
    nameCol: string,
    weightCol: string
  ) => void;
}

export const DataImportSection: React.FC<DataImportSectionProps> = ({
  candidates,
  columns,
  onDataLoaded,
}) => {
  const [activeTab, setActiveTab] = useState<'excel' | 'csv' | 'gsheet' | 'manual' | 'sample'>('sample');
  const [googleSheetUrl, setGoogleSheetUrl] = useState('');
  const [manualText, setManualText] = useState(
    'NIK,NAMA_KARYAWAN,JABATAN,CABANG,POIN_KINERJA\n' +
    'MIDI-202401,Budi Santoso,Store Leader,Makassar,150\n' +
    'MIDI-202402,Siti Nurhaliza,Cashier Staff,Bekasi,90\n' +
    'MIDI-202403,Ahmad Pratama,Store Crew,Tangerang,120\n' +
    'MIDI-202404,Dewi Lestari,Assistant Store Leader,Medan,110\n' +
    'MIDI-202405,Eko Wijaya,Store Crew,Manado,85\n' +
    'MIDI-202406,Rina Anggraini,Cashier Staff,Bogor,95\n' +
    'MIDI-202407,Bambang Hidayat,Warehouse Staff,Samarinda,100\n' +
    'MIDI-202408,Fitri Wulandari,Store Crew,Yogyakarta,130'
  );
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const processImportedData = (headers: string[], rows: Record<string, string | number>[]) => {
    if (rows.length === 0) {
      throw new Error('Data kosong atau tidak memiliki baris data yang valid.');
    }
    const recs = buildCandidateRecords(rows);
    const cols = analyzeColumns(headers, recs);
    const { nameCol, weightCol } = guessBestColumns(cols);

    onDataLoaded(recs, cols, nameCol, weightCol);
    setSuccessMessage(`Berhasil memuat ${recs.length.toLocaleString('id-ID')} entri peserta dengan ${cols.length} kolom terdeteksi!`);
    setErrorMessage(null);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>, type: 'csv' | 'excel') => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      if (type === 'excel') {
        const { headers, rows } = await parseExcel(file);
        processImportedData(headers, rows);
      } else {
        const text = await file.text();
        const { headers, rows } = parseCSV(text);
        processImportedData(headers, rows);
      }
    } catch (err: unknown) {
      setErrorMessage((err as Error)?.message || 'Gagal memproses file. Pastikan format valid.');
    } finally {
      setIsLoading(false);
      // Reset input value
      e.target.value = '';
    }
  };

  const handleFetchGoogleSheet = async () => {
    if (!googleSheetUrl.trim()) {
      setErrorMessage('Masukkan tautan Google Spreadsheet terlebih dahulu.');
      return;
    }
    setIsLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const { headers, rows } = await fetchGoogleSheet(googleSheetUrl);
      processImportedData(headers, rows);
    } catch (err: unknown) {
      setErrorMessage(
        (err as Error)?.message ||
          'Gagal mengambil Google Spreadsheet. Pastikan akses tautan diatur ke "Siapa saja yang memiliki link dapat melihat" (Public View).'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleProcessManual = () => {
    setIsLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const { headers, rows } = parseCSV(manualText);
      processImportedData(headers, rows);
    } catch (err: unknown) {
      setErrorMessage((err as Error)?.message || 'Format teks manual tidak valid.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadSample = (count: number) => {
    setIsLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    // Use setTimeout so the UI updates with loading state for large datasets
    setTimeout(() => {
      try {
        const { headers, rows } = generateSampleAlfamidiData(count);
        processImportedData(headers, rows);
      } catch (err: unknown) {
        setErrorMessage((err as Error)?.message || 'Gagal membuat sampel data.');
      } finally {
        setIsLoading(false);
      }
    }, 50);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 shadow-xl">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-5 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-red-500" />
            Sumber Data Peserta Undian
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Dukung puluhan ribu entri via Google Spreadsheet, file Excel, CSV, atau ketik manual.
          </p>
        </div>

        {candidates.length > 0 && (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-950/60 border border-emerald-600/40 text-emerald-400 text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>{candidates.length.toLocaleString('id-ID')} Peserta Aktif</span>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-1.5 p-1 bg-slate-950/80 rounded-xl mb-5 border border-slate-800">
        <button
          onClick={() => setActiveTab('sample')}
          className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'sample'
              ? 'bg-red-600 text-white shadow-md'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5 text-amber-300" />
          Sampel Alfamidi
        </button>
        <button
          onClick={() => setActiveTab('excel')}
          className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'excel'
              ? 'bg-red-600 text-white shadow-md'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <FileSpreadsheet className="w-3.5 h-3.5" />
          Upload Excel (.xlsx)
        </button>
        <button
          onClick={() => setActiveTab('csv')}
          className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'csv'
              ? 'bg-red-600 text-white shadow-md'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          Upload CSV
        </button>
        <button
          onClick={() => setActiveTab('gsheet')}
          className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'gsheet'
              ? 'bg-red-600 text-white shadow-md'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Link2 className="w-3.5 h-3.5" />
          Google Spreadsheet
        </button>
        <button
          onClick={() => setActiveTab('manual')}
          className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeTab === 'manual'
              ? 'bg-red-600 text-white shadow-md'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          Ketik Manual
        </button>
      </div>

      {/* Tab Panels */}
      <div className="space-y-4">
        {/* Sample Alfamidi Datasets */}
        {activeTab === 'sample' && (
          <div className="bg-slate-950/60 p-4 sm:p-5 rounded-xl border border-slate-800/80">
            <h3 className="text-sm font-bold text-white mb-1">
              Data Demo Karyawan Alfamidi (Siap Pakai)
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Gunakan data simulasi resmi lengkap dengan NIK, Nama Karyawan, Jabatan (Store Crew, Cashier, Store Leader, BM), Cabang se-Indonesia, dan Poin Kinerja untuk pengujian instan.
            </p>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => handleLoadSample(1000)}
                disabled={isLoading}
                className="px-4 py-2.5 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white text-xs font-bold rounded-xl transition-all cursor-pointer shadow-md disabled:opacity-50"
              >
                Muat 1.000 Karyawan Alfamidi
              </button>
              <button
                onClick={() => handleLoadSample(10000)}
                disabled={isLoading}
                className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-bold rounded-xl border border-amber-500/30 transition-all cursor-pointer shadow-sm disabled:opacity-50"
              >
                Muat 10.000 Karyawan (Uji Skala Menengah)
              </button>
              <button
                onClick={() => handleLoadSample(25000)}
                disabled={isLoading}
                className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-bold rounded-xl border border-emerald-500/30 transition-all cursor-pointer shadow-sm disabled:opacity-50"
              >
                Muat 25.000 Karyawan (Skala Akbar & Super Cepat)
              </button>
            </div>
          </div>
        )}

        {/* Upload Excel */}
        {activeTab === 'excel' && (
          <div className="border-2 border-dashed border-slate-700 hover:border-red-500/80 rounded-xl p-6 text-center transition-colors bg-slate-950/40">
            <FileSpreadsheet className="w-10 h-10 text-emerald-400 mx-auto mb-2" />
            <p className="text-sm font-bold text-white">Pilih File Excel (.xlsx, .xls)</p>
            <p className="text-xs text-slate-400 mt-1">
              Kolom baris pertama akan otomatis dideteksi sebagai judul kolom.
            </p>
            <label className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl cursor-pointer transition-colors shadow-sm">
              <UploadCloud className="w-4 h-4" />
              Pilih Berkas Excel
              <input
                type="file"
                accept=".xlsx, .xls"
                className="hidden"
                onChange={e => handleFileUpload(e, 'excel')}
              />
            </label>
          </div>
        )}

        {/* Upload CSV */}
        {activeTab === 'csv' && (
          <div className="border-2 border-dashed border-slate-700 hover:border-red-500/80 rounded-xl p-6 text-center transition-colors bg-slate-950/40">
            <FileText className="w-10 h-10 text-blue-400 mx-auto mb-2" />
            <p className="text-sm font-bold text-white">Pilih File CSV (.csv)</p>
            <p className="text-xs text-slate-400 mt-1">
              Mendukung pemisah koma (,), titik koma (;), atau tab (\t).
            </p>
            <label className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl cursor-pointer transition-colors shadow-sm">
              <UploadCloud className="w-4 h-4" />
              Pilih Berkas CSV
              <input
                type="file"
                accept=".csv, text/csv"
                className="hidden"
                onChange={e => handleFileUpload(e, 'csv')}
              />
            </label>
          </div>
        )}

        {/* Google Spreadsheet Link */}
        {activeTab === 'gsheet' && (
          <div className="bg-slate-950/60 p-4 sm:p-5 rounded-xl border border-slate-800/80 space-y-3">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
                Tautan Google Spreadsheet
              </label>
              <div className="flex gap-2">
                <input
                  type="url"
                  placeholder="https://docs.google.com/spreadsheets/d/.../edit"
                  value={googleSheetUrl}
                  onChange={e => setGoogleSheetUrl(e.target.value)}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-red-500"
                />
                <button
                  onClick={handleFetchGoogleSheet}
                  disabled={isLoading}
                  className="px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl transition-colors cursor-pointer shadow-sm disabled:opacity-50 flex items-center gap-1.5"
                >
                  <Link2 className="w-4 h-4" />
                  {isLoading ? 'Mengambil...' : 'Tarik Data'}
                </button>
              </div>
            </div>
            <p className="text-[11px] text-slate-400">
              💡 <strong>Tips:</strong> Pastikan spreadsheet Google Anda disetel ke{' '}
              <span className="text-amber-300">"Anyone with the link can view" (Publik)</span>{' '}
              agar sistem undian dapat membaca entri secara langsung tanpa login berulang.
            </p>
          </div>
        )}

        {/* Manual Text Input */}
        {activeTab === 'manual' && (
          <div className="bg-slate-950/60 p-4 sm:p-5 rounded-xl border border-slate-800/80 space-y-3">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">
                Ketik atau Tempel Data Manual
              </label>
              <p className="text-[11px] text-slate-400 mb-2">
                Format: <strong>koma (,)</strong> untuk memisahkan kolom, dan <strong>ENTER</strong> untuk baris baru.
                Baris pertama adalah judul kolom.
              </p>
              <textarea
                rows={6}
                value={manualText}
                onChange={e => setManualText(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 font-mono text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-red-500"
              />
            </div>
            <div className="flex justify-end">
              <button
                onClick={handleProcessManual}
                disabled={isLoading}
                className="px-5 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl transition-colors cursor-pointer shadow-sm disabled:opacity-50"
              >
                {isLoading ? 'Memproses...' : 'Terapkan Data Manual'}
              </button>
            </div>
          </div>
        )}

        {/* Alerts */}
        {errorMessage && (
          <div className="p-3 bg-red-950/70 border border-red-700/60 rounded-xl flex items-start gap-2.5 text-red-200 text-xs">
            <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        {successMessage && (
          <div className="p-3 bg-emerald-950/70 border border-emerald-700/60 rounded-xl flex items-start gap-2.5 text-emerald-200 text-xs">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
            <span>{successMessage}</span>
          </div>
        )}

        {/* Quick Data Preview Table if loaded */}
        {candidates.length > 0 && (
          <div className="mt-4 pt-4 border-t border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-300">
                Pratinjau Data Masuk (5 Baris Pertama):
              </span>
              <span className="text-[11px] text-slate-400">
                {columns.length} Kolom Terdeteksi: {columns.map(c => c.name).join(', ')}
              </span>
            </div>

            <div className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-950/80">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-slate-800 text-slate-300 font-semibold border-b border-slate-700">
                  <tr>
                    <th className="py-2 px-3 w-10 text-center">#</th>
                    {columns.map(col => (
                      <th key={col.name} className="py-2 px-3 whitespace-nowrap">
                        {col.name}
                        {col.isNumeric && (
                          <span className="ml-1 text-[10px] text-amber-400 font-normal">
                            (angka)
                          </span>
                        )}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {candidates.slice(0, 5).map((cand, idx) => (
                    <tr key={cand._id || idx} className="hover:bg-slate-800/40">
                      <td className="py-2 px-3 text-center text-slate-500 font-mono">
                        {idx + 1}
                      </td>
                      {columns.map(col => (
                        <td key={col.name} className="py-2 px-3 text-slate-300 whitespace-nowrap">
                          {String(cand[col.name] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
