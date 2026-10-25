# -*- coding: utf-8 -*-
"""
Analisis Pariwisata Indonesia 2026 — membaca CSV kompilasi BPS di data/,
menghitung findings.json dan membuat chart PNG berlabel Bahasa Indonesia.
Jalankan: ~/workspace/mienv/bin/python scripts/analysis.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
CHARTS = os.path.join(ROOT, "charts")
os.makedirs(CHARTS, exist_ok=True)

# Palet (kombinasi favorit user #1: marine blue + bright red + butter yellow di atas oat)
MARINE = "#0B3C5D"
MARINE_L = "#3E7CA6"
RED = "#D7263D"
BUTTER = "#F4B41A"
OAT = "#FAF6EF"
SLATE = "#22303C"
GREY = "#8A97A5"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": SLATE, "axes.edgecolor": "#C9CFD6",
    "axes.labelcolor": SLATE, "xtick.color": SLATE, "ytick.color": SLATE,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.grid": True, "grid.color": "#E4E8ED", "grid.linewidth": 0.7,
    "font.size": 10,
})


def fmt_jt(x):
    return f"{x/1e6:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " jt"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, name), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("chart:", name)


# ------------------------------------------------------------------ muat data
tahunan = pd.read_csv(os.path.join(DATA, "wisman_tahunan.csv"))
bulanan = pd.read_csv(os.path.join(DATA, "wisman_bulanan.csv"))
pintu = pd.read_csv(os.path.join(DATA, "wisman_pintu_masuk.csv"))
moda = pd.read_csv(os.path.join(DATA, "wisman_moda_pintu.csv"))
keb = pd.read_csv(os.path.join(DATA, "wisman_kebangsaan.csv"))
tpk = pd.read_csv(os.path.join(DATA, "tpk_provinsi.csv"))
tpk_nat = pd.read_csv(os.path.join(DATA, "tpk_nasional_tahunan.csv"))
rlm = pd.read_csv(os.path.join(DATA, "rlm_tamu.csv"))
wisnus = pd.read_csv(os.path.join(DATA, "wisnus_provinsi.csv"))

# ------------------------------------------------------------- verifikasi dasar
for thn in [2019, 2020, 2021, 2022, 2023]:
    s = bulanan[bulanan.tahun == thn].kunjungan_wisman.sum()
    t = tahunan[tahunan.tahun == thn].kunjungan_wisman.iloc[0]
    assert s == t, f"Bulanan {thn} tidak cocok: {s} vs {t}"
s26 = bulanan[bulanan.tahun == 2026].kunjungan_wisman.sum()
assert s26 == 10578286, f"Jan-Agu 2026 tidak cocok: {s26}"
prov_sum = wisnus[wisnus.provinsi_tujuan != "INDONESIA"].perjalanan_2025.sum()
indo_row = wisnus[wisnus.provinsi_tujuan == "INDONESIA"].perjalanan_2025.iloc[0]
print(f"Cek wisnus: jumlah provinsi 2025 = {prov_sum:,} vs baris INDONESIA = {indo_row:,}")

F = {}
th = dict(zip(tahunan.tahun, tahunan.kunjungan_wisman))
base19 = th[2019]
F["wisman_tahunan"] = {int(k): int(v) for k, v in th.items()}
F["pemulihan_vs_2019_persen"] = {
    int(k): round(v / base19 * 100, 1) for k, v in th.items() if k != 2026}
F["pertumbuhan_yoy_persen"] = {
    int(k): round((th[k] / th[k - 1] - 1) * 100, 2)
    for k in [2020, 2021, 2022, 2023, 2024, 2025] if k - 1 in th}
F["penurunan_2021_vs_2019_persen"] = round((th[2021] / base19 - 1) * 100, 1)
jan_agu_2019 = bulanan[bulanan.tahun == 2019].nlargest(8, "bulan_ke").kunjungan_wisman.sum()
jan_agu_2019 = bulanan[(bulanan.tahun == 2019) & (bulanan.bulan_ke <= 8)].kunjungan_wisman.sum()
F["ytd_2026_vs_2019_persen"] = round(th[2026] / jan_agu_2019 * 100, 1)
F["jan_agu_2019"] = int(jan_agu_2019)

b26 = bulanan[bulanan.tahun == 2026].sort_values("bulan_ke")
F["bulanan_2026"] = {r.bulan: int(r.kunjungan_wisman) for r in b26.itertuples()}
F["puncak_2026"] = {"bulan": b26.loc[b26.kunjungan_wisman.idxmax(), "bulan"],
                     "kunjungan": int(b26.kunjungan_wisman.max())}
F["lembah_2026"] = {"bulan": b26.loc[b26.kunjungan_wisman.idxmin(), "bulan"],
                    "kunjungan": int(b26.kunjungan_wisman.min())}
b23 = bulanan[bulanan.tahun == 2023]
F["puncak_2023"] = {"bulan": b23.loc[b23.kunjungan_wisman.idxmax(), "bulan"],
                    "kunjungan": int(b23.kunjungan_wisman.max())}

# Indeks musiman: pangsa rata-rata per bulan dari total tahun (2019 & 2023)
piv = bulanan[bulanan.tahun.isin([2019, 2023])].pivot_table(
    index="bulan_ke", columns="tahun", values="kunjungan_wisman")
share = piv.div(piv.sum(axis=0), axis=1) * 100
indeks = (share.mean(axis=1) / share.mean(axis=1).mean() * 100).round(1)
F["indeks_musiman"] = {bulanan[bulanan.bulan_ke == i].bulan.iloc[0]: float(v)
                       for i, v in indeks.items()}

# Pintu masuk 2025
p25 = pintu[pintu.periode == "2025"].copy()
tot25 = th[2025]
p25["pangsa"] = p25.kunjungan / tot25 * 100
F["pintu_2025"] = {r.pintu_masuk: {"kunjungan": int(r.kunjungan),
                                   "pangsa_persen": round(r.pangsa, 2)}
                   for r in p25.itertuples()}
F["pangsa_ngurah_rai_2025"] = round(
    p25[p25.pintu_masuk.str.contains("Ngurah")].kunjungan.iloc[0] / tot25 * 100, 1)
F["pangsa_top2_2025"] = round(p25.nlargest(2, "kunjungan").kunjungan.sum() / tot25 * 100, 1)
F["pangsa_6_gerbang_2025"] = round(p25.kunjungan.sum() / tot25 * 100, 1)
m25 = moda[moda.periode.astype(str) == "2025"]
F["pangsa_pintu_utama_2025"] = round(
    m25[m25.kelompok_pintu.str.contains("utama")].kunjungan.iloc[0] / tot25 * 100, 1)

# Kebangsaan: pemulihan 2023 vs 2019
k19 = keb[keb.periode == "2019"].set_index("kebangsaan").kunjungan
k23 = keb[keb.periode == "2023"].set_index("kebangsaan").kunjungan
negara = [n for n in k19.index if n not in ("TOTAL SEMUA", "Total ASEAN")]
F["kebangsaan_pemulihan_2023"] = {
    n: round(k23[n] / k19[n] * 100, 1) for n in negara}
F["pangsa_asean"] = {"2019": round(k19["Total ASEAN"] / k19["TOTAL SEMUA"] * 100, 1),
                     "2023": round(k23["Total ASEAN"] / k23["TOTAL SEMUA"] * 100, 1),
                     "2025": 41.3}
k26 = keb[keb.periode == "Agu 2026"].set_index("kebangsaan").kunjungan
F["kebangsaan_agu2026_pangsa"] = {
    n: round(v / k26["TOTAL SEMUA"] * 100, 2) for n, v in k26.items()
    if n != "TOTAL SEMUA"}

# TPK
tp = tpk[tpk.provinsi != "INDONESIA"].copy()
F["tpk_nasional"] = {int(r.tahun): float(r.tpk_bintang_persen)
                     for r in tpk_nat.itertuples()}
F["tpk_2025_tertinggi"] = {"provinsi": tp.loc[tp.tpk_bintang_tahunan_2025_persen.idxmax(), "provinsi"],
                           "nilai": float(tp.tpk_bintang_tahunan_2025_persen.max())}
F["tpk_2025_terendah"] = {"provinsi": tp.loc[tp.tpk_bintang_tahunan_2025_persen.idxmin(), "provinsi"],
                          "nilai": float(tp.tpk_bintang_tahunan_2025_persen.min())}
F["tpk_bali_2025"] = float(tp[tp.provinsi == "Bali"].tpk_bintang_tahunan_2025_persen.iloc[0])
F["tpk_des2025_tertinggi"] = {"provinsi": tp.loc[tp.tpk_bintang_des2025_persen.idxmax(), "provinsi"],
                              "nilai": float(tp.tpk_bintang_des2025_persen.max())}

# Wisnus
w = wisnus[wisnus.provinsi_tujuan != "INDONESIA"].copy()
tot_w25 = int(indo_row)
F["wisnus_total_2025"] = tot_w25
F["wisnus_total_2024"] = int(wisnus[wisnus.provinsi_tujuan == "INDONESIA"].perjalanan_2024.iloc[0])
F["wisnus_pertumbuhan_2025_persen"] = round((tot_w25 / F["wisnus_total_2024"] - 1) * 100, 2)
F["rasio_wisnus_wisman_2025"] = round(tot_w25 / tot25, 1)
top_w = w.nlargest(5, "perjalanan_2025")
F["wisnus_top5_2025"] = {r.provinsi_tujuan: int(r.perjalanan_2025) for r in top_w.itertuples()}
jawa = ["Jawa Timur", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "DKI Jakarta", "Banten"]
F["pangsa_jawa_wisnus_2025"] = round(
    w[w.provinsi_tujuan.isin(jawa)].perjalanan_2025.sum() / tot_w25 * 100, 1)
F["wisnus_bali_2025"] = int(w[w.provinsi_tujuan == "Bali"].perjalanan_2025.iloc[0])

r_id = rlm[(rlm.periode == "Des 2025") & (rlm.wilayah == "Indonesia")].set_index("kelompok_tamu")
F["rlm_des2025"] = {k: float(v) for k, v in r_id.rata_rata_lama_menginap_malam.items()}

with open(os.path.join(ROOT, "findings.json"), "w", encoding="utf-8") as f:
    json.dump(F, f, indent=2, ensure_ascii=False)
print("findings.json tertulis")

# --------------------------------------------------------------------- chart 1
fig, ax = plt.subplots(figsize=(9.2, 4.6))
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
vals = [th[y] / 1e6 for y in years]
colors = [MARINE if y != 2021 else RED for y in years]
ax.bar([str(y) for y in years], vals, color=colors, width=0.62, zorder=3)
for i, v in enumerate(vals):
    ax.annotate(f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                (i, v + 0.45), ha="center", fontsize=10, fontweight="bold")
ax.axhline(th[2019] / 1e6, color=RED, ls="--", lw=1.2, zorder=2)
ax.annotate("Baseline 2019: 16,11 jt", (6.45, th[2019] / 1e6 + 0.4),
            ha="right", color=RED, fontsize=9)
ax.bar(["2026\n(Jan–Agu)"], [th[2026] / 1e6], color=BUTTER, width=0.62, zorder=3)
ax.annotate("10,58", (7, th[2026] / 1e6 + 0.45), ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Juta kunjungan")
ax.set_title("Kunjungan Wisman ke Indonesia, 2019–2026\nKolaps pandemi 2021 lalu pulih bertahap (2025 = 95,5% dari 2019)",
             fontsize=12, fontweight="bold", loc="left")
ax.set_ylim(0, 18.2)
ax.grid(axis="x", visible=False)
save(fig, "01_tren_tahunan.png")

# --------------------------------------------------------------------- chart 2
fig, ax = plt.subplots(figsize=(9.2, 4.4))
rec_years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
rec = [100.0] + [F["pemulihan_vs_2019_persen"][y] for y in rec_years[1:]]
ax.plot(rec_years, rec, color=MARINE, lw=2.6, marker="o", ms=7, zorder=3)
ax.fill_between(rec_years, rec, color=MARINE, alpha=0.10)
ax.axhline(100, color=RED, ls="--", lw=1.2)
for x, v in zip(rec_years, rec):
    ax.annotate(f"{v:.1f}%".replace(".", ","), (x, v + 4), ha="center",
                fontsize=10, fontweight="bold")
ax.annotate("YTD Jan–Agu 2026 = 98,7% dari periode sama 2019", (2023.1, 30),
            fontsize=9.5, color=SLATE,
            bbox=dict(boxstyle="round,pad=0.35", fc=BUTTER, ec="none", alpha=0.55))
ax.set_ylabel("% terhadap 2019")
ax.set_title("Tingkat Pemulihan Wisman terhadap Baseline 2019",
             fontsize=12, fontweight="bold", loc="left")
ax.set_ylim(0, 118)
ax.set_xticks(rec_years)
ax.grid(axis="x", visible=False)
save(fig, "02_kurva_pemulihan.png")

# --------------------------------------------------------------------- chart 3
fig, ax = plt.subplots(figsize=(9.6, 4.6))
for yr, c, lw in [(2019, MARINE, 2.4), (2020, RED, 2.0), (2021, "#B0413E", 2.0),
                  (2022, BUTTER, 2.0), (2023, MARINE_L, 2.4)]:
    d = bulanan[bulanan.tahun == yr].sort_values("bulan_ke")
    ax.plot(d.bulan_ke, d.kunjungan_wisman / 1e6, label=str(yr), color=c, lw=lw,
            marker="o", ms=3.5)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu",
                    "Sep", "Okt", "Nov", "Des"])
ax.set_ylabel("Juta kunjungan per bulan")
ax.set_title("Wisman Bulanan 2019–2023: Jurang Pandemi dan Tangga Pemulihan",
             fontsize=12, fontweight="bold", loc="left")
ax.legend(ncol=5, frameon=False, loc="upper left")
ax.grid(axis="x", visible=False)
save(fig, "03_bulanan_2019_2023.png")

# --------------------------------------------------------------------- chart 4
fig, ax = plt.subplots(figsize=(9.2, 4.5))
d26 = bulanan[bulanan.tahun == 2026].sort_values("bulan_ke")
d25 = bulanan[bulanan.tahun == 2025].sort_values("bulan_ke")
ax.bar(d26.bulan_ke - 0.2, d26.kunjungan_wisman / 1e6, width=0.4, color=MARINE,
       label="2026", zorder=3)
ax.bar(d25.bulan_ke + 0.2, d25.kunjungan_wisman / 1e6, width=0.4, color=GREY,
       label="2025", zorder=3)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu",
                    "Sep", "Okt", "Nov", "Des"])
ax.set_ylabel("Juta kunjungan")
ax.set_title("Wisman Bulanan 2026 vs 2025 — Puncak Musiman di Agustus (1,60 jt)",
             fontsize=12, fontweight="bold", loc="left")
ax.legend(frameon=False)
ax.grid(axis="x", visible=False)
save(fig, "04_bulanan_2026_vs_2025.png")

# --------------------------------------------------------------------- chart 5
fig, ax = plt.subplots(figsize=(9.2, 4.2))
bulan_lbl = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep",
             "Okt", "Nov", "Des"]
vals_idx = [indeks[i] for i in range(1, 13)]
cols = [RED if v == max(vals_idx) else MARINE for v in vals_idx]
ax.bar(bulan_lbl, vals_idx, color=cols, width=0.62, zorder=3)
ax.axhline(100, color=SLATE, ls="--", lw=1.1)
for i, v in enumerate(vals_idx):
    ax.annotate(f"{v:.0f}", (i, v + 2.5), ha="center", fontsize=9, fontweight="bold")
ax.set_ylabel("Indeks (rata-rata = 100)")
ax.set_title("Indeks Musiman Wisman (rata-rata 2019 & 2023)\nAgustus teratas; Februari–Maret terendah",
             fontsize=12, fontweight="bold", loc="left")
ax.set_ylim(0, 128)
ax.grid(axis="x", visible=False)
save(fig, "05_indeks_musiman.png")

# --------------------------------------------------------------------- chart 6
fig, ax = plt.subplots(figsize=(9.2, 4.6))
p = p25.sort_values("kunjungan")
ax.barh(p.pintu_masuk, p.kunjungan / 1e6,
        color=[RED if "Ngurah" in n else MARINE for n in p.pintu_masuk], zorder=3)
for i, (v, s) in enumerate(zip(p.kunjungan, p.pangsa)):
    ax.annotate(f"{v/1e6:,.2f} jt ({s:.1f}%)".replace(",", "X").replace(".", ",").replace("X", "."),
                (v / 1e6 + 0.18, i), va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("Juta kunjungan, Jan–Des 2025")
ax.set_title("Enam Gerbang Utama Wisman 2025 — Ngurah Rai Sendirian 44,9% dari Total Nasional",
             fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 8.6)
ax.grid(axis="y", visible=False)
save(fig, "06_pintu_masuk_2025.png")

# --------------------------------------------------------------------- chart 7
fig, ax = plt.subplots(figsize=(6.8, 4.6))
labels = ["Ngurah Rai", "Soekarno-Hatta", "Batam", "Gerbang utama lain",
          "Pintu perbatasan"]
ng = p25[p25.pintu_masuk.str.contains("Ngurah")].kunjungan.iloc[0]
so = p25[p25.pintu_masuk.str.contains("Soekarno")].kunjungan.iloc[0]
ba = p25[p25.pintu_masuk.str.contains("Batam")].kunjungan.iloc[0]
main_tot = m25[m25.kelompok_pintu.str.contains("utama")].kunjungan.iloc[0]
lain = main_tot - ng - so - ba
bord = m25[m25.kelompok_pintu.str.contains("perbatasan")].kunjungan.iloc[0]
vals = [ng, so, ba, lain, bord]
ax.pie(vals, labels=labels, colors=[MARINE, MARINE_L, RED, BUTTER, GREY],
       autopct="%1.1f%%", pctdistance=0.78, startangle=90,
       wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
       textprops={"fontsize": 9.5})
ax.set_title("Komposisi Pintu Kedatangan Wisman 2025 (total 15,39 jt)",
             fontsize=12, fontweight="bold")
save(fig, "07_komposisi_pintu_2025.png")

# --------------------------------------------------------------------- chart 8
fig, ax = plt.subplots(figsize=(9.4, 4.8))
neg = ["Malaysia", "Tiongkok", "Singapura", "Australia", "Timor Leste", "India"]
x = range(len(neg))
ax.bar([i - 0.2 for i in x], [k19[n] / 1e6 for n in neg], width=0.4,
       color=GREY, label="2019", zorder=3)
ax.bar([i + 0.2 for i in x], [k23[n] / 1e6 for n in neg], width=0.4,
       color=MARINE, label="2023", zorder=3)
ax.set_xticks(list(x))
ax.set_xticklabels(neg)
ax.set_ylabel("Juta kunjungan per tahun")
ax.set_title("Kebangsaan Teratas: 2019 vs 2023\nAustralia sudah lampaui 2019; Tiongkok baru pulih 38,0%",
             fontsize=12, fontweight="bold", loc="left")
ax.legend(frameon=False)
ax.grid(axis="x", visible=False)
save(fig, "08_kebangsaan_2019_2023.png")

# --------------------------------------------------------------------- chart 9
fig, ax = plt.subplots(figsize=(9.2, 4.5))
k26s = keb[(keb.periode == "Agu 2026") &
           (~keb.kebangsaan.isin(["TOTAL SEMUA", "Total ASEAN"]))].sort_values("kunjungan")
ax.barh(k26s.kebangsaan, k26s.kunjungan / 1e3,
        color=[RED if n == "Malaysia" else MARINE for n in k26s.kebangsaan], zorder=3)
for i, v in enumerate(k26s.kunjungan):
    ax.annotate(f"{v/1e3:,.1f} rb".replace(",", "X").replace(".", ",").replace("X", "."),
                (v / 1e3 + 6, i), va="center", fontsize=9.5, fontweight="bold")
ax.set_xlabel("Ribu kunjungan, Agustus 2026")
ax.set_title("Kebangsaan Teratas Agustus 2026 — Malaysia 18,5%; ASEAN total 39,0%",
             fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 345)
ax.grid(axis="y", visible=False)
save(fig, "09_kebangsaan_agu2026.png")

# -------------------------------------------------------------------- chart 10
fig, ax = plt.subplots(figsize=(9.4, 5.4))
top10 = tp.nlargest(10, "tpk_bintang_tahunan_2025_persen")
bot5 = tp.nsmallest(5, "tpk_bintang_tahunan_2025_persen")
sub = pd.concat([top10, bot5]).sort_values("tpk_bintang_tahunan_2025_persen")
cols = []
for n in sub.provinsi:
    cols.append(RED if n in set(bot5.provinsi) else (BUTTER if n == "Bali" else MARINE))
ax.barh(sub.provinsi, sub.tpk_bintang_tahunan_2025_persen, color=cols, zorder=3)
ax.axvline(49.30, color=SLATE, ls="--", lw=1.1)
ax.annotate("Nasional 49,30%", (49.8, len(sub) - 0.6), fontsize=9.5)
for i, v in enumerate(sub.tpk_bintang_tahunan_2025_persen):
    ax.annotate(f"{v:.2f}%".replace(".", ","), (v + 0.8, i), va="center",
                fontsize=9.5, fontweight="bold")
ax.set_xlabel("TPK hotel bintang, rata-rata Jan–Des 2025 (%)")
ax.set_title("TPK Hotel Bintang per Provinsi 2025: 10 Tertinggi & 5 Terendah\nBali tertinggi (61,02%); Aceh terendah (25,01%)",
             fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 68)
ax.grid(axis="y", visible=False)
save(fig, "10_tpk_provinsi_2025.png")

# -------------------------------------------------------------------- chart 11
fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.2))
ax = axes[0]
yrs = [2023, 2024, 2025]
ax.bar([str(y) for y in yrs], [F["tpk_nasional"][y] for y in yrs],
       color=[MARINE_L, MARINE, RED], width=0.55, zorder=3)
for i, y in enumerate(yrs):
    ax.annotate(f"{F['tpk_nasional'][y]:.2f}%".replace(".", ","),
                (i, F["tpk_nasional"][y] + 1.2), ha="center", fontweight="bold")
ax.set_ylim(0, 60)
ax.set_title("TPK Bintang Nasional\nTurun 3,27 poin pada 2025", fontsize=11, fontweight="bold", loc="left")
ax.grid(axis="x", visible=False)
ax = axes[1]
bali = [62.35, 61.02]
nas = [52.57, 49.30]
x = range(2)
ax.bar([i - 0.2 for i in x], nas, width=0.4, color=GREY, label="Nasional", zorder=3)
ax.bar([i + 0.2 for i in x], bali, width=0.4, color=MARINE, label="Bali", zorder=3)
ax.set_xticks(list(x))
ax.set_xticklabels(["2024", "2025"])
ax.set_ylim(0, 72)
ax.set_title("Bali Konsisten di Atas Nasional\n(+11,7 poin pada 2025)", fontsize=11, fontweight="bold", loc="left")
ax.legend(frameon=False)
ax.grid(axis="x", visible=False)
save(fig, "11_tpk_tren_dan_bali.png")

# -------------------------------------------------------------------- chart 12
fig, ax = plt.subplots(figsize=(9.4, 5.2))
top10w = w.nlargest(10, "perjalanan_2025").sort_values("perjalanan_2025")
ax.barh(top10w.provinsi_tujuan, top10w.perjalanan_2025 / 1e6,
        color=[MARINE if n != "Bali" else BUTTER for n in top10w.provinsi_tujuan],
        zorder=3)
for i, v in enumerate(top10w.perjalanan_2025):
    ax.annotate(f"{v/1e6:,.1f} jt".replace(",", "X").replace(".", ",").replace("X", "."),
                (v / 1e6 + 5, i), va="center", fontsize=9.5, fontweight="bold")
ax.set_xlabel("Juta perjalanan wisnus, Jan–Des 2025")
ax.set_title("10 Provinsi Tujuan Wisnus Teratas 2025 — Jawa Timur & Jawa Barat di Atas 210 Juta",
             fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 255)
ax.grid(axis="y", visible=False)
save(fig, "12_wisnus_tujuan_2025.png")

# -------------------------------------------------------------------- chart 13
fig, ax = plt.subplots(figsize=(8.6, 4.3))
cats = ["Wisnus\n(perjalanan domestik)", "Wisman\n(kunjungan asing)"]
vals = [tot_w25 / 1e6, tot25 / 1e6]
ax.bar(cats, vals, color=[MARINE, RED], width=0.5, zorder=3)
ax.set_yscale("log")
ax.set_ylim(1, 3200)
for i, v in enumerate(vals):
    ax.annotate(f"{v:,.1f} jt".replace(",", "X").replace(".", ",").replace("X", "."),
                (i, v * 1.35), ha="center", fontsize=11, fontweight="bold")
ax.set_ylabel("Juta (skala log)")
ax.set_title("Skala 2025: Perjalanan Wisnus 78 Kali Kunjungan Wisman",
             fontsize=12, fontweight="bold", loc="left")
ax.grid(axis="x", visible=False)
save(fig, "13_wisnus_vs_wisman.png")

# -------------------------------------------------------------------- chart 14
fig, ax = plt.subplots(figsize=(8.8, 4.3))
r26 = rlm[(rlm.periode == "Agu 2026") & (rlm.wilayah == "Indonesia")]
r26d = dict(zip(r26.kelompok_tamu, r26.rata_rata_lama_menginap_malam))
groups = ["Des 2025", "Agu 2026"]
asing = [F["rlm_des2025"]["Asing"], float(r26d["Asing"])]
indo = [F["rlm_des2025"]["Indonesia"], float(r26d["Indonesia"])]
x = range(2)
ax.bar([i - 0.2 for i in x], asing, width=0.4, color=MARINE, label="Tamu asing", zorder=3)
ax.bar([i + 0.2 for i in x], indo, width=0.4, color=BUTTER, label="Tamu Indonesia", zorder=3)
for i, v in enumerate(asing):
    ax.annotate(f"{v:.2f}".replace(".", ","), (i - 0.2, v + 0.08), ha="center", fontweight="bold")
for i, v in enumerate(indo):
    ax.annotate(f"{v:.2f}".replace(".", ","), (i + 0.2, v + 0.08), ha="center", fontweight="bold")
ax.set_xticks(list(x))
ax.set_xticklabels(groups)
ax.set_ylabel("Malam")
ax.set_ylim(0, 3.1)
ax.set_title("Rata-Rata Lama Menginap Tamu Hotel Bintang\nTamu asing menginap ±1 malam lebih lama",
             fontsize=12, fontweight="bold", loc="left")
ax.legend(frameon=False)
ax.grid(axis="x", visible=False)
save(fig, "14_rlm_tamu.png")

print("SELESAI — temuan kunci:")
print(json.dumps({k: F[k] for k in ["pemulihan_vs_2019_persen", "ytd_2026_vs_2019_persen",
                                    "pangsa_ngurah_rai_2025", "rasio_wisnus_wisman_2025"]},
                 indent=1, ensure_ascii=False))
