export interface CandidateRecord {
  _id: string;
  [key: string]: string | number;
}

export interface ColumnMeta {
  name: string;
  sampleValues: (string | number)[];
  isNumeric: boolean;
  totalFilled: number;
}

export interface PrizeCategory {
  id: string;
  name: string;
  winnerCount: number;
}

export interface DrawSettings {
  nameColumn: string;
  useWeighting: boolean;
  weightColumn: string;
  winnerCount: number;
  groupName: string;
  displayColumns: string[];
  eventTitle: string;
  allowDuplicateWinners: boolean;
  categories: PrizeCategory[];
}

export interface WinnerItem {
  id: string;
  rank: number;
  group: string;
  name: string;
  displayFormatted: string; // e.g. "BUDI SANTOSO - STORE LEADER - CABANG MAKASSAR"
  data: Record<string, string | number>;
  weightScore?: number;
  drawTimestamp: string;
}

export interface DrawHistoryEntry {
  id: string;
  groupName: string;
  eventTitle: string;
  timestamp: string;
  winnerCount: number;
  displayColumns: string[];
  winners: WinnerItem[];
}
