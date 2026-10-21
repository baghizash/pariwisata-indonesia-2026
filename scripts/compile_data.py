# -*- coding: utf-8 -*-
"""
Kompilasi data Pariwisata Indonesia dari publikasi resmi BPS.
Semua angka diketik dari tabel pada publikasi BPS (lihat data/SOURCES.md).
Angka turunan (residual antar kumulatif BPS) ditandai pada kolom 'catatan'.
Jalankan: ~/workspace/mienv/bin/python scripts/compile_data.py
"""
import csv
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(BASE, exist_ok=True)


def write_csv(name, header, rows):
    path = os.path.join(BASE, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} baris")
    return path


# ---------------------------------------------------------------- tahunan
# Sumber: Statistik Kunjungan Wisman 2023 (Lampiran 1 & 3), BRS Des 2024,
# BRS Des 2025 (revisi 2024), BRS Agu 2026 (kumulatif Jan-Agu 2026).
TAHUNAN = [
    # tahun, kunjungan, status
    (2019, 16106954, "Setahun penuh"),
    (2020, 4052923, "Setahun penuh"),
    (2021, 1557530, "Setahun penuh"),
    (2022, 5889031, "Setahun penuh (angka final publikasi BPS; rilis awal BRS menyebut 5,47 juta)"),
    (2023, 11677825, "Setahun penuh"),
    (2024, 13886678, "Setahun penuh (revisi pada BRS Des 2025; angka awal BRS Des 2024: 13.902.420)"),
    (2025, 15386646, "Setahun penuh"),
    (2026, 10578286, "Kumulatif Jan-Agu 2026 (YTD)"),
]
write_csv("wisman_tahunan.csv", ["tahun", "kunjungan_wisman", "status_periode"],
          TAHUNAN)

# ---------------------------------------------------------------- bulanan
BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
            "Agustus", "September", "Oktober", "November", "Desember"]

# Statistik Kunjungan Wisman 2023, Lampiran 1 (baris tahun 2019-2023)
BULANAN_PUBLIKASI = {
    2019: [1201735, 1243996, 1311911, 1274231, 1249536, 1434103,
           1468173, 1530268, 1388719, 1346434, 1280781, 1377067],
    2020: [1290411, 872765, 486155, 158066, 161842, 156561,
           155742, 161549, 148984, 152293, 144476, 164079],
    2021: [126515, 105788, 119979, 112756, 139433, 126844,
           127249, 118533, 120100, 146137, 150577, 163619],
    2022: [136298, 117509, 158629, 230076, 354920, 483883,
           645121, 670509, 700606, 734228, 704783, 952469],
    2023: [798469, 749436, 869244, 865811, 953714, 1062791,
           1121189, 1132638, 1070245, 978519, 931227, 1144542],
}
# BRS Des 2024 (Tabel 1): hanya Nov & Des 2024 yang diambil eksak dari tabel
BULANAN_2024 = {11: 1092067, 12: 1244372}
# 2025: Tabel 1 antar-BRS + residual kumulatif BPS (ditandai)
BULANAN_2025 = {
    1: (1155978, "Turunan: kumulatif Jan-Apr 2025 (BRS Apr 2026) dikurangi Feb-Apr; konsisten dengan narasi BRS 1,16 juta"),
    2: (1022928, "Turunan: Feb 2026 1.159.690 dibagi (1 + 13,37%) dari rilis BPS Feb 2026; konsisten dengan narasi BRS 1,02 juta"),
    3: (984769, "Rilis BPS Mar 2026 (dikutip Kemenpar)"),
    4: (1164539, "BRS Apr 2026, Tabel 1 (kolom bulan yang sama tahun sebelumnya)"),
    5: (1306000, "Turunan: kumulatif Jan-Jun 2025 (BRS Jun 2026) dikurangi Jan-Apr dan Jun 2025"),
    6: (1417096, "BRS Jun 2026, Tabel 1 (kolom bulan yang sama tahun sebelumnya)"),
    7: (1481346, "Turunan: kumulatif Jan-Agu 2025 (BRS Agu 2026) dikurangi Jan-Jun dan Agu 2025"),
    8: (1505220, "BRS Agu 2026, Tabel 1 (kolom bulan yang sama tahun sebelumnya)"),
    11: (1199007, "BRS Des 2025, Tabel 1"),
    12: (1405860, "BRS Des 2025, Tabel 1"),
}
# 2026: rantai Tabel 1 antar-BRS (semua eksak; Jan turunan terverifikasi silang)
BULANAN_2026 = {
    1: (1188420, "Turunan: kumulatif Jan-Feb 2026 (BRS) dikurangi Feb 2026; terverifikasi dari perubahan m-to-m Feb -2,42%"),
    2: (1159690, "Rilis BPS Feb 2026 (1 Apr 2026)"),
    3: (1088166, "BRS Apr 2026, Tabel 1 (kolom bulan sebelumnya)"),
    4: (1248651, "BRS Apr 2026, Tabel 1"),
    5: (1382087, "BRS Jun 2026, Tabel 1 (kolom bulan sebelumnya)"),
    6: (1386575, "BRS Jun 2026, Tabel 1"),
    7: (1525037, "BRS Agu 2026, Tabel 1 (kolom bulan sebelumnya)"),
    8: (1599660, "BRS Agu 2026, Tabel 1"),
}

