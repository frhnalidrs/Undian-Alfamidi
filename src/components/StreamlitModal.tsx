import React, { useState } from 'react';
import { X, Copy, Check, Download, Terminal, FileCode } from 'lucide-react';

interface StreamlitModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const StreamlitModal: React.FC<StreamlitModalProps> = ({ isOpen, onClose }) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleDownload = () => {
    // Fetch and download streamlit.py
    fetch('/streamlit.py')
      .then(res => res.text())
      .then(text => {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'streamlit.py';
        a.click();
        URL.revokeObjectURL(url);
      })
      .catch(() => {
        alert('File streamlit.py tersedia di root direktori project.');
      });
  };

  const handleCopyCmd = () => {
    navigator.clipboard.writeText('pip install streamlit pandas openpyxl requests numpy\nstreamlit run streamlit.py');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl p-5 sm:p-6 text-slate-100 flex flex-col space-y-4 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-xl bg-red-600/20 text-red-400 flex items-center justify-center border border-red-500/30">
              <FileCode className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-extrabold text-base text-white">Streamlit Deployment (streamlit.py)</h3>
              <p className="text-xs text-slate-400">File <code className="text-amber-400">streamlit.py</code> dan <code className="text-amber-400">requirements.txt</code> telah dibuat</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3 text-xs text-slate-300">
          <p>
            Aplikasi <strong>Alfamidi Lucky Draw</strong> sudah dikonversi secara utuh ke dalam bahasa <strong>Python Streamlit</strong> (<code className="text-amber-300">streamlit.py</code>) dengan seluruh fitur lengkap:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li>Dukungan puluhan ribu peserta via Excel, CSV, Google Spreadsheet, teks manual, & data generator.</li>
            <li>Pengaturan Kategori Hadiah massal (bulk) & dropdown di panggung.</li>
            <li>Tombol Merah arcade untuk memutar undian dengan algoritma matematis <em>A-Res Weighted Sampling</em>.</li>
            <li>Tampilan sesuai jumlah pemenang: $\le 3$ pemenang di slot machine, $4-10$ pemenang via amplop surat vintage resmi PT Midi Utama Indonesia Tbk, dan &gt;10 pemenang via tabel interaktif.</li>
            <li>Fitur ekspor laporan langsung ke Excel (.xlsx).</li>
          </ul>

          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[11px] text-amber-400 font-bold flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5" />
                Cara Menjalankan:
              </span>
              <button
                onClick={handleCopyCmd}
                className="text-[11px] px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center gap-1 cursor-pointer"
              >
                {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                {copied ? 'Tersalin' : 'Salin Perintah'}
              </button>
            </div>
            <pre className="font-mono text-xs text-emerald-300 bg-black/60 p-2.5 rounded-lg overflow-x-auto">
pip install -r requirements.txt{'\n'}
streamlit run streamlit.py
            </pre>
          </div>
        </div>

        <div className="flex items-center justify-end gap-2.5 pt-2 border-t border-slate-800">
          <button
            onClick={handleDownload}
            className="px-4 py-2 bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white font-bold text-xs rounded-xl flex items-center gap-1.5 shadow-md cursor-pointer transition-all"
          >
            <Download className="w-3.5 h-3.5" />
            Unduh streamlit.py
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl cursor-pointer transition-colors"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
};
