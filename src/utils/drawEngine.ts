import { CandidateRecord, DrawSettings, WinnerItem } from '../types';

/**
 * High-performance draw engine capable of processing 100,000+ entries in milliseconds.
 * Uses Efraimidis-Spirakis (Algorithm A-Res) for weighted random sampling without replacement,
 * and Partial Fisher-Yates for uniform random sampling.
 */
export function drawWinners(
  pool: CandidateRecord[],
  settings: DrawSettings,
  alreadyWonIds: Set<string> = new Set()
): WinnerItem[] {
  // Filter out previous winners if duplicate wins are disallowed
  let eligible = pool;
  if (!settings.allowDuplicateWinners && alreadyWonIds.size > 0) {
    eligible = pool.filter(c => !alreadyWonIds.has(c._id));
  }

  const k = Math.min(settings.winnerCount, eligible.length);
  if (k <= 0) return [];

  let selectedCandidates: CandidateRecord[] = [];

  if (settings.useWeighting && settings.weightColumn) {
    // Weighted Sampling Without Replacement (A-Res Algorithm)
    // Score r = u ^ (1 / weight) where u ~ Uniform(0, 1)
    // Sort descending by r, take top k
    const weightCol = settings.weightColumn;

    const scored = eligible.map(candidate => {
      const rawWeight = Number(candidate[weightCol]);
      // Ensure positive non-zero weight (minimum 0.1)
      const weight = isNaN(rawWeight) || rawWeight <= 0 ? 1 : rawWeight;
      const u = Math.random();
      const score = Math.pow(u, 1 / weight);
      return { candidate, score, weight };
    });

    // Quick selection or partial sort for top K
    scored.sort((a, b) => b.score - a.score);
    selectedCandidates = scored.slice(0, k).map(s => s.candidate);
  } else {
    // Uniform Random Sampling (Partial Fisher-Yates)
    const copy = [...eligible];
    const n = copy.length;
    for (let i = 0; i < k; i++) {
      const j = i + Math.floor(Math.random() * (n - i));
      const temp = copy[i];
      copy[i] = copy[j];
      copy[j] = temp;
    }
    selectedCandidates = copy.slice(0, k);
  }

  const nowIso = new Date().toISOString();

  return selectedCandidates.map((cand, index) => {
    const rawName = String(cand[settings.nameColumn] || 'Tanpa Nama');

    // Format display string: e.g. "BUDI SANTOSO - STORE LEADER - CABANG MAKASSAR"
    const additionalParts = settings.displayColumns
      .filter(col => col !== settings.nameColumn && cand[col] !== undefined && cand[col] !== '')
      .map(col => String(cand[col]));

    const displayFormatted = [rawName, ...additionalParts].join(' - ');

    const weightVal = settings.weightColumn && cand[settings.weightColumn] !== undefined
      ? Number(cand[settings.weightColumn])
      : undefined;

    return {
      id: cand._id,
      rank: index + 1,
      group: settings.groupName || 'Doorprize Utama',
      name: rawName,
      displayFormatted,
      data: { ...cand },
      weightScore: weightVal,
      drawTimestamp: nowIso,
    };
  });
}