rows = []
for tahun, vals in BULANAN_PUBLIKASI.items():
    for i, v in enumerate(vals, start=1):
        rows.append((tahun, i, BULAN_ID[i - 1], v, "Statistik Kunjungan Wisman 2023, Lampiran 1"))
for bln, v in BULANAN_2024.items():
    rows.append((2024, bln, BULAN_ID[bln - 1], v, "BRS Des 2024, Tabel 1"))
for bln, (v, note) in BULANAN_2025.items():
    rows.append((2025, bln, BULAN_ID[bln - 1], v, note))
for bln, (v, note) in BULANAN_2026.items():
    rows.append((2026, bln, BULAN_ID[bln - 1], v, note))
rows.sort(key=lambda r: (r[0], r[1]))
write_csv("wisman_bulanan.csv",
          ["tahun", "bulan_ke", "bulan", "kunjungan_wisman", "sumber_catatan"], rows)

# ------------------------------------------------------- pintu masuk (gates)
# Baris: periode, pintu, moda, kunjungan
PINTU = [
    # Statistik Wisman 2023, Lampiran 3 - tahunan 2019 & 2023 (pintu imigrasi)
    ("2019", "Ngurah Rai (Bali)", "Udara", 6239543),
    ("2019", "Soekarno-Hatta (Banten)", "Udara", 2419196),
    ("2019", "Juanda (Jawa Timur)", "Udara", 243899),
    ("2019", "Kualanamu (Sumatera Utara)", "Udara", 244530),
    ("2019", "Batam (Kepulauan Riau)", "Laut", 1947943),
    ("2019", "Tanjung Uban (Kepulauan Riau)", "Laut", 634735),
    ("2023", "Ngurah Rai (Bali)", "Udara", 5248113),
    ("2023", "Soekarno-Hatta (Banten)", "Udara", 1953005),
    ("2023", "Juanda (Jawa Timur)", "Udara", 218458),
    ("2023", "Kualanamu (Sumatera Utara)", "Udara", 196475),
    ("2023", "Batam (Kepulauan Riau)", "Laut", 1185685),
    ("2023", "Tanjung Uban (Kepulauan Riau)", "Laut", 222118),
    # BRS Des 2024 Tabel 1 (Jan-Des 2024) & BRS Des 2025 Tabel 1 (Jan-Des 2025)
    ("2024", "Ngurah Rai (Bali)", "Udara", 6308541),
    ("2024", "Soekarno-Hatta (Banten)", "Udara", 2524253),
    ("2024", "Juanda (Jawa Timur)", "Udara", 322045),
    ("2024", "Kualanamu (Sumatera Utara)", "Udara", 247038),
    ("2024", "Batam (Kepulauan Riau)", "Laut", 1316219),
    ("2024", "Tanjung Uban (Kepulauan Riau)", "Laut", 208605),
    ("2025", "Ngurah Rai (Bali)", "Udara", 6907585),
    ("2025", "Soekarno-Hatta (Banten)", "Udara", 2760838),
    ("2025", "Juanda (Jawa Timur)", "Udara", 329945),
    ("2025", "Kualanamu (Sumatera Utara)", "Udara", 289656),
    ("2025", "Batam (Kepulauan Riau)", "Laut", 1593757),
    ("2025", "Tanjung Uban (Kepulauan Riau)", "Laut", 253366),
    # BRS Agu 2026 Tabel 1 - kumulatif Jan-Agu 2026
    ("Jan-Agu 2026", "Ngurah Rai (Bali)", "Udara", 4571316),
    ("Jan-Agu 2026", "Soekarno-Hatta (Banten)", "Udara", 1909902),
    ("Jan-Agu 2026", "Juanda (Jawa Timur)", "Udara", 236733),
    ("Jan-Agu 2026", "Kualanamu (Sumatera Utara)", "Udara", 205793),
    ("Jan-Agu 2026", "Batam (Kepulauan Riau)", "Laut", 1114612),
    ("Jan-Agu 2026", "Tanjung Uban (Kepulauan Riau)", "Laut", 193045),
    # BRS Agu 2026 Tabel 1 - bulan Agustus 2026 saja
    ("Agu 2026", "Ngurah Rai (Bali)", "Udara", 685956),
    ("Agu 2026", "Soekarno-Hatta (Banten)", "Udara", 323880),
    ("Agu 2026", "Juanda (Jawa Timur)", "Udara", 41024),
    ("Agu 2026", "Kualanamu (Sumatera Utara)", "Udara", 31105),
    ("Agu 2026", "Batam (Kepulauan Riau)", "Laut", 177167),
    ("Agu 2026", "Tanjung Uban (Kepulauan Riau)", "Laut", 29492),
]
write_csv("wisman_pintu_masuk.csv", ["periode", "pintu_masuk", "moda", "kunjungan"], PINTU)

