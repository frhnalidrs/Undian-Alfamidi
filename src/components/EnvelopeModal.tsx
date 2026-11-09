import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { WinnerItem } from '../types';
import { soundEffects } from '../utils/soundEffects';
import { exportWinnersToExcel, exportWinnersToPDF } from '../utils/exportUtils';
import { FileSpreadsheet, FileText, X, Sparkles, CheckCircle2 } from 'lucide-react';

interface EnvelopeModalProps {
  isOpen: boolean;
  onClose: () => void;
  winners: WinnerItem[];
  eventTitle: string;
  groupName: string;
  displayColumns: string[];
}

export const EnvelopeModal: React.FC<EnvelopeModalProps> = ({
  isOpen,
  onClose,
  winners,
  eventTitle,
  groupName,
  displayColumns,
}) => {
  // Animation stages: 'sliding-up' -> 'opened-flap' -> 'letter-emerged'
  const [animStage, setAnimStage] = useState<'idle' | 'sliding' | 'opening' | 'emerged'>('idle');

  useEffect(() => {
    if (!isOpen) {
      setAnimStage('idle');
      return;
    }

    // Trigger sliding animation
    setAnimStage('sliding');
    soundEffects.playWhoosh();

    const openTimer = setTimeout(() => {
      setAnimStage('opening');
    }, 900);

    const emergeTimer = setTimeout(() => {
      setAnimStage('emerged');
      soundEffects.playFanfare();

      // Launch celebration confetti
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#d71920', '#ffcc00', '#1e40af', '#ffffff'],
      });

      const secondBlast = setTimeout(() => {
        confetti({
          particleCount: 50,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: ['#d71920', '#ffcc00', '#ffffff'],
        });
        confetti({
          particleCount: 50,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors: ['#1e40af', '#ffcc00', '#ffffff'],
        });
      }, 350);

      return () => clearTimeout(secondBlast);
    }, 1800);

    return () => {
      clearTimeout(openTimer);
      clearTimeout(emergeTimer);
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto bg-slate-950/80 backdrop-blur-md transition-opacity duration-300">
      {/* Background ambient lighting */}
      <div className="absolute inset-0 bg-radial from-red-600/15 via-transparent to-transparent pointer-events-none" />

      {/* Main Container */}
      <div className="relative w-full max-w-3xl flex flex-col items-center my-auto transition-all duration-700">
        {/* Floating Close Button */}
        <button
          onClick={onClose}
          className="absolute -top-12 right-0 sm:right-2 z-30 p-2 text-white/80 hover:text-white bg-slate-900/80 hover:bg-slate-800 rounded-full border border-white/20 transition-all cursor-pointer shadow-lg"
          title="Tutup Pengumuman"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Envelope & Letter Stage */}
        <div className="relative w-full flex flex-col items-center">
          {/* THE LETTER (Surat Hasil Undian) */}
          <div
            className={`w-full max-w-2xl bg-[#fffef9] text-slate-800 rounded-xl shadow-2xl border border-amber-200/80 p-5 sm:p-8 z-20 transition-all duration-700 ease-out transform ${
              animStage === 'emerged'
                ? 'translate-y-0 opacity-100 scale-100'
                : 'translate-y-28 opacity-0 scale-95 pointer-events-none'
            }`}
            style={{
              backgroundImage: 'radial-gradient(#e5e7eb 0.75px, transparent 0.75px)',
              backgroundSize: '16px 16px',
            }}
          >
            {/* Top Corporate Ribbon / Badge */}
            <div className="flex items-center justify-between border-b-2 border-red-600 pb-4 mb-5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center text-white font-black text-xl shadow-md">
                  A
                </div>
                <div>
                  <h3 className="font-extrabold text-sm sm:text-base tracking-wide text-slate-900 uppercase">
                    PT MIDI UTAMA INDONESIA TBK
                  </h3>
                  <p className="text-[11px] sm:text-xs text-slate-500 font-medium">
                    Surat Keputusan Pemenang Undian Resmi
                  </p>
                </div>
              </div>
              <div className="text-right">
                <span className="text-[10px] sm:text-xs font-semibold uppercase tracking-wider text-red-600 block">
                  {groupName || 'Doorprize'}
                </span>
                <span className="text-[10px] text-slate-400">
                  {new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })}
                </span>
              </div>
            </div>

            {/* Letter Title */}
            <div className="text-center mb-6">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-bold uppercase tracking-wider mb-2">
                <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                Daftar Pemenang Terpilih
              </div>
              <h2 className="text-xl sm:text-2xl font-black text-red-700 tracking-tight font-serif uppercase">
                {eventTitle || 'DOORPRIZE 18 TAHUN ALFAMIDI'}
              </h2>
              <p className="text-xs text-slate-600 mt-1">
                Selamat kepada {winners.length} rekan karyawan Alfamidi berikut yang beruntung:
              </p>
            </div>

            {/* Winner List (Formatted: NAMA - JABATAN - CABANG, etc.) */}
            <div className="space-y-2.5 max-h-[42vh] overflow-y-auto pr-1">
              {winners.map((winner, idx) => (
                <div
                  key={winner.id || idx}
                  className="flex items-start gap-3 p-3 sm:p-3.5 bg-gradient-to-r from-red-50/70 via-white to-amber-50/50 rounded-lg border border-red-100 hover:border-red-300 transition-colors shadow-xs"
                >
                  <div className="flex-shrink-0 w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-red-600 text-white font-extrabold text-xs sm:text-sm flex items-center justify-center shadow-xs">
                    {winner.rank || idx + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm sm:text-base font-bold text-slate-900 tracking-tight leading-snug">
                      {winner.displayFormatted}
                    </p>
                    {winner.weightScore !== undefined && (
                      <p className="text-[11px] text-slate-500 mt-0.5">
                        Bobot Poin: <span className="font-semibold text-slate-700">{winner.weightScore}</span>
                      </p>
                    )}
                  </div>
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                </div>
              ))}
            </div>

            {/* Verification Footer Note */}
            <div className="mt-5 pt-3 border-t border-slate-200 flex flex-wrap items-center justify-between gap-3 text-xs text-slate-500">
              <span className="italic">
                Sah & Terverifikasi oleh Sistem Pengundian Terbuka Alfamidi
              </span>
              <span className="font-mono text-[11px] text-slate-400">
                TOTAL: {winners.length} PEMENANG
              </span>
            </div>

            {/* Action Buttons */}
            <div className="mt-5 flex flex-wrap items-center justify-end gap-2.5">
              <button
                onClick={() => exportWinnersToExcel(winners, groupName, eventTitle, displayColumns)}
                className="px-3.5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer shadow-sm"
              >
                <FileSpreadsheet className="w-3.5 h-3.5" />
                Unduh Excel
              </button>
              <button
                onClick={() => exportWinnersToPDF(winners, groupName, eventTitle, displayColumns)}
                className="px-3.5 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer shadow-sm"
              >
                <FileText className="w-3.5 h-3.5" />
                Cetak PDF
              </button>
              <button
                onClick={onClose}
                className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-900 text-white text-xs font-semibold transition-colors cursor-pointer"
              >
                Selesai
              </button>
            </div>
          </div>

          {/* THE VINTAGE AIRMAIL ENVELOPE (AMPLOP SESUAI amplop.png) */}
          <div
            className={`w-full max-w-xl aspect-[1.65/1] rounded-lg shadow-2xl relative overflow-hidden transition-all duration-700 ease-out ${
              animStage === 'idle'
                ? 'translate-y-full opacity-0'
                : animStage === 'sliding'
                ? 'translate-y-0 opacity-100'
                : 'translate-y-12 sm:translate-y-16 scale-90 sm:scale-95 opacity-90'
            }`}
            style={{
              backgroundColor: '#f5efe4', // textured envelope cream
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.65)',
            }}
          >
            {/* Airmail Border (Diagonal Red & Blue Stripes like in amplop.png) */}
            <div
              className="absolute inset-0 pointer-events-none p-2 sm:p-3"
              style={{
                background:
                  'repeating-linear-gradient(135deg, #d71920 0, #d71920 18px, transparent 18px, transparent 24px, #1e40af 24px, #1e40af 42px, transparent 42px, transparent 48px)',
              }}
            >
              {/* Inner Cream Paper Body */}
              <div className="w-full h-full bg-[#fbf7f0] rounded-sm relative p-4 sm:p-7 flex flex-col justify-between overflow-hidden shadow-inner">
                {/* Paper texture overlay */}
                <div
                  className="absolute inset-0 opacity-35 pointer-events-none"
                  style={{
                    backgroundImage:
                      'radial-gradient(circle at 50% 50%, rgba(120, 90, 40, 0.08) 0%, transparent 60%)',
                  }}
                />

                {/* Top Section: PT MIDI UTAMA INDONESIA TBK + Stamp */}
                <div className="relative z-10 flex items-start justify-between">
                  {/* Left: Company Sender details */}
                  <div className="max-w-[65%] sm:max-w-[70%]">
                    <h4 className="font-serif font-black text-xs sm:text-base text-slate-800 tracking-wider uppercase leading-tight">
                      PT MIDI UTAMA INDONESIA TBK
                    </h4>
                    <p className="text-[9px] sm:text-[11px] text-slate-600 font-serif leading-tight mt-1">
                      Alfa Tower Alam Sutera, Jl. Jalur Sutera Bar. No.Kav. 7-9,
                      <br />
                      Kota Tangerang, Banten, Indonesia, 15143
                    </p>
                  </div>

                  {/* Right: Vintage Alfamidi Postage Stamp */}
                  <div className="relative flex-shrink-0">
                    <div
                      className="w-16 h-20 sm:w-20 sm:h-24 bg-[#a35e38] p-1.5 rounded-sm shadow-md flex items-center justify-center"
                      style={{
                        clipPath:
                          'polygon(0% 4%, 4% 0%, 8% 4%, 12% 0%, 16% 4%, 20% 0%, 24% 4%, 28% 0%, 32% 4%, 36% 0%, 40% 4%, 44% 0%, 48% 4%, 52% 0%, 56% 4%, 60% 0%, 64% 4%, 68% 0%, 72% 4%, 76% 0%, 80% 4%, 84% 0%, 88% 4%, 92% 0%, 96% 4%, 100% 0%, 100% 100%, 0% 100%)',
                      }}
                    >
                      <div className="w-full h-full bg-white border border-amber-900/30 rounded-xs flex flex-col items-center justify-center p-1">
                        <div className="w-8 h-8 sm:w-10 sm:h-10 bg-red-600 rounded-lg flex items-center justify-center text-white font-black text-xl sm:text-2xl shadow-xs">
                          A
                        </div>
                        <span className="text-[10px] sm:text-[11px] font-black text-red-600 tracking-tighter mt-1">
                          Alfamidi
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Center Section: "TO: THE WINNER OF DOORPRIZE 18 TAHUN ALFAMIDI" */}
                <div className="relative z-10 my-auto pl-4 sm:pl-8 py-2">
                  <div className="text-xs sm:text-sm font-serif font-black text-red-800 tracking-wider">
                    TO : THE WINNER OF
                  </div>
                  <div className="text-base sm:text-2xl md:text-3xl font-serif font-black text-red-700 uppercase tracking-tight leading-tight mt-0.5">
                    {eventTitle || 'DOORPRIZE 18 TAHUN ALFAMIDI'}
                  </div>
                  <div className="text-[10px] sm:text-xs font-semibold text-slate-600 mt-1 uppercase tracking-wider">
                    {groupName} • {winners.length} PEMENANG RESMI
                  </div>
                </div>

                {/* Bottom decorative stamp */}
                <div className="relative z-10 flex justify-between items-end text-[9px] text-slate-400 font-mono">
                  <span>AIR MAIL / PAR AVION</span>
                  <span>CONFIDENTIAL & OFFICIAL</span>
                </div>
              </div>
            </div>

            {/* Envelope Flap Overlay for opening animation */}
            <div
              className={`absolute top-0 inset-x-0 h-1/2 origin-top transition-transform duration-700 ease-in-out pointer-events-none ${
                animStage === 'opening' || animStage === 'emerged'
                  ? '-rotate-x-180 opacity-0'
                  : 'rotate-x-0 opacity-100'
              }`}
              style={{
                transformStyle: 'preserve-3d',
                background: 'linear-gradient(to bottom, #ede3d2, #dccdb3)',
                clipPath: 'polygon(0% 0%, 50% 100%, 100% 0%)',
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
