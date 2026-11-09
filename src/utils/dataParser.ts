import * as XLSX from 'xlsx';
import { CandidateRecord, ColumnMeta } from '../types';

/**
 * Robust CSV Line Parser that handles quotes and multiple common delimiters
 */
export function parseCSV(rawText: string): { headers: string[]; rows: Record<string, string | number>[] } {
  const clean = rawText.trim();
  if (!clean) return { headers: [], rows: [] };

  const lines = clean.split(/\r?\n/).filter(line => line.trim().length > 0);
  if (lines.length === 0) return { headers: [], rows: [] };

  // Detect delimiter (, or ; or \t)
  const firstLine = lines[0];
  const commaCount = (firstLine.match(/,/g) || []).length;
  const semicolonCount = (firstLine.match(/;/g) || []).length;
  const tabCount = (firstLine.match(/\t/g) || []).length;

  let delimiter = ',';
  if (semicolonCount > commaCount && semicolonCount > tabCount) {
    delimiter = ';';
  } else if (tabCount > commaCount && tabCount > semicolonCount) {
    delimiter = '\t';
  }

  const parseRow = (line: string): string[] => {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"') {
        if (inQuotes && line[i + 1] === '"') {
          current += '"';
          i++; // skip escaped quote
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === delimiter && !inQuotes) {
        result.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    result.push(current.trim());
    return result;
  };

  const rawHeaders = parseRow(lines[0]);
  const headers = rawHeaders.map((h, idx) => (h && h.length > 0 ? h : `Kolom_${idx + 1}`));

  const rows: Record<string, string | number>[] = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseRow(lines[i]);
    if (values.every(v => v === '')) continue;
    const row: Record<string, string | number> = {};
    headers.forEach((h, idx) => {
      const val = values[idx] ?? '';
      // Parse numeric if valid pure number
      const num = Number(val);
      if (val !== '' && !isNaN(num) && /^-?\d+(\.\d+)?$/.test(val.trim())) {
        row[h] = num;
      } else {
        row[h] = val;
      }
    });
    rows.push(row);
  }

  return { headers, rows };
}

/**
 * Parse Excel file (xlsx, xls) buffer
 */
export async function parseExcel(file: File): Promise<{ headers: string[]; rows: Record<string, string | number>[] }> {
  const buffer = await file.arrayBuffer();
  const workbook = XLSX.read(buffer, { type: 'array' });
  const firstSheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[firstSheetName];

  // Convert sheet to json array of objects
  const rawRows = XLSX.utils.sheet_to_json<Record<string, unknown>>(worksheet, { defval: '' });
  if (rawRows.length === 0) return { headers: [], rows: [] };

  const headers = Object.keys(rawRows[0] || {});
  const rows: Record<string, string | number>[] = rawRows.map(r => {
    const item: Record<string, string | number> = {};
    headers.forEach(h => {
      const v = r[h];
      if (typeof v === 'number') {
        item[h] = v;
      } else {
        const strVal = String(v ?? '').trim();
        const numVal = Number(strVal);
        if (strVal !== '' && !isNaN(numVal) && /^-?\d+(\.\d+)?$/.test(strVal)) {
          item[h] = numVal;
        } else {
          item[h] = strVal;
        }
      }
    });
    return item;
  });

  return { headers, rows };
}

/**
 * Fetch and parse Google Spreadsheet link
 */