# Ringkasan moda & kelompok pintu per periode (untuk pangsa)
MODA = [
    # periode, kelompok, kunjungan
    ("2019", "Pintu utama - Udara", 9834706),
    ("2019", "Pintu utama - Laut", 2972314),
    ("2019", "Pintu utama - Darat", 228216),
    ("2019", "Pintu perbatasan", 3071718),
    ("2023", "Pintu utama - Udara", 7972651),
    ("2023", "Pintu utama - Laut", 1620626),
    ("2023", "Pintu utama - Darat", 237092),
    ("2023", "Pintu perbatasan", 1847456),
    ("2024", "Pintu utama - Udara", 9830550),
    ("2024", "Pintu utama - Laut", 1787133),
    ("2024", "Pintu utama - Darat", 332665),
    ("2024", "Pintu perbatasan", 1952072),
    ("2025", "Pintu utama (semua moda)", 13443023),
    ("2025", "Pintu perbatasan", 1943623),
]
# Catatan: Tabel 1 BRS Des 2025 yang diekstrak memuat total pintu utama dan
# perbatasan 2025, tetapi rincian per moda 2025 tidak lengkap sehingga tidak
# dikompilasi. Rincian moda tersedia untuk 2019, 2023 (Lampiran 3) dan 2024
# (BRS Des 2024, vintage awal: totalnya 13.902.420, berbeda 0,11% dari angka
# revisi 13.886.678 pada BRS Des 2025).
write_csv("wisman_moda_pintu.csv", ["periode", "kelompok_pintu", "kunjungan"], MODA)

# ------------------------------------------------------------- kebangsaan
KEBANGSAAN_TAHUNAN = [
    # kebangsaan, 2019, 2023  (Statistik Wisman 2023, Lampiran 4)
    ("Malaysia", 2980753, 1901242),
    ("Singapura", 1934445, 1414447),
    ("Australia", 1386803, 1431177),
    ("Tiongkok", 2072079, 787924),
    ("Timor Leste", 1178381, 728586),
    ("India", 657300, 606439),
    ("Jepang", 519623, 251866),
    ("Korea Selatan", 388316, 347185),
    ("Filipina", 260980, 209458),
    ("Total ASEAN", 6157190, 4248750),
    ("TOTAL SEMUA", 16106954, 11677825),
]
rows = []
for nama, v19, v23 in KEBANGSAAN_TAHUNAN:
    rows.append(("2019", nama, v19))
    rows.append(("2023", nama, v23))
# Des 2025 (BRS Des 2025, Tabel 2) - bulan Desember 2025
DES2025 = [("Malaysia", 243162), ("Singapura", 204512), ("Australia", 154868),
           ("Timor Leste", 119098), ("Tiongkok", 100686), ("India", 72872),
           ("Total ASEAN", 677674), ("TOTAL SEMUA", 1405860)]
for nama, v in DES2025:
    rows.append(("Des 2025", nama, v))
