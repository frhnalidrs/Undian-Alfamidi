import React, { useState, useEffect, useRef } from 'react';
import confetti from 'canvas-confetti';
import { CandidateRecord, DrawSettings, WinnerItem } from '../types';
import { soundEffects } from '../utils/soundEffects';
import { Sparkles, Volume2, VolumeX, RefreshCw, Gift, Users, Eye, Play } from 'lucide-react';

interface SlotMachineProps {
  candidates: CandidateRecord[];
  settings: DrawSettings;
  isSpinning: boolean;
  onPullLever: () => void;
  recentWinners: WinnerItem[] | null;
  onResetDraw: () => void;
  onSelectCategory: (categoryName: string) => void;
  onUpdateWinnerCount: (count: number) => void;
  onViewLastResultModal?: () => void;
  hasLastResult?: boolean;
  lastResultCount?: number;
}

export const SlotMachine: React.FC<SlotMachineProps> = ({
  candidates,
  settings,
  isSpinning,
  onPullLever,
  recentWinners,
  onResetDraw,
  onSelectCategory,
  onUpdateWinnerCount,
  onViewLastResultModal,
  hasLastResult = false,
  lastResultCount = 0,
}) => {
  const [buttonPressed, setButtonPressed] = useState(false);
  const [soundOn, setSoundOn] = useState(true);

  // Reel values cycling during spin
  const [reelItems, setReelItems] = useState<{ name: string; extra: string }[]>([
    { name: 'ALFAMIDI', extra: 'SIAP UNDI' },
    { name: 'DOORPRIZE', extra: 'SIAP UNDI' },
    { name: '18 TAHUN', extra: 'SIAP UNDI' },
  ]);

  const spinIntervalRef = useRef<number | null>(null);

  const toggleSound = () => {
    soundEffects.enabled = !soundOn;
    setSoundOn(!soundOn);
  };

  const handleStartDraw = () => {
    if (isSpinning || candidates.length === 0) return;
    setButtonPressed(true);
    soundEffects.playLeverPull();
    setTimeout(() => {
      setButtonPressed(false);
    }, 300);
    onPullLever();
  };

  // Spinning animation cycle
  useEffect(() => {
    if (isSpinning) {
      const nameCol = settings.nameColumn;
      const extraCols = settings.displayColumns.filter(c => c !== nameCol);

      let tickCounter = 0;
      spinIntervalRef.current = window.setInterval(() => {
        tickCounter++;
        if (tickCounter % 3 === 0) {
          soundEffects.playReelTick(Math.random() * 40 - 20);
        }

        // Pick random items from pool
        const numReels = Math.min(3, Math.max(1, settings.winnerCount));
        const newItems: { name: string; extra: string }[] = [];

        for (let i = 0; i < numReels; i++) {
          const randIdx = Math.floor(Math.random() * candidates.length);
          const cand = candidates[randIdx];
          const name = cand ? String(cand[nameCol] || 'Kandidat') : 'Alfamidi';
          const extra = extraCols.length > 0 && cand
            ? extraCols.map(c => String(cand[c] || '')).filter(Boolean).join(' • ')
            : 'Peserta Undian';
          newItems.push({ name, extra });
        }
        setReelItems(newItems);
      }, 50);
    } else {
      if (spinIntervalRef.current) {
        clearInterval(spinIntervalRef.current);
        spinIntervalRef.current = null;
      }

      // If we have <= 3 winners and draw just completed, populate reels with actual winners!
      if (recentWinners && recentWinners.length > 0 && recentWinners.length <= 3) {
        soundEffects.playReelStop(659.25);
        soundEffects.playFanfare();

        // Confetti for slot machine win
        confetti({
          particleCount: 70,
          spread: 80,
          origin: { y: 0.55 },
          colors: ['#d71920', '#ffcc00', '#ffffff'],
        });

        const numReels = recentWinners.length;
        const finalReels = recentWinners.slice(0, numReels).map(w => {
          const extra = settings.displayColumns
            .filter(c => c !== settings.nameColumn)
            .map(c => String(w.data[c] || ''))
            .filter(Boolean)
            .join(' • ');
          return {
            name: w.name,
            extra: extra || (w.group || 'Pemenang'),
          };
        });
        setReelItems(finalReels);
      }
    }

    return () => {
      if (spinIntervalRef.current) {
        clearInterval(spinIntervalRef.current);
      }
    };
  }, [isSpinning, recentWinners, candidates, settings]);

  const numReels = Math.min(3, Math.max(1, settings.winnerCount));
  const showWinnersDirectlyInSlot = recentWinners && recentWinners.length > 0 && recentWinners.length <= 3;

  return (
    <div className="relative w-full max-w-4xl mx-auto flex items-center justify-center py-2 px-2 sm:px-6">
      {/* Background radial glow */}
      <div className="absolute inset-0 bg-radial from-red-600/20 via-amber-500/10 to-transparent blur-2xl pointer-events-none" />

      {/* Main Slot Machine Chassis */}
      <div className="relative w-full bg-gradient-to-b from-red-800 via-red-900 to-red-950 p-4 sm:p-7 rounded-3xl border-4 border-amber-400 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.9)] flex flex-col items-center">
        {/* Flashing Arcade Bulbs Top Bar */}
        <div className="w-full flex items-center justify-between px-3 py-1 mb-3 bg-red-950/70 rounded-full border border-amber-500/40">
          <div className="flex items-center gap-1.5 sm:gap-2">
            {[...Array(8)].map((_, i) => (
              <span
                key={i}
                className={`w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full transition-all duration-300 ${
                  isSpinning
                    ? i % 2 === 0
                      ? 'bg-amber-300 shadow-[0_0_8px_#fde047]'
                      : 'bg-red-500 shadow-[0_0_8px_#ef4444]'
                    : 'bg-amber-400/80'
                }`}
              />
            ))}
          </div>

          <button
            onClick={toggleSound}
            className="flex items-center gap-1 text-[11px] font-semibold text-amber-300 hover:text-white bg-red-900/60 px-2.5 py-1 rounded-full border border-amber-400/30 transition-colors cursor-pointer"
            title={soundOn ? 'Matikan Suara' : 'Nyalakan Suara'}
          >
            {soundOn ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5 text-slate-400" />}
            <span className="hidden sm:inline">{soundOn ? 'Suara ON' : 'Mute'}</span>
          </button>

          <div className="flex items-center gap-1.5 sm:gap-2">
            {[...Array(8)].map((_, i) => (
              <span
                key={i}
                className={`w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full transition-all duration-300 ${
                  isSpinning
                    ? i % 2 === 1
                      ? 'bg-amber-300 shadow-[0_0_8px_#fde047]'
                      : 'bg-red-500 shadow-[0_0_8px_#ef4444]'
                    : 'bg-amber-400/80'
                }`}
              />
            ))}
          </div>
        </div>

        {/* Marquee Banner Header */}
        <div className="w-full text-center py-2 px-4 mb-3 rounded-xl bg-gradient-to-r from-amber-600 via-amber-400 to-amber-600 text-slate-950 font-black shadow-lg border-2 border-amber-200">
          <div className="flex items-center justify-center gap-2">
            <Sparkles className="w-5 h-5 text-red-700 animate-spin" />
            <h2 className="text-base sm:text-xl md:text-2xl font-black tracking-wider uppercase font-serif drop-shadow-xs">
              {settings.eventTitle || 'DOORPRIZE 18 TAHUN ALFAMIDI'}
            </h2>
            <Sparkles className="w-5 h-5 text-red-700 animate-spin" />
          </div>
        </div>

        {/* KATEGORI HADIAH & JUMLAH PEMENANG CONTAINER (Rapi dan tidak keluar boks) */}
        <div className="w-full mb-4 p-3 sm:p-4 bg-red-950/85 rounded-2xl border border-amber-400/40 shadow-inner space-y-2.5">
          {/* Baris 1: Kategori Hadiah Dropdown */}
          <div className="flex flex-col sm:flex-row sm:items-center gap-2">
            <div className="flex items-center gap-2 flex-shrink-0">
              <Gift className="w-4 h-4 text-amber-400" />
              <span className="text-xs font-bold text-amber-300 uppercase tracking-wider">
                Kategori Hadiah:
              </span>
            </div>
            <select
              value={settings.groupName}
              onChange={e => onSelectCategory(e.target.value)}
              disabled={isSpinning}
              className="flex-1 w-full bg-slate-900 border border-amber-400/60 rounded-xl px-3 py-2 text-xs sm:text-sm font-bold text-white focus:outline-none focus:border-amber-300 cursor-pointer shadow-inner truncate"
            >
              {settings.categories && settings.categories.length > 0 ? (
                settings.categories.map(cat => (
                  <option key={cat.id} value={cat.name}>
                    {cat.name} ({cat.winnerCount} Pemenang)
                  </option>
                ))
              ) : (
                <option value={settings.groupName}>{settings.groupName}</option>
              )}
            </select>
          </div>

          {/* Baris 2: Jumlah Pemenang (Dipindahkan ke bawah Kategori Hadiah dengan icon Users 3 orang) */}
          <div className="pt-2 border-t border-red-900/60 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-amber-300 flex-shrink-0" />
              <span className="text-xs font-bold text-amber-200 uppercase tracking-wider">
                Jumlah Pemenang:
              </span>
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              {/* Quick count chips */}
              <div className="flex items-center gap-1">
                {[1, 3, 5, 10, 20].map(cnt => (
                  <button
                    key={cnt}
                    type="button"
                    onClick={() => onUpdateWinnerCount(cnt)}
                    disabled={isSpinning}
                    className={`px-2 py-0.5 text-xs font-bold rounded-lg transition-colors cursor-pointer ${
                      settings.winnerCount === cnt
                        ? 'bg-amber-400 text-slate-950 font-black shadow-xs'
                        : 'bg-red-900/80 text-amber-200/80 hover:bg-red-800 hover:text-white'
                    }`}
                  >
                    {cnt}
                  </button>
                ))}
              </div>

              {/* Number Input */}
              <div className="flex items-center gap-1 bg-slate-900 px-2 py-1 rounded-lg border border-amber-400/50">
                <input
                  type="number"
                  min={1}
                  max={Math.max(1, candidates.length)}
                  value={settings.winnerCount}
                  onChange={e => onUpdateWinnerCount(Math.max(1, parseInt(e.target.value) || 1))}
                  disabled={isSpinning}
                  className="w-12 sm:w-16 bg-transparent text-xs sm:text-sm text-amber-300 font-mono font-black text-center focus:outline-none"
                />
                <span className="text-[11px] text-slate-400 font-semibold">Orang</span>
              </div>
            </div>
          </div>
        </div>

        {/* Slot Reels Container & Arcade Big Red Button */}
        <div className="w-full flex flex-col md:flex-row items-center justify-between gap-4 sm:gap-6">
          {/* Glass Reels Display Box */}
          <div className="flex-1 w-full bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 p-3 sm:p-5 rounded-2xl border-4 border-amber-500/80 shadow-[inset_0_10px_25px_rgba(0,0,0,0.8)] relative overflow-hidden">
            {/* Gloss reflection overlay */}
            <div className="absolute top-0 inset-x-0 h-1/3 bg-gradient-to-b from-white/15 to-transparent pointer-events-none rounded-t-xl" />

            {/* Center target indicator line */}
            <div className="absolute inset-y-0 left-0 right-0 my-auto h-20 sm:h-24 border-y-2 border-amber-400/40 bg-amber-400/5 pointer-events-none z-10 flex items-center justify-between px-1">
              <span className="text-amber-400 text-xs font-black">▶</span>
              <span className="text-amber-400 text-xs font-black">◀</span>
            </div>

            {/* Reels Grid */}
            <div
              className={`grid gap-3 sm:gap-4 relative z-0 ${
                numReels === 1
                  ? 'grid-cols-1'
                  : numReels === 2
                  ? 'grid-cols-2'
                  : 'grid-cols-1 sm:grid-cols-3'
              }`}
            >
              {[...Array(numReels)].map((_, idx) => {
                const item = reelItems[idx] || { name: 'Alfamidi', extra: 'Siap Undi' };
                const isWinnerResult = showWinnersDirectlyInSlot && recentWinners?.[idx];

                return (
                  <div
                    key={idx}
                    className={`h-28 sm:h-36 rounded-xl border-2 flex flex-col items-center justify-center text-center p-2.5 transition-all relative overflow-hidden ${
                      isWinnerResult
                        ? 'bg-gradient-to-b from-amber-100 via-white to-amber-50 border-amber-400 shadow-[0_0_20px_#f59e0b]'
                        : 'bg-gradient-to-b from-slate-800 to-slate-900 border-slate-700 text-slate-100 shadow-inner'
                    } ${isSpinning ? 'blur-[0.5px] scale-[0.99]' : ''}`}
                  >
                    {/* Badge if 1-3 winner displayed */}
                    {isWinnerResult && (
                      <span className="absolute top-1.5 right-1.5 px-2 py-0.5 bg-red-600 text-white text-[10px] font-black rounded-full uppercase shadow-xs">
                        Pemenang #{idx + 1}
                      </span>
                    )}

                    <div className="w-full my-auto">
                      <p
                        className={`font-black text-sm sm:text-base md:text-lg tracking-tight uppercase line-clamp-2 px-1 ${
                          isWinnerResult ? 'text-red-700' : 'text-amber-300'
                        }`}
                      >
                        {item.name}
                      </p>

                      <p
                        className={`text-[11px] sm:text-xs font-medium mt-1 line-clamp-2 px-1 ${
                          isWinnerResult ? 'text-slate-700 font-semibold' : 'text-slate-400'
                        }`}
                      >
                        {item.extra}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* ARCADE BIG RED BUTTON (Menggantikan Animasi Tuas) */}
          <div className="flex flex-col items-center justify-center flex-shrink-0 select-none py-1">
            <div className="relative group">
              {/* Outer Golden Arcade Bezel Ring */}
              <div className="w-28 h-28 sm:w-32 sm:h-32 rounded-full p-2 bg-gradient-to-b from-amber-300 via-amber-500 to-amber-700 shadow-[0_12px_28px_rgba(0,0,0,0.8),inset_0_2px_4px_rgba(255,255,255,0.6)] flex items-center justify-center">
                {/* Inner Metallic Bezel Ring */}
                <div className="w-full h-full rounded-full p-2 bg-gradient-to-b from-slate-800 via-slate-900 to-black shadow-inner flex items-center justify-center">
                  {/* The Big 3D Red Push Button */}
                  <button
                    type="button"
                    onClick={handleStartDraw}
                    disabled={isSpinning || candidates.length === 0}
                    className={`w-full h-full rounded-full cursor-pointer transition-all duration-150 flex flex-col items-center justify-center text-center relative overflow-hidden outline-none ${
                      isSpinning
                        ? 'bg-gradient-to-b from-red-800 to-red-950 scale-95 opacity-80 cursor-not-allowed shadow-inner'
                        : buttonPressed
                        ? 'bg-gradient-to-b from-red-700 to-red-900 scale-90 translate-y-1 shadow-[inset_0_4px_10px_rgba(0,0,0,0.9)]'
                        : 'bg-gradient-to-b from-red-500 via-red-600 to-red-800 hover:from-red-400 hover:to-red-700 shadow-[0_6px_0_#7f1d1d,0_12px_20px_rgba(220,38,38,0.6)] hover:shadow-[0_8px_0_#7f1d1d,0_16px_25px_rgba(239,68,68,0.8)] active:scale-95 active:translate-y-1'
                    }`}
                    title="Tekan Tombol Merah untuk Mengundi!"
                  >
                    {/* Top glass reflection highlight */}
                    <div className="absolute top-1 inset-x-3 h-1/3 bg-gradient-to-b from-white/50 to-transparent rounded-full pointer-events-none" />

                    {/* Button Text & Icon */}
                    <Play className={`w-5 h-5 sm:w-6 sm:h-6 text-white drop-shadow-md mb-0.5 fill-white ${isSpinning ? 'animate-spin' : ''}`} />
                    <span className="text-[11px] sm:text-xs font-black tracking-wider uppercase text-white drop-shadow-md font-mono leading-none">
                      {isSpinning ? 'PUTAR' : 'TEKAN'}
                    </span>
                    <span className="text-[9px] font-bold text-amber-200 tracking-widest uppercase leading-none mt-0.5">
                      UNDI
                    </span>
                  </button>
                </div>
              </div>

              {/* Pulsing glow ring when idle */}
              {!isSpinning && candidates.length > 0 && (
                <div className="absolute inset-0 rounded-full border-2 border-red-500/40 animate-ping pointer-events-none" />
              )}
            </div>

            <span className="text-[11px] font-black text-amber-300 uppercase tracking-widest mt-2">
              TOMBOL UNDI
            </span>
          </div>
        </div>

        {/* Bottom Control Bar */}
        <div className="w-full mt-4 flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-red-700/60">
          <div className="flex items-center gap-2 text-xs text-red-200">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>
              Total Kandidat: <strong className="text-white font-mono">{candidates.length.toLocaleString('id-ID')}</strong> peserta
            </span>
          </div>

          <div className="flex items-center gap-2.5 flex-wrap">
            {/* Tombol Lihat Hasil Undian Terakhir (jika modal tertutup tidak sengaja) */}
            {hasLastResult && onViewLastResultModal && (
              <button
                type="button"
                onClick={onViewLastResultModal}
                disabled={isSpinning}
                className="px-3 py-2 bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white text-xs font-bold rounded-xl border border-amber-400/40 flex items-center gap-1.5 transition-all cursor-pointer shadow-md hover:scale-105"
                title="Buka kembali modal hasil undian terakhir"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Lihat Modal Terakhir ({lastResultCount})</span>
              </button>
            )}

            {showWinnersDirectlyInSlot && (
              <button
                onClick={onResetDraw}
                className="px-3 py-2 bg-red-950/80 hover:bg-red-900 text-amber-300 text-xs font-semibold rounded-xl border border-amber-400/40 flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Undi Ulang
              </button>
            )}

            {/* Big Action Button */}
            <button
              onClick={handleStartDraw}
              disabled={isSpinning || candidates.length === 0}
              className={`px-6 sm:px-9 py-2.5 sm:py-3 rounded-xl font-black text-xs sm:text-sm uppercase tracking-wider transition-all duration-200 cursor-pointer shadow-xl ${
                isSpinning
                  ? 'bg-amber-600 text-amber-950 cursor-not-allowed opacity-80'
                  : candidates.length === 0
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-red-600 via-red-500 to-amber-500 hover:from-red-500 hover:to-amber-400 text-white border-2 border-amber-300 hover:scale-105 active:scale-95 shadow-[0_0_25px_rgba(239,68,68,0.6)]'
              }`}
            >
              {isSpinning ? 'SEDANG MEMUTAR...' : 'PUTAR UNDIAN SEKARANG'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
