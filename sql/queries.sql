-- ============================================================
-- Kueri analitik Pariwisata Indonesia 2026 (dialek SQLite)
-- Tabel mengikuti nama berkas CSV di folder data/:
--   wisman_tahunan, wisman_bulanan, wisman_pintu_masuk,
--   wisman_kebangsaan, tpk_provinsi, wisnus_provinsi, rlm_tamu
-- ============================================================

-- 1. Tingkat pemulihan wisman terhadap baseline 2019 (per tahun penuh)
SELECT t.tahun,
       t.kunjungan_wisman,
       ROUND(100.0 * t.kunjungan_wisman / b.kunjungan_wisman, 1) AS pemulihan_persen
FROM wisman_tahunan t
CROSS JOIN (SELECT kunjungan_wisman FROM wisman_tahunan WHERE tahun = 2019) b
WHERE t.status_periode LIKE 'Setahun penuh%'
ORDER BY t.tahun;
-- Hasil kunci: 2021 = 9,7% (titik terendah), 2025 = 95,5%

-- 2. Pertumbuhan tahunan (year-on-year)
SELECT tahun,
       kunjungan_wisman,
       ROUND(100.0 * (kunjungan_wisman - LAG(kunjungan_wisman) OVER (ORDER BY tahun))
             / LAG(kunjungan_wisman) OVER (ORDER BY tahun), 2) AS yoy_persen
FROM wisman_tahunan
WHERE status_periode LIKE 'Setahun penuh%';
-- Hasil kunci: 2022 = +278,10%, 2025 = +10,80%

-- 3. Pemeriksaan konsistensi: jumlah bulanan 2026 = kumulatif resmi Jan-Agu
SELECT SUM(kunjungan_wisman) AS total_jan_agu_2026
FROM wisman_bulanan
WHERE tahun = 2026;
-- Harus menghasilkan 10578286

-- 4. Pangsa gerbang utama terhadap total nasional 2025
SELECT pintu_masuk,
       kunjungan,
       ROUND(100.0 * kunjungan / 15386646, 2) AS pangsa_persen
FROM wisman_pintu_masuk
WHERE periode = '2025'
ORDER BY kunjungan DESC;
-- Hasil kunci: Ngurah Rai = 44,89%

-- 5. Pemulihan per kebangsaan: 2023 vs 2019
SELECT a.kebangsaan,
       a.kunjungan AS kunjungan_2019,
       b.kunjungan AS kunjungan_2023,
       ROUND(100.0 * b.kunjungan / a.kunjungan, 1) AS pemulihan_persen
FROM wisman_kebangsaan a
JOIN wisman_kebangsaan b
  ON b.kebangsaan = a.kebangsaan AND b.periode = '2023'
WHERE a.periode = '2019'
  AND a.kebangsaan NOT IN ('TOTAL SEMUA', 'Total ASEAN')
ORDER BY pemulihan_persen DESC;
-- Hasil kunci: Australia 103,2% tertinggi, Tiongkok 38,0% terendah

-- 6. Peringkat TPK hotel bintang 2025 (10 tertinggi)
SELECT provinsi, tpk_bintang_tahunan_2025_persen
FROM tpk_provinsi
WHERE provinsi <> 'INDONESIA'
ORDER BY tpk_bintang_tahunan_2025_persen DESC
LIMIT 10;
-- Hasil kunci: Bali 61,02% di puncak

-- 7. Provinsi dengan penurunan TPK tahunan terdalam 2024 -> 2025
SELECT provinsi,
       tpk_bintang_tahunan_2024_persen,
       tpk_bintang_tahunan_2025_persen,
       ROUND(tpk_bintang_tahunan_2025_persen - tpk_bintang_tahunan_2024_persen, 2) AS perubahan_poin
FROM tpk_provinsi
WHERE provinsi <> 'INDONESIA'
ORDER BY perubahan_poin ASC
LIMIT 5;
-- Hasil kunci: Aceh turun 17,57 poin

-- 8. Pertumbuhan wisnus per provinsi tujuan 2024 -> 2025 (10 tercepat, provinsi >= 5 jt perjalanan 2024)
SELECT provinsi_tujuan,
       perjalanan_2024,
       perjalanan_2025,
       ROUND(100.0 * (perjalanan_2025 - perjalanan_2024) / perjalanan_2024, 2) AS pertumbuhan_persen
FROM wisnus_provinsi
WHERE provinsi_tujuan <> 'INDONESIA' AND perjalanan_2024 >= 5000000
ORDER BY pertumbuhan_persen DESC
LIMIT 10;
-- Hasil kunci: Kalimantan Tengah +73,85%, Kalimantan Selatan +62,98%

-- 9. Pangsa Pulau Jawa pada perjalanan wisnus 2025
SELECT ROUND(100.0 * SUM(perjalanan_2025) /
       (SELECT perjalanan_2025 FROM wisnus_provinsi WHERE provinsi_tujuan = 'INDONESIA'), 1)
       AS pangsa_jawa_persen
FROM wisnus_provinsi
WHERE provinsi_tujuan IN ('Jawa Timur', 'Jawa Barat', 'Jawa Tengah',
                          'DI Yogyakarta', 'DKI Jakarta', 'Banten');
-- Hasil: 64,8%

-- 10. Selisih lama menginap tamu asing vs Indonesia (Des 2025)
SELECT periode,
       MAX(CASE WHEN kelompok_tamu = 'Asing' THEN rata_rata_lama_menginap_malam END) AS tamu_asing,
       MAX(CASE WHEN kelompok_tamu = 'Indonesia' THEN rata_rata_lama_menginap_malam END) AS tamu_indonesia
FROM rlm_tamu
WHERE wilayah = 'Indonesia'
GROUP BY periode;
-- Hasil kunci: Des 2025 -> 2,65 vs 1,46 malam
