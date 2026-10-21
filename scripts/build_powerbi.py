# -*- coding: utf-8 -*-
"""
Membangun kit Power BI di powerbi/: CSV star-schema (grain terpisah),
measures_dax.md (nama measure polos + tabel verifikasi dari angka nyata),
dashboard_layout.md, build_guide.md, dan dashboard_preview_halaman1.png.
Jalankan setelah compile_data.py & analysis.py.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
PBI = os.path.join(ROOT, "powerbi")
os.makedirs(PBI, exist_ok=True)

MARINE = "#0B3C5D"; MARINE_L = "#3E7CA6"; RED = "#D7263D"; BUTTER = "#F4B41A"
SLATE = "#22303C"; GREY = "#8A97A5"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": SLATE,
                     "axes.edgecolor": "#C9CFD6", "axes.labelcolor": SLATE,
                     "xtick.color": SLATE, "ytick.color": SLATE, "font.size": 10})

F = json.load(open(os.path.join(ROOT, "findings.json")))

# ---------------------------------------------------------------- star schema
bulanan = pd.read_csv(os.path.join(DATA, "wisman_bulanan.csv"))
bulanan[["tahun", "bulan_ke", "bulan", "kunjungan_wisman"]].to_csv(
    os.path.join(PBI, "fact_wisman_bulanan.csv"), index=False)

tahunan = pd.read_csv(os.path.join(DATA, "wisman_tahunan.csv"))
tahunan.to_csv(os.path.join(PBI, "fact_wisman_tahunan.csv"), index=False)

pintu = pd.read_csv(os.path.join(DATA, "wisman_pintu_masuk.csv"))
pintu.to_csv(os.path.join(PBI, "fact_wisman_pintu.csv"), index=False)

keb = pd.read_csv(os.path.join(DATA, "wisman_kebangsaan.csv"))
keb.to_csv(os.path.join(PBI, "fact_wisman_kebangsaan.csv"), index=False)

tpk = pd.read_csv(os.path.join(DATA, "tpk_provinsi.csv"))
tpk_long = tpk[tpk.provinsi != "INDONESIA"].melt(
    id_vars="provinsi",
    value_vars=["tpk_bintang_tahunan_2024_persen", "tpk_bintang_tahunan_2025_persen"],
    var_name="kolom", value_name="tpk_persen")
tpk_long["tahun"] = tpk_long.kolom.str.extract(r"(202\d)").astype(int)
tpk_long[["provinsi", "tahun", "tpk_persen"]].sort_values(
    ["tahun", "provinsi"]).to_csv(os.path.join(PBI, "fact_tpk_provinsi.csv"), index=False)
tpk_snap = tpk[tpk.provinsi != "INDONESIA"][["provinsi", "tpk_bintang_des2025_persen"]].copy()
tpk_snap.columns = ["provinsi", "tpk_persen"]
tpk_snap.insert(1, "periode", "Des 2025")
tpk_snap.to_csv(os.path.join(PBI, "fact_tpk_snapshot.csv"), index=False)

rlm = pd.read_csv(os.path.join(DATA, "rlm_tamu.csv"))
rlm.to_csv(os.path.join(PBI, "fact_rlm.csv"), index=False)

wis = pd.read_csv(os.path.join(DATA, "wisnus_provinsi.csv"))
wis = wis[wis.provinsi_tujuan != "INDONESIA"]
wis_long = wis.melt(id_vars="provinsi_tujuan",
                    value_vars=["perjalanan_2024", "perjalanan_2025"],
                    var_name="kolom", value_name="perjalanan")
wis_long["tahun"] = wis_long.kolom.str.extract(r"(202\d)").astype(int)
wis_long = wis_long.rename(columns={"provinsi_tujuan": "provinsi"})
wis_long[["provinsi", "tahun", "perjalanan"]].sort_values(
    ["tahun", "provinsi"]).to_csv(os.path.join(PBI, "fact_wisnus_tujuan.csv"), index=False)

pd.DataFrame({"bulan_ke": range(1, 13),
              "bulan": ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                        "Juli", "Agustus", "September", "Oktober", "November",
                        "Desember"],
              "bulan_singkat": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul",
                                "Agu", "Sep", "Okt", "Nov", "Des"]}).to_csv(
    os.path.join(PBI, "dim_bulan.csv"), index=False)
pd.DataFrame({"tahun": [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
              "fase": ["Prapandemi", "Pandemi", "Pandemi", "Pemulihan",
                       "Pemulihan", "Pemulihan", "Pemulihan", "Pemulihan (YTD)"]}).to_csv(
    os.path.join(PBI, "dim_tahun.csv"), index=False)
print("CSV kit tertulis")

# ------------------------------------------------------------ angka verifikasi
v_bul_2019 = int(bulanan[bulanan.tahun == 2019].kunjungan_wisman.sum())
v_bul_2023 = int(bulanan[bulanan.tahun == 2023].kunjungan_wisman.sum())
v_bul_2026 = int(bulanan[bulanan.tahun == 2026].kunjungan_wisman.sum())
p25 = pintu[pintu.periode.astype(str) == "2025"]
v_ngurah = int(p25[p25.pintu_masuk.str.contains("Ngurah")].kunjungan.iloc[0])
v_tot25 = 15386646
v_pangsa_ngurah = round(v_ngurah / v_tot25 * 100, 1)
v_wis25 = int(wis_long[wis_long.tahun == 2025].perjalanan.sum())
v_wis24 = int(wis_long[wis_long.tahun == 2024].perjalanan.sum())
v_g_wis = round((v_wis25 / v_wis24 - 1) * 100, 2)
tpk25 = tpk_long[tpk_long.tahun == 2025]
v_tpk_avg = round(tpk25.tpk_persen.mean(), 2)
v_tpk_bali = float(tpk25[tpk25.provinsi == "Bali"].tpk_persen.iloc[0])
v_rlm_asing = float(rlm[(rlm.periode == "Des 2025") & (rlm.wilayah == "Indonesia")
                        & (rlm.kelompok_tamu == "Asing")].rata_rata_lama_menginap_malam.iloc[0])

def idnum(x):
    return f"{x:,}".replace(",", ".")

DAX = f"""# Measure DAX — Dashboard Pariwisata Indonesia 2026

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
| Total Kunjungan Wisman | Tahun = 2019 | {idnum(v_bul_2019)} |
| Total Kunjungan Wisman | Tahun = 2023 | {idnum(v_bul_2023)} |
| Total Kunjungan Wisman | Tahun = 2026 (Jan–Agu) | {idnum(v_bul_2026)} |
| Tingkat Pemulihan vs 2019 | Tahun = 2025 (dari tabel tahunan: 15.386.646 / 16.106.954) | 95,5% |
| Pangsa Pintu Masuk | Periode = 2025, Pintu = Ngurah Rai (Bali) | {str(v_pangsa_ngurah).replace('.', ',')}% |
| Wisnus 2025 | (tanpa filter provinsi) | {idnum(v_wis25)} |
| Pertumbuhan Wisnus Persen | (tanpa filter provinsi) | {str(v_g_wis).replace('.', ',')}% |
| Rata Rata TPK Provinsi | Tahun = 2025 | {str(v_tpk_avg).replace('.', ',')} |
| TPK Bali | Tahun = 2025, Provinsi = Bali | {str(v_tpk_bali).replace('.', ',')} |
| RLM Rata Rata | Periode = Des 2025, Wilayah = Indonesia, Kelompok = Asing | {str(v_rlm_asing).replace('.', ',')} malam |