export async function fetchGoogleSheet(url: string): Promise<{ headers: string[]; rows: Record<string, string | number>[] }> {
  let exportUrl = url.trim();

  // If standard edit / sharing link, extract sheet ID
  const sheetIdMatch = exportUrl.match(/\/d\/([a-zA-Z0-9-_]+)/);
  if (sheetIdMatch) {
    const sheetId = sheetIdMatch[1];
    const gidMatch = exportUrl.match(/gid=([0-9]+)/);
    const gid = gidMatch ? gidMatch[1] : '0';
    exportUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=csv&gid=${gid}`;
  } else if (exportUrl.includes('/pubhtml') || exportUrl.includes('/pub?')) {
    exportUrl = exportUrl.replace(/\/pubhtml.*$/, '/pub?output=csv');
  }

  const response = await fetch(exportUrl);
  if (!response.ok) {
    throw new Error(`Gagal mengambil Google Spreadsheet. Pastikan link disetel ke "Siapa saja yang memiliki link dapat melihat" (Public View). Status: ${response.status}`);
  }

  const csvText = await response.text();
  return parseCSV(csvText);
}

/**
 * Convert parsed rows to CandidateRecord with unique IDs
 */
export function buildCandidateRecords(rows: Record<string, string | number>[]): CandidateRecord[] {
  return rows.map((row, index) => ({
    _id: `row-${index + 1}`,
    ...row,
  }));
}

/**
 * Analyze column characteristics: numeric status, sample values, uniqueness
 */
export function analyzeColumns(headers: string[], candidates: CandidateRecord[]): ColumnMeta[] {
  const sampleLimit = Math.min(candidates.length, 100);

  return headers.map(header => {
    let numericCount = 0;
    let filledCount = 0;
    const sampleValues: (string | number)[] = [];

    for (let i = 0; i < sampleLimit; i++) {
      const val = candidates[i]?.[header];
      if (val !== undefined && val !== null && val !== '') {
        filledCount++;
        if (typeof val === 'number') {
          numericCount++;
        } else if (!isNaN(Number(val)) && /^-?\d+(\.\d+)?$/.test(String(val).trim())) {
          numericCount++;
        }
        if (sampleValues.length < 3 && !sampleValues.includes(val)) {
          sampleValues.push(val);
        }
      }
    }

    const isNumeric = sampleLimit > 0 && numericCount >= Math.floor(filledCount * 0.8) && filledCount > 0;

    return {
      name: header,
      sampleValues,
      isNumeric,
      totalFilled: filledCount,
    };
  });
}

/**
 * Guess best candidates for Name/Identity column and Weight column
 */
export function guessBestColumns(columns: ColumnMeta[]): { nameCol: string; weightCol: string } {
  let nameCol = columns[0]?.name || '';
  let weightCol = '';

  const nameKeywords = ['nama', 'name', 'karyawan', 'pegawai', 'employee', 'peserta', 'staff'];
  const weightKeywords = ['poin', 'point', 'bobot', 'weight', 'kupon', 'tiket', 'skor', 'score', 'kinerja', 'hadir'];

  for (const col of columns) {
    const lower = col.name.toLowerCase();
    if (nameKeywords.some(kw => lower.includes(kw))) {
      nameCol = col.name;
      break;
    }
  }

  for (const col of columns) {
    const lower = col.name.toLowerCase();
    if (col.isNumeric && weightKeywords.some(kw => lower.includes(kw))) {
      weightCol = col.name;
      break;
    }
  }

  if (!weightCol) {
    const anyNumeric = columns.find(c => c.isNumeric && c.name !== nameCol);
    if (anyNumeric) weightCol = anyNumeric.name;
  }

  return { nameCol, weightCol };
}

/**
 * Generator for realistic Alfamidi sample datasets
 * Supports 1,000 entries up to 30,000 entries
 */
export function generateSampleAlfamidiData(count = 1000): { headers: string[]; rows: Record<string, string | number>[] } {
  const firstNames = [
    'Agus', 'Budi', 'Siti', 'Dewi', 'Eko', 'Rina', 'Bambang', 'Wayan', 'Dian', 'Hendra',
    'Rahmat', 'Nur', 'Yanto', 'Tri', 'Ahmad', 'Fitri', 'Wahyu', 'Putri', 'Hadi', 'Ratna',
    'Rizky', 'Fajar', 'Dedi', 'Indah', 'Bayu', 'Mega', 'Surya', 'Anisa', 'Faisal', 'Tika',
    'Joko', 'Sri', 'Dimas', 'Lestari', 'Arif', 'Maya', 'Ilham', 'Wulan', 'Gilang', 'Nita',
    'Farhan', 'Syahrul', 'Nabila', 'Rian', 'Sari', 'Danu', 'Kartika', 'Adi', 'Melinda', 'Irfan'
  ];

  const lastNames = [
    'Santoso', 'Pratama', 'Kusuma', 'Wijaya', 'Saputra', 'Lestari', 'Hidayat', 'Nugroho',
    'Wibowo', 'Firmansyah', 'Suryono', 'Utomo', 'Siregar', 'Harahap', 'Nasution', 'Simanjuntak',
    'Pangestu', 'Gunawan', 'Hartono', 'Purnomo', 'Setiawan', 'Kurniawan', 'Ramadhan', 'Subagyo',
    'Pamungkas', 'Anggraini', 'Mahendra', 'Suharto', 'Yuliana', 'Suhendar', 'Alamsyah', 'Fadillah'
  ];

  const positions = [
    { title: 'Store Crew', weight: 45 },
    { title: 'Cashier Staff', weight: 25 },
    { title: 'Store Leader (Kepala Toko)', weight: 12 },
    { title: 'Assistant Store Leader', weight: 8 },
    { title: 'Area Coordinator', weight: 4 },
    { title: 'Warehouse & Logistics Staff', weight: 3 },
    { title: 'IT & Support Specialist', weight: 1.5 },
    { title: 'Human Capital Officer', weight: 1 },
    { title: 'Branch Operation Manager', weight: 0.5 },
  ];

  const branches = [
    'Cabang Tangerang (Head Office)',
    'Cabang Bekasi',
    'Cabang Bogor',
    'Cabang Medan',
    'Cabang Makassar',
    'Cabang Manado',
    'Cabang Samarinda',
    'Cabang Palu',
    'Cabang Ambon',
    'Cabang Kendari',
    'Cabang Bitung',
    'Cabang Palembang',
    'Cabang Pasuruan',
    'Cabang Yogyakarta',
  ];

  const getRandomPosition = (): string => {
    const totalWeight = positions.reduce((sum, p) => sum + p.weight, 0);
    let rand = Math.random() * totalWeight;
    for (const p of positions) {
      if (rand < p.weight) return p.title;
      rand -= p.weight;
    }
    return 'Store Crew';
  };

  const headers = ['NIK', 'NAMA_KARYAWAN', 'JABATAN', 'CABANG', 'MASA_KERJA_TAHUN', 'POIN_UNDIAN'];
  const rows: Record<string, string | number>[] = [];

  for (let i = 1; i <= count; i++) {
    const fn = firstNames[Math.floor(Math.random() * firstNames.length)];
    const ln = lastNames[Math.floor(Math.random() * lastNames.length)];
    const name = `${fn} ${ln}`;
    const nik = `MIDI-${String(100000 + i)}`;
    const position = getRandomPosition();
    const branch = branches[Math.floor(Math.random() * branches.length)];
    const tenure = Math.floor(Math.random() * 15) + 1; // 1 - 15 tahun
    // Poin undian berdasarkan masa kerja + performa (10 - 250 poin)
    const points = tenure * 10 + Math.floor(Math.random() * 80) + 10;

    rows.push({
      NIK: nik,
      NAMA_KARYAWAN: name,
      JABATAN: position,
      CABANG: branch,
      MASA_KERJA_TAHUN: tenure,
      POIN_UNDIAN: points,
    });
  }

  return { headers, rows };
}
