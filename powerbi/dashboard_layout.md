# Layout Dashboard Power BI — Pariwisata Indonesia 2026 (4 Halaman)

Nama berkas yang disarankan: **Pariwisata-Indonesia-2026.pbix**
Tema warna: Marine `#0B3C5D`, aksen merah `#D7263D`, butter `#F4B41A`,
latar oat `#FAF6EF`, teks slate `#22303C`.

## Halaman 1 — Ringkasan Eksekutif
- **Kartu KPI 1:** Kunjungan Wisman 2025 → measure `Kunjungan Wisman 2025` (15,39 jt)
- **Kartu KPI 2:** Tingkat Pemulihan vs 2019 → measure `Tingkat Pemulihan vs 2019`
  dengan konteks tahun 2025 (95,5%)
- **Kartu KPI 3:** Kunjungan Wisman YTD 2026 → measure `Kunjungan Wisman YTD 2026`
  (10,58 jt, Jan–Agu)
- **Kartu KPI 4:** Wisnus 2025 → measure `Wisnus 2025` (1,20 miliar perjalanan)
- **Column chart:** kunjungan tahunan (sumbu: dim_tahun[tahun]; nilai:
  `Total Kunjungan Wisman`) — untuk 2024 gunakan catatan kaki karena bulanan
  2024 hanya Nov–Des; alternatif: pakai fact_wisman_tahunan[kunjungan_wisman]
- **Line chart:** bulanan 2026 (sumbu: dim_bulan[bulan_singkat]; nilai:
  `Total Kunjungan Wisman`; filter tahun = 2026)
- **Donut chart:** pangsa pintu masuk 2025 (legend: fact_wisman_pintu[pintu_masuk];
  nilai: `Pangsa Pintu Masuk`; filter periode = 2025)
- **Slicer:** dim_tahun[tahun], dim_tahun[fase]

## Halaman 2 — Pintu Masuk & Kebangsaan
- **Bar chart terurut:** kunjungan per gerbang (fact_wisman_pintu, filter
  periode dapat diganti: 2019 / 2023 / 2024 / 2025 / Jan–Agu 2026 / Agu 2026)
- **Stacked bar:** kunjungan per moda (fact_wisman_pintu[moda])
- **Clustered column:** kebangsaan 2019 vs 2023 (fact_wisman_kebangsaan;
  filter kebangsaan selain TOTAL SEMUA & Total ASEAN)
- **Bar chart:** kebangsaan Agustus 2026 (filter periode = Agu 2026)
- **Kartu:** Pangsa Pintu Masuk Ngurah Rai periode 2025 (44,9%)
- **Slicer:** fact_wisman_pintu[periode], fact_wisman_kebangsaan[periode]

## Halaman 3 — Hotel: TPK & Lama Menginap
- **Bar chart terurut:** TPK per provinsi (fact_tpk_provinsi; slicer tahun
  2024/2025) — Bali teratas pada 2025 (61,02%)
- **Bar chart snapshot:** TPK Des 2025 per provinsi (fact_tpk_snapshot)
- **Clustered column:** RLM menurut kelompok tamu (fact_rlm; filter
  wilayah = Indonesia; sumbu periode)
- **Kartu:** Rata Rata TPK Provinsi 2025; RLM tamu asing Des 2025 (2,65 malam)
- **Slicer:** fact_tpk_provinsi[tahun], fact_rlm[periode], fact_rlm[wilayah]
- Catatan: visual peta (filled map) boleh ditambahkan manual di Desktop untuk
  TPK provinsi; pada paket PBIP visual peta diganti bar terurut.

## Halaman 4 — Wisatawan Nusantara (Wisnus)
- **Kartu KPI:** Wisnus 2025 (1.200.332.559), Pertumbuhan Wisnus Persen (+17,55%)
- **Bar chart terurut:** 10 provinsi tujuan teratas (fact_wisnus_tujuan;
  filter tahun = 2025)
- **Clustered column:** perbandingan 2024 vs 2025 per provinsi (Top 10)
- **Tabel:** seluruh 38 provinsi dengan perjalanan 2024, 2025, dan
  measure `Pertumbuhan Wisnus Persen` per provinsi (format kondisional)
- **Slicer:** fact_wisnus_tujuan[tahun]

## Relasi model (star schema)
- dim_tahun[tahun] → fact_wisman_bulanan[tahun], fact_wisman_tahunan[tahun],
  fact_tpk_provinsi[tahun], fact_wisnus_tujuan[tahun]
- dim_bulan[bulan_ke] → fact_wisman_bulanan[bulan_ke]
- fact_wisman_pintu, fact_wisman_kebangsaan, fact_rlm, fact_tpk_snapshot
  berdiri sendiri (difilter lewat kolom periode masing-masing)
