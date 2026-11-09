/**
 * Synthesizes realistic audio effects using Web Audio API
 * No external audio files needed - 100% reliable in all environments.
 */

class SoundEffectsManager {
  private ctx: AudioContext | null = null;
  public enabled: boolean = true;

  private getContext(): AudioContext | null {
    if (!this.enabled) return null;
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    return this.ctx;
  }

  // Play mechanical lever pull and spring sound
  playLeverPull(): void {
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;

    // Lever click/creak
    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sawtooth';
    osc1.frequency.setValueAtTime(140, now);
    osc1.frequency.exponentialRampToValueAtTime(45, now + 0.12);
    gain1.gain.setValueAtTime(0.35, now);
    gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);
    osc1.start(now);
    osc1.stop(now + 0.13);

    // Mechanical snap/spring
    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'square';
    osc2.frequency.setValueAtTime(320, now + 0.1);
    osc2.frequency.exponentialRampToValueAtTime(80, now + 0.28);
    gain2.gain.setValueAtTime(0, now);
    gain2.gain.setValueAtTime(0.25, now + 0.1);
    gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);
    osc2.start(now + 0.1);
    osc2.stop(now + 0.29);
  }

  // Play rapid reel clicking sound
  playReelTick(pitchOffset = 0): void {
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(440 + pitchOffset, now);
    osc.frequency.exponentialRampToValueAtTime(220 + pitchOffset, now + 0.04);

    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.045);
  }

  // Reel stop clunk / bell chime
  playReelStop(tone = 523.25): void {
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(tone, now);

    gain.gain.setValueAtTime(0.28, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.45);
  }

  // Envelope slide whoosh
  playWhoosh(): void {
    const ctx = this.getContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(120, now);
    osc.frequency.exponentialRampToValueAtTime(480, now + 0.35);

    gain.gain.setValueAtTime(0.01, now);
    gain.gain.linearRampToValueAtTime(0.2, now + 0.15);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.46);
  }

  // Celebratory victory fanfare
  playFanfare(): void {
    const ctx = this.getContext();
    if (!ctx) return;

    const notes = [
      { freq: 523.25, time: 0, duration: 0.15 },      // C5
      { freq: 659.25, time: 0.16, duration: 0.15 },   // E5
      { freq: 783.99, time: 0.32, duration: 0.18 },   // G5
      { freq: 1046.50, time: 0.52, duration: 0.65 },  // C6
    ];

    const baseTime = ctx.currentTime;

    notes.forEach(({ freq, time, duration }) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, baseTime + time);

      gain.gain.setValueAtTime(0.25, baseTime + time);
      gain.gain.exponentialRampToValueAtTime(0.001, baseTime + time + duration);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(baseTime + time);
      osc.stop(baseTime + time + duration + 0.05);
    });
  }
}

export const soundEffects = new SoundEffectsManager();
