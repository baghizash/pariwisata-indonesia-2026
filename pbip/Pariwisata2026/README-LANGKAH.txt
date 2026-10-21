PAKET POWER BI PROJECT (.pbip) — Pariwisata Indonesia 2026
=============================================================

Isi paket ini adalah project Power BI (format .pbip) yang sudah dirakit:
model data (10 tabel), 14 measure DAX, 5 relasi, dan 4 halaman dashboard.
Tinggal dibuka, diarahkan ke folder data, refresh, lalu simpan sebagai .pbix.

LANGKAH MEMBUKA
---------------
1. Extract zip ini di mana saja (misalnya D:\PowerBI\Pariwisata2026\).
2. Buka file Pariwisata2026.pbip dengan Power BI Desktop.
3. Kalau data gagal dimuat (error FolderData): menu Modeling - Edit parameters
   - isi FolderData dengan path folder "data" hasil extract
   (contoh: D:\PowerBI\Pariwisata2026\data) - OK - Refresh.
   Default parameter adalah C:\PowerBI\Pariwisata\data.
4. Setelah semua tabel termuat, File - Save As - simpan sebagai
   Pariwisata-Indonesia-2026.pbix.
5. Cek cepat: kartu Kunjungan Wisman 2025 di halaman Ringkasan Eksekutif
   harus menunjukkan 15.386.646, kartu Pemulihan vs 2019 sebesar 95,5%,
   pangsa Ngurah Rai pada donat 2025 sebesar 44,9%, dan total Wisnus 2025
   sebesar 1.200.332.559.

CATATAN / HAL YANG MUNGKIN PERLU SENTUHAN KECIL SAAT PERTAMA DIBUKA
--------------------------------------------------------------------
- Angka setahun penuh selalu berasal dari fact_wisman_tahunan. Tabel
  bulanan (fact_wisman_bulanan) untuk 2024 hanya memuat Nov-Des dan untuk
  2025 memuat 10 bulan, karena bulan lainnya tidak diterbitkan BPS sebagai
  angka eksak per bulan; grafik garis bulanan di halaman 1 memakai 2026
  (Jan-Agu, lengkap) sehingga tidak terpengaruh.
- Kartu KPI lain dikunci ke konteks headline lewat filter level visual
  (pemulihan = tahun 2025, RLM = Des 2025 tamu asing, TPK = tahun 2025),
  supaya angkanya langsung benar. Slicer tetap menggerakkan visual
  eksplorasi di halamannya.
- Visual peta untuk TPK provinsi SENGAJA diganti bar terurut (visual peta
  PBIR rawan error saat pertama dibuka). Jika ingin peta, tambahkan visual
  Filled Map manual di Power BI Desktop memakai fact_tpk_provinsi.
- Slicer tahun pada halaman 3 (Hotel) berbentuk daftar; TPK snapshot
  Des 2025 adalah tabel terpisah (fact_tpk_snapshot) dan tidak ikut slicer.
- Mark as date table tidak diperlukan: model ini tidak memakai tabel
  kalender otomatis; dim_bulan terurut oleh kolom bulan_ke.

SUMBER DATA: BPS (BRS Perkembangan Pariwisata Des 2024-Agu 2026 dan
Statistik Kunjungan Wisman 2023), folder data/ berisi 10 CSV star-schema
yang sama dengan kit proyek pariwisata-indonesia-2026.