# Agu 2026 (BRS Agu 2026, Tabel 2 - menurut paspor)
AGU2026 = [("Malaysia", 296227), ("Australia", 171937), ("Tiongkok", 162568),
           ("Singapura", 131676), ("Timor Leste", 87386), ("India", 52196),
           ("Jepang", 49789), ("Korea Selatan", 49420),
           ("Total ASEAN", 624349), ("TOTAL SEMUA", 1599660)]
for nama, v in AGU2026:
    rows.append(("Agu 2026", nama, v))
write_csv("wisman_kebangsaan.csv", ["periode", "kebangsaan", "kunjungan"], rows)

# Pangsa tahunan 2025 (narasi BRS Des 2025 - hanya pangsa yang dipublikasikan)
write_csv("wisman_kebangsaan_pangsa_2025.csv",
          ["kebangsaan", "pangsa_persen_2025"],
          [("Malaysia", 17.2), ("Singapura", 9.9), ("Total ASEAN", 41.3)])

# ------------------------------------------------------------------- TPK
# BRS Des 2025, Tabel 7: provinsi, TPK tahunan 2024, TPK tahunan 2025, TPK Des 2025
TPK = [
    ("Aceh", 42.58, 25.01, 27.53), ("Sumatera Utara", 48.23, 40.62, 44.43),
    ("Sumatera Barat", 44.40, 43.29, 43.44), ("Riau", 45.00, 44.37, 52.92),
    ("Jambi", 51.73, 49.16, 54.08), ("Sumatera Selatan", 51.85, 47.20, 55.48),
    ("Bengkulu", 46.54, 42.74, 51.57), ("Lampung", 47.28, 43.67, 54.44),
    ("Kep. Bangka Belitung", 29.22, 25.55, 31.28), ("Kepulauan Riau", 56.57, 47.84, 56.96),
    ("DKI Jakarta", 53.28, 53.62, 59.97), ("Jawa Barat", 51.23, 47.16, 58.13),
    ("Jawa Tengah", 46.55, 44.42, 52.47), ("DI Yogyakarta", 55.76, 52.37, 66.38),
    ("Jawa Timur", 53.58, 49.32, 56.32), ("Banten", 52.99, 49.90, 53.39),
    ("Bali", 62.35, 61.02, 60.88), ("Nusa Tenggara Barat", 40.38, 40.46, 41.98),
    ("Nusa Tenggara Timur", 42.48, 42.49, 45.76), ("Kalimantan Barat", 49.87, 49.99, 60.84),
    ("Kalimantan Tengah", 52.18, 48.28, 57.64), ("Kalimantan Selatan", 56.40, 52.92, 59.80),
    ("Kalimantan Timur", 65.09, 53.36, 62.98), ("Kalimantan Utara", 53.03, 46.15, 54.92),
    ("Sulawesi Utara", 47.63, 44.14, 53.30), ("Sulawesi Tengah", 55.03, 48.82, 52.67),
    ("Sulawesi Selatan", 49.64, 44.84, 53.33), ("Sulawesi Tenggara", 40.37, 34.47, 38.62),
    ("Gorontalo", 49.17, 38.92, 42.75), ("Sulawesi Barat", 32.67, 26.25, 30.90),
    ("Maluku", 35.57, 33.38, 40.22), ("Maluku Utara", 44.51, 42.26, 46.39),
    ("Papua Barat", 35.48, 30.93, 39.57), ("Papua Barat Daya", 50.58, 44.68, 61.90),
    ("Papua", 44.27, 40.79, 49.26), ("Papua Selatan", 53.40, 53.40, 52.85),
    ("Papua Tengah", 39.84, 37.62, 47.04), ("Papua Pegunungan", 31.13, 28.57, 43.07),
    ("INDONESIA", 52.57, 49.30, 56.12),
]
write_csv("tpk_provinsi.csv",
          ["provinsi", "tpk_bintang_tahunan_2024_persen", "tpk_bintang_tahunan_2025_persen",
           "tpk_bintang_des2025_persen"], TPK)

# TPK nasional tahunan hotel bintang (BRS Des 2024 & Des 2025)
write_csv("tpk_nasional_tahunan.csv", ["tahun", "tpk_bintang_persen"],
          [(2023, 51.27), (2024, 52.57), (2025, 49.30)])

