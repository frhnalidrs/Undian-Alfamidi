import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { WinnerItem } from '../types';

export function exportWinnersToExcel(
  winners: WinnerItem[],
  groupName: string,
  eventTitle: string,
  displayColumns: string[]
): void {
  if (winners.length === 0) return;

  // Build clean rows for Excel
  const excelRows = winners.map((w, index) => {
    const row: Record<string, string | number> = {
      'No. Urut': index + 1,
      'Kategori Hadiah': w.group || groupName,
      'Nama Pemenang': w.name,
      'Format Lengkap': w.displayFormatted,
    };

    // Add selected display columns
    displayColumns.forEach(col => {
      row[col] = w.data[col] ?? '';
    });

    // Add other fields from data
    Object.keys(w.data).forEach(key => {
      if (key !== '_id' && !row[key]) {
        row[key] = w.data[key];
      }
    });

    row['Waktu Undian'] = new Date(w.drawTimestamp).toLocaleString('id-ID');
    return row;
  });

  const worksheet = XLSX.utils.json_to_sheet(excelRows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Pemenang Undian');

  // Set column widths
  const colWidths = [
    { wch: 10 },
    { wch: 25 },
    { wch: 28 },
    { wch: 45 },
    { wch: 20 },
    { wch: 25 },
    { wch: 25 },
  ];
  worksheet['!cols'] = colWidths;

  const safeTitle = (groupName || 'Pemenang_Undian').replace(/[^a-zA-Z0-9]/g, '_');
  const filename = `Alfamidi_Doorprize_${safeTitle}_${Date.now()}.xlsx`;
  XLSX.writeFile(workbook, filename);
}

export function exportWinnersToPDF(
  winners: WinnerItem[],
  groupName: string,
  eventTitle: string,
  displayColumns: string[]
): void {
  if (winners.length === 0) return;

  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  // Top Alfamidi red accent bar
  doc.setFillColor(215, 25, 32); // Alfamidi signature red #d71920
  doc.rect(0, 0, 210, 8, 'F');

  // Yellow strip below red bar
  doc.setFillColor(255, 204, 0); // Alfamidi signature yellow
  doc.rect(0, 8, 210, 2.5, 'F');

  // Company Letterhead
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.setTextColor(30, 41, 59);
  doc.text('PT MIDI UTAMA INDONESIA TBK', 14, 20);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(100, 116, 139);
  doc.text(
    'Alfa Tower Alam Sutera, Jl. Jalur Sutera Bar. No.Kav. 7-9, Kota Tangerang, Banten, Indonesia 15143',
    14,
    26
  );
  doc.text('Telepon: (021) 5088 2888 | Website: www.alfamidiku.com', 14, 31);

  // Divider line
  doc.setDrawColor(226, 232, 240);
  doc.setLineWidth(0.6);
  doc.line(14, 35, 196, 35);

  // Document Title
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(215, 25, 32);
  doc.text('BERITA ACARA RESMI PENGUNDIAN DOORPRIZE', 14, 43);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10);
  doc.setTextColor(51, 65, 85);
  doc.text(`Acara / Event  : ${eventTitle || 'DOORPRIZE 18 TAHUN ALFAMIDI'}`, 14, 49);
  doc.text(`Kategori Undian: ${groupName || 'Hadiah Utama'}`, 14, 55);
  doc.text(`Jumlah Pemenang: ${winners.length} Orang`, 14, 61);
  doc.text(`Waktu Penarikan: ${new Date().toLocaleString('id-ID', { dateStyle: 'full', timeStyle: 'medium' })} WIB`, 14, 67);

  // AutoTable columns
  const tableHeaders = ['No', 'Nama Pemenang'];
  // Add user display columns
  displayColumns.forEach(col => {
    tableHeaders.push(col.toUpperCase());
  });

  const tableRows = winners.map((w, index) => {
    const row = [(index + 1).toString(), w.name];
    displayColumns.forEach(col => {
      row.push(String(w.data[col] ?? '-'));
    });
    return row;
  });

  autoTable(doc, {
    startY: 73,
    head: [tableHeaders],
    body: tableRows,
    theme: 'striped',
    headStyles: {
      fillColor: [215, 25, 32],
      textColor: [255, 255, 255],
      fontSize: 9,
      fontStyle: 'bold',
      halign: 'left',
    },
    bodyStyles: {
      fontSize: 8.5,
      textColor: [30, 41, 59],
    },
    alternateRowStyles: {
      fillColor: [254, 242, 242], // very light red tint
    },
    margin: { left: 14, right: 14 },
  });

  // Get final Y position after table
  const finalY = (doc as unknown as { lastAutoTable?: { finalY: number } }).lastAutoTable?.finalY || 180;

  // Signature Block if space permits, otherwise add page
  const signY = finalY > 230 ? (doc.addPage(), 30) : finalY + 15;

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(71, 85, 105);
  doc.text('Demikian Berita Acara Hasil Pengundian ini dibuat dengan sebenar-benarnya dan bersifat mutlak.', 14, signY);

  const col1X = 25;
  const col2X = 90;
  const col3X = 155;
  const signLabelY = signY + 10;
  const signLineY = signLabelY + 22;

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8.5);
  doc.setTextColor(51, 65, 85);
  doc.text('Saksi 1 (Manajemen)', col1X, signLabelY, { align: 'center' });
  doc.text('Saksi 2 (Notaris/Auditor)', col2X, signLabelY, { align: 'center' });
  doc.text('Ketua Panitia Undian', col3X, signLabelY, { align: 'center' });

  doc.setDrawColor(148, 163, 184);
  doc.line(col1X - 20, signLineY, col1X + 20, signLineY);
  doc.line(col2X - 20, signLineY, col2X + 20, signLineY);
  doc.line(col3X - 20, signLineY, col3X + 20, signLineY);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text('(Tanda Tangan & Cap)', col1X, signLineY + 5, { align: 'center' });
  doc.text('(Tanda Tangan & Cap)', col2X, signLineY + 5, { align: 'center' });
  doc.text('(Tanda Tangan & Cap)', col3X, signLineY + 5, { align: 'center' });

  const safeTitle = (groupName || 'Pemenang_Undian').replace(/[^a-zA-Z0-9]/g, '_');
  doc.save(`Berita_Acara_Alfamidi_${safeTitle}_${Date.now()}.pdf`);
}
