# Panduan Membangun Dashboard — Pariwisata Indonesia 2026

Nama berkas akhir yang disarankan: **Pariwisata-Indonesia-2026.pbix**

## Langkah
1. Buka Power BI Desktop → Get Data → Text/CSV. Muat 9 berkas pada folder ini:
   fact_wisman_bulanan, fact_wisman_tahunan, fact_wisman_pintu,
   fact_wisman_kebangsaan, fact_tpk_provinsi, fact_tpk_snapshot, fact_rlm,
   fact_wisnus_tujuan, dim_bulan, dim_tahun.
2. Buat relasi sesuai daftar di `dashboard_layout.md` (bagian Relasi model).
   Atur dim_bulan terurut oleh kolom bulan_ke.
3. Buat semua measure pada `measures_dax.md` satu per satu
   (Home → New measure). Nama measure harus persis seperti di dokumen
   (teks polos, tanpa "=" di dalam nama).
4. Uji setiap measure dengan kartu kosong memakai filter pada
   **Tabel Verifikasi** di `measures_dax.md`. Semua angka harus cocok
   sebelum lanjut ke visual.
5. Susun 4 halaman mengikuti `dashboard_layout.md`. Terapkan tema:
   marine #0B3C5D, merah #D7263D, butter #F4B41A, latar #FAF6EF.
6. Simpan sebagai **Pariwisata-Indonesia-2026.pbix**.

## Catatan data (penting)
- Angka setahun penuh memakai fact_wisman_tahunan. Tabel bulanan 2024 hanya
  berisi November–Desember dan 2025 berisi 10 bulan (lihat data/SOURCES.md),
  jadi jangan menilai total tahunan dari tabel bulanan untuk 2024/2025.
- fact_wisman_pintu dan fact_wisman_kebangsaan memakai kolom `periode`
  berformat campuran (tahun, bulan-tahun, rentang YTD) — selalu aktifkan
  filter periode sebelum membaca pangsa.
- TPK tahunan adalah rata-rata Jan–Des; fact_tpk_snapshot adalah bulan
  Desember 2025 saja. Jangan menjumlahkan keduanya.