Catatan: total bulanan 2024 hanya memuat November & Desember (bulan lain tidak
dikompilasi — lihat data/SOURCES.md), jadi kartu tahun 2024 pada tabel bulanan
memang tidak penuh; gunakan fact_wisman_tahunan untuk angka setahun penuh 2024.
"""
open(os.path.join(PBI, "measures_dax.md"), "w", encoding="utf-8").write(DAX)

LAYOUT = """# Layout Dashboard Power BI — Pariwisata Indonesia 2026 (4 Halaman)

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
"""
open(os.path.join(PBI, "dashboard_layout.md"), "w", encoding="utf-8").write(LAYOUT)

GUIDE = """# Panduan Membangun Dashboard — Pariwisata Indonesia 2026

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
"""
open(os.path.join(PBI, "build_guide.md"), "w", encoding="utf-8").write(GUIDE)
print("Dokumen kit tertulis")

# ------------------------------------------------------------- pratinjau hal. 1
fig = plt.figure(figsize=(12.8, 7.2))
fig.patch.set_facecolor("#FAF6EF")
axT = fig.add_axes([0.03, 0.90, 0.94, 0.08]); axT.axis("off")
axT.text(0, 0.55, "Pariwisata Indonesia 2026 — Ringkasan Eksekutif", fontsize=19,
         fontweight="bold", color=MARINE, va="center")
axT.text(0, 0.02, "Data kompilasi BPS (BRS & Statistik Kunjungan Wisman) • Halaman 1 dari 4",
         fontsize=10.5, color=SLATE, va="center")
kpis = [("WISMAN 2025", "15,39 jt", "kunjungan setahun penuh"),
        ("PEMULIHAN vs 2019", "95,5%", "dari baseline prapandemi"),
        ("WISMAN JAN–AGU 2026", "10,58 jt", "98,7% dari periode sama 2019"),
        ("WISNUS 2025", "1,20 M", "perjalanan domestik (+17,55%)")]
for i, (lab, val, sub) in enumerate(kpis):
    axc = fig.add_axes([0.03 + i * 0.245, 0.755, 0.225, 0.125])
    axc.axis("off")
    axc.add_patch(plt.Rectangle((0, 0), 1, 1, transform=axc.transAxes,
                                fc="white", ec=MARINE, lw=1.4))
    axc.text(0.06, 0.72, lab, fontsize=9, color=GREY, fontweight="bold", va="center")
    axc.text(0.06, 0.40, val, fontsize=19, color=MARINE, fontweight="bold", va="center")
    axc.text(0.06, 0.12, sub, fontsize=8.2, color=SLATE, va="center")
ax1 = fig.add_axes([0.045, 0.13, 0.42, 0.55])
th = dict(zip(tahunan.tahun, tahunan.kunjungan_wisman))
yrs = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
ax1.bar([str(y) for y in yrs], [th[y] / 1e6 for y in yrs],
        color=[MARINE if y != 2021 else RED for y in yrs], width=0.62, zorder=3)
ax1.set_title("Kunjungan wisman tahunan (juta)", fontsize=11, fontweight="bold", loc="left")
ax1.set_ylim(0, 18)
ax1.grid(axis="x", visible=False)
ax2 = fig.add_axes([0.53, 0.13, 0.42, 0.55])
b26 = bulanan[bulanan.tahun == 2026].sort_values("bulan_ke")
ax2.plot(b26.bulan_ke, b26.kunjungan_wisman / 1e6, color=MARINE, lw=2.4,
         marker="o", ms=5, zorder=3)
ax2.fill_between(b26.bulan_ke, b26.kunjungan_wisman / 1e6, color=MARINE, alpha=0.10)
ax2.set_xticks(range(1, 9))
ax2.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu"])
ax2.set_title("Wisman bulanan 2026 — puncak Agustus 1,60 jt", fontsize=11,
              fontweight="bold", loc="left")
ax2.grid(axis="x", visible=False)
axf = fig.add_axes([0.03, 0.015, 0.94, 0.05]); axf.axis("off")
axf.text(0, 0.5, "Gerbang utama 2025: Ngurah Rai 44,9% • Dua gerbang teratas 62,8% • "
                 "TPK bintang 2025: 49,30% (Bali 61,02%)",
         fontsize=10.5, color=SLATE, va="center")
fig.savefig(os.path.join(PBI, "dashboard_preview_halaman1.png"), dpi=150,
            facecolor="#FAF6EF")
plt.close(fig)
print("Pratinjau tertulis")
