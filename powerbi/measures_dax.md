# Measure DAX — Dashboard Pariwisata Indonesia 2026

Semua nama measure memakai **teks polos** (tanpa tanda "=" dan tanpa karakter
khusus di dalam nama). Salin rumus apa adanya ke Power BI Desktop
(Home → New measure), lalu atur format angkanya sesuai kolom Format.

## 1. Total Kunjungan Wisman
Menghitung total kunjungan dari tabel bulanan (hormati filter tahun & bulan).

```dax
Total Kunjungan Wisman =
SUM ( fact_wisman_bulanan[kunjungan_wisman] )
```

## 2. Total Kunjungan Tahunan
Total dari tabel tahunan — sumber yang benar untuk angka setahun penuh
(tabel bulanan 2024/2025 tidak lengkap, lihat catatan di akhir dokumen).

```dax
Total Kunjungan Tahunan =
SUM ( fact_wisman_tahunan[kunjungan_wisman] )
```

## 3. Kunjungan Wisman 2019
Baseline prapandemi dari tabel tahunan, kebal terhadap filter tahun slicer.

```dax
Kunjungan Wisman 2019 =
CALCULATE ( [Total Kunjungan Tahunan], fact_wisman_tahunan[tahun] = 2019 )
```

## 4. Kunjungan Wisman 2025
Tahun penuh terakhir yang sudah final, dari tabel tahunan.

```dax
Kunjungan Wisman 2025 =
CALCULATE ( [Total Kunjungan Tahunan], fact_wisman_tahunan[tahun] = 2025 )
```

## 5. Tingkat Pemulihan vs 2019
Format: Percentage (1 desimal). Memakai tabel tahunan; aktifkan konteks
tahun yang ingin dibandingkan (mis. filter tahun = 2025 menghasilkan 95,5%).

```dax
Tingkat Pemulihan vs 2019 =
DIVIDE ( [Total Kunjungan Tahunan], [Kunjungan Wisman 2019] )
```

## 6. Kunjungan Wisman YTD 2026
Kumulatif Januari–Agustus 2026 dari tabel tahunan.

```dax
Kunjungan Wisman YTD 2026 =
CALCULATE (
    SUM ( fact_wisman_tahunan[kunjungan_wisman] ),
    fact_wisman_tahunan[tahun] = 2026
)
```

## 7. Total Kunjungan Pintu Masuk

```dax
Total Kunjungan Pintu =
SUM ( fact_wisman_pintu[kunjungan] )
```

## 8. Pangsa Pintu Masuk
Format: Percentage (1 desimal). Pangsa tiap gerbang terhadap total pada
periode yang sama (filter periode wajib aktif).

```dax
Pangsa Pintu Masuk =
DIVIDE (
    [Total Kunjungan Pintu],
    CALCULATE ( [Total Kunjungan Pintu], ALL ( fact_wisman_pintu[pintu_masuk] ) )
)
```

## 9. Total Perjalanan Wisnus

```dax
Total Perjalanan Wisnus =
SUM ( fact_wisnus_tujuan[perjalanan] )
```

## 10. Wisnus 2024 dan Wisnus 2025

```dax
Wisnus 2024 =
CALCULATE ( [Total Perjalanan Wisnus], fact_wisnus_tujuan[tahun] = 2024 )

Wisnus 2025 =
CALCULATE ( [Total Perjalanan Wisnus], fact_wisnus_tujuan[tahun] = 2025 )
```

## 11. Pertumbuhan Wisnus Persen
Format: Percentage (2 desimal).

```dax
Pertumbuhan Wisnus Persen =
DIVIDE ( [Wisnus 2025] - [Wisnus 2024], [Wisnus 2024] )
```

## 12. Rata Rata TPK Provinsi
Rata-rata sederhana TPK antarprovinsi pada konteks tahun terpilih.
Format: Number (2 desimal).

```dax
Rata Rata TPK Provinsi =
AVERAGE ( fact_tpk_provinsi[tpk_persen] )
```

## 13. RLM Rata Rata
Rata-rata lama menginap (malam) sesuai filter periode, wilayah, kelompok tamu.

```dax
RLM Rata Rata =
AVERAGE ( fact_rlm[rata_rata_lama_menginap_malam] )
```

## Tabel Verifikasi (bandingkan dengan hasil kartu di Power BI)

| Pemeriksaan | Filter yang dipakai | Nilai yang benar |
|---|---|---|
| Total Kunjungan Wisman | Tahun = 2019 | 16.106.954 |
| Total Kunjungan Wisman | Tahun = 2023 | 11.677.825 |
| Total Kunjungan Wisman | Tahun = 2026 (Jan–Agu) | 10.578.286 |
| Tingkat Pemulihan vs 2019 | Tahun = 2025 (dari tabel tahunan: 15.386.646 / 16.106.954) | 95,5% |
| Pangsa Pintu Masuk | Periode = 2025, Pintu = Ngurah Rai (Bali) | 44,9% |
| Wisnus 2025 | (tanpa filter provinsi) | 1.200.332.559 |
| Pertumbuhan Wisnus Persen | (tanpa filter provinsi) | 17,55% |
| Rata Rata TPK Provinsi | Tahun = 2025 | 43,42 |
| TPK Bali | Tahun = 2025, Provinsi = Bali | 61,02 |
| RLM Rata Rata | Periode = Des 2025, Wilayah = Indonesia, Kelompok = Asing | 2,65 malam |

Catatan: total bulanan 2024 hanya memuat November & Desember (bulan lain tidak
dikompilasi — lihat data/SOURCES.md), jadi kartu tahun 2024 pada tabel bulanan
memang tidak penuh; gunakan fact_wisman_tahunan untuk angka setahun penuh 2024.