# ------------------------------------------------------------------- RLM
RLM = [
    # periode, wilayah, tamu, malam
    ("Des 2025", "Indonesia", "Asing", 2.65),
    ("Des 2025", "Indonesia", "Indonesia", 1.46),
    ("Des 2025", "Indonesia", "Total", 1.58),
    ("Des 2025", "Bali", "Asing", 3.21),
    ("Des 2025", "Bali", "Indonesia", 2.48),
    ("Des 2025", "Bali", "Total", 2.91),
    ("Agu 2026", "Indonesia", "Asing", 2.48),
    ("Agu 2026", "Indonesia", "Indonesia", 1.48),
    ("Agu 2026", "Indonesia", "Total", 1.63),
    ("Agu 2026", "Bali", "Total", 2.77),
]
write_csv("rlm_tamu.csv", ["periode", "wilayah", "kelompok_tamu", "rata_rata_lama_menginap_malam"], RLM)

# ----------------------------------------------------------------- wisnus
# BRS Des 2025, Tabel 4: provinsi tujuan, Jan-Des 2024, Jan-Des 2025
WISNUS = [
    ("Aceh", 12924997, 20096350), ("Sumatera Utara", 42766198, 56910262),
    ("Sumatera Barat", 19142418, 22302808), ("Riau", 17992224, 23926171),
    ("Jambi", 8534569, 10877483), ("Sumatera Selatan", 18143118, 26065516),
    ("Bengkulu", 4571903, 7211781), ("Lampung", 17875613, 27090780),
    ("Kep. Bangka Belitung", 3144851, 4511219), ("Kepulauan Riau", 3491947, 4294670),
    ("DKI Jakarta", 87233238, 99396992), ("Jawa Barat", 167396804, 211762921),
    ("Jawa Tengah", 146842040, 146253837), ("DI Yogyakarta", 38030739, 40592837),
    ("Jawa Timur", 218711818, 217197652), ("Banten", 48257848, 62556582),
    ("Bali", 22644939, 26615306), ("Nusa Tenggara Barat", 13769746, 14848407),
    ("Nusa Tenggara Timur", 7983247, 10401869), ("Kalimantan Barat", 8165686, 13192118),
    ("Kalimantan Tengah", 6499070, 11298337), ("Kalimantan Selatan", 11668618, 19017247),
    ("Kalimantan Timur", 12205958, 15683381), ("Kalimantan Utara", 962342, 1698620),
    ("Sulawesi Utara", 8202302, 14537959), ("Sulawesi Tengah", 9329221, 11572179),
    ("Sulawesi Selatan", 36518290, 42530358), ("Sulawesi Tenggara", 12946373, 13272738),
    ("Gorontalo", 3437439, 5280383), ("Sulawesi Barat", 4008524, 4630996),
    ("Maluku", 1856446, 3604744), ("Maluku Utara", 2219681, 3531781),
    ("Papua Barat", 419157, 900522), ("Papua Barat Daya", 917412, 1689495),
    ("Papua", 1269706, 2855407), ("Papua Selatan", 178819, 379854),
    ("Papua Tengah", 441438, 905084), ("Papua Pegunungan", 379292, 837913),
    ("INDONESIA", 1021084031, 1200332559),
]
write_csv("wisnus_provinsi.csv",
          ["provinsi_tujuan", "perjalanan_2024", "perjalanan_2025"], WISNUS)

# Wisnus nasional bulanan (yang terpublikasi eksplisit pada rilis BPS 2026)
WISNUS_BULANAN = [
    (2025, 12, "Desember", 105978131, "BRS Des 2025, Tabel 4 (total)"),
    (2026, 1, "Januari", 102030000, "Turunan: kumulatif Jan-Feb 2026 193,17 juta (rilis BPS Feb 2026) dikurangi Feb 2026; dibulatkan ke 10 ribu"),
    (2026, 2, "Februari", 91140000, "Rilis BPS Feb 2026: 91,14 juta perjalanan"),
    (2026, 3, "Maret", 126340000, "Rilis BPS Mar 2026: 126,34 juta perjalanan"),
    (2026, 4, "April", 97550000, "Rilis BPS Apr 2026: 97,55 juta perjalanan"),
    (2026, 8, "Agustus", 104300000, "BRS Agu 2026: 104,30 juta perjalanan"),
]
write_csv("wisnus_bulanan.csv",
          ["tahun", "bulan_ke", "bulan", "perjalanan", "sumber_catatan"], WISNUS_BULANAN)

print("Selesai. Semua CSV tertulis di", BASE)
