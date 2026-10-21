# -*- coding: utf-8 -*-
"""
Membangun Portofolio-Analisis-Pariwisata.pptx (10 slide, 16:9) mengikuti
standar deck terbaru: cover panel hero, chip KPI, slide temuan,
slide 9 Dashboard Power BI, dan Designed Close.
"""
import json
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(ROOT, "charts")
F = json.load(open(os.path.join(ROOT, "findings.json")))

MARINE = RGBColor(0x0B, 0x3C, 0x5D)
MARINE_L = RGBColor(0x3E, 0x7C, 0xA6)
RED = RGBColor(0xD7, 0x26, 0x3D)
BUTTER = RGBColor(0xF4, 0xB4, 0x1A)
OAT = RGBColor(0xFA, 0xF6, 0xEF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SLATE = RGBColor(0x22, 0x30, 0x3C)
GREY = RGBColor(0x8A, 0x97, 0xA5)
LIGHT = RGBColor(0xE9, 0xEF, 0xF3)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5


def slide(bg=OAT):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg
    r.line.fill.background()
    r.shadow.inherit = False
    return s


def box(s, x, y, w, h, fill=None, line=None, round_=False):
    shp = s.shapes.add_shape(5 if round_ else 1, Inches(x), Inches(y),
                             Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(1.1)
    shp.shadow.inherit = False
    return shp


def txt(s, x, y, w, h, text, size=14, bold=False, color=SLATE, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = font
    return tb


def title_bar(s, kicker, title, page):
    box(s, 0, 0, SW, 1.06, fill=MARINE)
    txt(s, 0.55, 0.10, 11.5, 0.3, kicker.upper(), size=11, bold=True, color=BUTTER)
    txt(s, 0.55, 0.36, 12.2, 0.62, title, size=25, bold=True, color=WHITE)
    txt(s, 12.35, 0.30, 0.6, 0.5, str(page), size=16, bold=True, color=BUTTER,
        align=PP_ALIGN.RIGHT)
    txt(s, 0.55, 7.12, 9.5, 0.3,
        "Pariwisata Indonesia 2026 • Sumber data: BPS (BRS & Statistik Kunjungan Wisman)",
        size=9.5, color=GREY)


def bullets(s, x, y, w, items, size=13.5, gap=0.30, color=SLATE):
    cy = y
    for head, body in items:
        box(s, x, cy + 0.075, 0.13, 0.13, fill=RED)
        txt(s, x + 0.28, cy, w - 0.28, 0.3, head, size=size, bold=True, color=MARINE)
        cy += gap
        if body:
            txt(s, x + 0.28, cy, w - 0.28, 0.62, body, size=size - 1.5, color=color)
            cy += gap + 0.26
    return cy


def pic(s, name, x, y, w):
    s.shapes.add_picture(os.path.join(CH, name), Inches(x), Inches(y), width=Inches(w))


def chip(s, x, y, w, label, value, sub, val_color=MARINE):
    box(s, x, y, w, 1.18, fill=WHITE, line=MARINE_L, round_=True)
    txt(s, x + 0.16, y + 0.09, w - 0.3, 0.26, label, size=10, bold=True, color=GREY)
    txt(s, x + 0.16, y + 0.33, w - 0.3, 0.5, value, size=23, bold=True, color=val_color)
    txt(s, x + 0.16, y + 0.86, w - 0.3, 0.28, sub, size=10, color=SLATE)


# ============================================================ 1 — COVER
s = slide(bg=MARINE)
box(s, 0, 0, 7.6, SH, fill=MARINE)
box(s, 7.6, 0, 5.733, SH, fill=WHITE)
txt(s, 0.7, 0.75, 6.4, 0.35, "PORTOFOLIO ANALISIS DATA", size=13, bold=True, color=BUTTER)
txt(s, 0.7, 1.25, 6.6, 1.9, "Pariwisata\nIndonesia 2026", size=47, bold=True, color=WHITE)
txt(s, 0.7, 3.15, 6.3, 1.0,
    "Kolaps pandemi, tangga pemulihan, dan dominasi Bali:\n"
    "membaca ulang arus wisatawan dari data resmi BPS.",
    size=15, color=LIGHT)
box(s, 0.7, 4.55, 6.2, 0.035, fill=BUTTER)
txt(s, 0.7, 4.85, 6.4, 0.35, "Disusun oleh", size=11.5, color=LIGHT)
txt(s, 0.7, 5.15, 6.6, 0.5, "BAGHIZ ASSHIDDIQIE ARASYA", size=19, bold=True, color=WHITE)
txt(s, 0.7, 5.75, 6.4, 0.35, "Data Analyst • Python, SQL, Power BI", size=12, color=LIGHT)
txt(s, 8.0, 0.85, 4.9, 0.35, "ANGKA UTAMA 2025", size=12, bold=True, color=GREY)
txt(s, 8.0, 1.25, 4.9, 1.1, "15,39 jt", size=52, bold=True, color=MARINE)
txt(s, 8.0, 2.30, 4.9, 0.6, "kunjungan wisman setahun penuh,\nnaik 10,80% dari 2024",
    size=13.5, color=SLATE)
box(s, 8.0, 3.15, 4.5, 0.03, fill=LIGHT)
txt(s, 8.0, 3.35, 4.9, 0.9, "95,5%", size=30, bold=True, color=RED)
txt(s, 8.0, 4.05, 4.9, 0.35, "tingkat pemulihan terhadap 2019", size=12.5, color=SLATE)
box(s, 8.0, 4.65, 4.5, 0.03, fill=LIGHT)
txt(s, 8.0, 4.85, 4.9, 0.9, "1,20 M", size=30, bold=True, color=MARINE)
txt(s, 8.0, 5.55, 4.9, 0.35, "perjalanan wisnus sepanjang 2025", size=12.5, color=SLATE)
txt(s, 8.0, 6.55, 4.9, 0.35, "Periode data: 2019 – Agustus 2026", size=11, color=GREY)

# ============================================================ 2 — RINGKASAN
s = slide()
title_bar(s, "Ringkasan Eksekutif", "2025: Tahun Terakhir Sebelum Garis 2019 Terlampaui", 2)
chip(s, 0.55, 1.30, 2.95, "WISMAN 2025", "15,39 jt", "+10,80% vs 2024")
chip(s, 3.65, 1.30, 2.95, "PEMULIHAN vs 2019", "95,5%", "dari 16,11 jt (2019)", val_color=RED)
chip(s, 6.75, 1.30, 2.95, "WISMAN JAN–AGU 2026", "10,58 jt", "98,7% dari periode sama 2019")
chip(s, 9.85, 1.30, 2.95, "TPK BINTANG 2025", "49,30%", "turun 3,27 poin vs 2024")
pic(s, "01_tren_tahunan.png", 0.55, 2.72, 7.55)
bullets(s, 8.45, 2.85, 4.35, [
    ("Nyaris pulih sepenuhnya", "2025 mencapai 15,39 juta kunjungan; Jan–Agu 2026 sudah 98,7% dari periode sama 2019."),
    ("Mesin domestik jauh lebih besar", "Perjalanan wisnus 2025 = 1,20 miliar, atau 78 kali kunjungan wisman."),
    ("Satu catatan kaki", "TPK hotel bintang justru turun ke 49,30% — kamar bertambah lebih cepat daripada tamu."),
], size=13)

# ============================================================ 3 — KOLAPS & PEMULIHAN
s = slide()
title_bar(s, "Temuan 1 • Kolaps & Pemulihan", "Dari 16,11 Juta ke 1,56 Juta, Lalu Naik Lagi", 3)
pic(s, "02_kurva_pemulihan.png", 0.55, 1.30, 6.35)
pic(s, "03_bulanan_2019_2023.png", 7.10, 1.30, 5.70)
bullets(s, 0.55, 5.15, 12.25, [
    ("Titik terendah 2021: 9,7% dari 2019",
     "Kunjungan anjlok 74,84% pada 2020 dan 61,57% lagi pada 2021 — total hilang 14,55 juta kunjungan dari baseline."),
    ("Pemulihan berbentuk tangga",
     "2022 = 36,6%, 2023 = 72,5%, 2024 = 86,2%, 2025 = 95,5%. Tidak ada satu tahun pun yang mundur."),
], size=13.5)

# ============================================================ 4 — MUSIMAN
s = slide()
title_bar(s, "Temuan 2 • Musiman", "Agustus Selalu Jadi Puncak; Awal Tahun Selalu Sepi", 4)
pic(s, "05_indeks_musiman.png", 0.55, 1.30, 6.15)
pic(s, "04_bulanan_2026_vs_2025.png", 6.90, 1.30, 5.90)
bullets(s, 0.55, 5.05, 12.25, [
    ("Indeks Agustus 115, Februari 85",
     "Pola dari rata-rata 2019 & 2023: semester dua konsisten lebih ramai; Maret 2026 jadi lembah tahun berjalan (1,09 jt) karena Ramadan."),
    ("2026 menguat di musim puncak",
     "Agustus 2026 = 1,60 juta kunjungan, tertinggi sepanjang 2026 dan naik 6,27% dari Agustus 2025."),
], size=13.5)

# ============================================================ 5 — PINTU MASUK
s = slide()
title_bar(s, "Temuan 3 • Pintu Masuk", "Satu Bandara Menampung 44,9% Tamu Asing Indonesia", 5)
pic(s, "06_pintu_masuk_2025.png", 0.55, 1.35, 7.35)
pic(s, "07_komposisi_pintu_2025.png", 8.35, 1.45, 4.30)
bullets(s, 0.55, 5.55, 12.25, [
    ("Konsentrasi sangat tinggi",
     "Ngurah Rai (6,91 jt) + Soekarno-Hatta (2,76 jt) = 62,8% dari seluruh kunjungan 2025; enam gerbang utama menampung 78,9%."),
    ("Jalur laut Kepri adalah gerbang ketiga",
     "Batam mencatat 1,59 juta kunjungan (10,4%), digerakkan pasar Singapura & Malaysia jarak pendek."),
], size=13.5)

# ============================================================ 6 — KEBANGSAAN
s = slide()
title_bar(s, "Temuan 4 • Kebangsaan", "Australia Sudah Lampaui 2019; Tiongkok Baru 38%", 6)
pic(s, "08_kebangsaan_2019_2023.png", 0.55, 1.30, 6.45)
pic(s, "09_kebangsaan_agu2026.png", 7.25, 1.30, 5.55)
bullets(s, 0.55, 5.30, 12.25, [
    ("Pemulihan tidak merata antar pasar",
     "Pada 2023 Australia mencapai 103,2% dari level 2019, India 92,3%, sedangkan Tiongkok baru 38,0% dan Jepang 48,5%."),
    ("ASEAN menguat lagi",
     "Pangsa ASEAN naik dari 36,4% (2023) ke 41,3% (2025); Malaysia tetap nomor satu (17,2% pada 2025; 18,5% pada Agu 2026)."),
], size=13.5)

# ============================================================ 7 — HOTEL
s = slide()
title_bar(s, "Temuan 5 • Hotel", "Bali Paling Penuh, tetapi TPK Nasional Justru Turun", 7)
pic(s, "10_tpk_provinsi_2025.png", 0.55, 1.28, 6.55)
pic(s, "11_tpk_tren_dan_bali.png", 7.30, 1.28, 5.50)
pic(s, "14_rlm_tamu.png", 7.30, 4.15, 5.50)
bullets(s, 0.55, 6.05, 6.7, [
    ("Rentang antarprovinsi lebar",
     "Bali 61,02% vs Aceh 25,01% pada 2025 — selisih 36 poin menunjukkan pasokan kamar belum sejalan dengan permintaan di banyak provinsi."),
], size=12.5)
txt(s, 7.30, 6.62, 5.5, 0.3, "RLM: tamu asing 2,65 malam vs tamu Indonesia 1,46 malam (Des 2025).",
    size=11.5, color=SLATE)

# ============================================================ 8 — WISNUS
s = slide()
title_bar(s, "Temuan 6 • Wisatawan Nusantara", "1,20 Miliar Perjalanan Domestik, Dua-pertiga di Jawa", 8)
pic(s, "12_wisnus_tujuan_2025.png", 0.55, 1.30, 6.75)
pic(s, "13_wisnus_vs_wisman.png", 7.55, 1.30, 5.30)
bullets(s, 0.55, 5.85, 12.25, [
    ("Tumbuh 17,55% dalam setahun",
     "Dari 1,02 miliar (2024) menjadi 1,20 miliar perjalanan (2025). Jawa Timur (217,2 jt) dan Jawa Barat (211,8 jt) jadi tujuan teratas."),
    ("Bali hanya 2,2% dari wisnus",
     "Meski ikonik untuk wisman, Bali mencatat 26,6 juta perjalanan wisnus — kalah jauh dari provinsi-provinsi Jawa yang padat penduduk."),
], size=13.5)

# ============================================================ 9 — POWER BI
s = slide()
title_bar(s, "Dashboard Power BI", "Kit Siap Rakit: Star Schema, 12 Measure DAX, 4 Halaman", 9)
s.shapes.add_picture(os.path.join(ROOT, "powerbi", "dashboard_preview_halaman1.png"),
                     Inches(0.55), Inches(1.35), width=Inches(8.1))
bullets(s, 9.05, 1.55, 3.85, [
    ("9 tabel star schema", "Fact & dim terpisah per grain: bulanan, tahunan, pintu, kebangsaan, TPK, RLM, wisnus."),
    ("Measure terverifikasi", "14 measure DAX bernama polos + tabel verifikasi angka (mis. pangsa Ngurah Rai 44,9%)."),
    ("Paket PBIP menyertai", "Tinggal buka, arahkan parameter FolderData, refresh, Save As .pbix."),
], size=12.5)
txt(s, 9.05, 5.55, 3.85, 0.6, "Berkas: Pariwisata-Indonesia-2026.pbix\n(folder powerbi/ pada repo)",
    size=11.5, color=GREY)

# ============================================================ 10 — PENUTUP
s = slide(bg=MARINE)
box(s, 0, 0, SW, SH, fill=MARINE)
txt(s, 0.7, 0.65, 11.9, 0.35, "KESIMPULAN", size=13, bold=True, color=BUTTER)
txt(s, 0.7, 1.10, 12.0, 0.8, "Pariwisata Indonesia Sudah di Ambang Pulih Penuh",
    size=32, bold=True, color=WHITE)
items = [
    ("1 • Pemulihan 95,5% dan masih naik",
     "Jan–Agu 2026 sudah 98,7% dari periode sama 2019 — dengan laju ini, 2026 berpeluang menutup di atas baseline prapandemi."),
    ("2 • Konsentrasi adalah risiko sekaligus kekuatan",
     "Dua bandara menampung 62,8% wisman dan Bali sendirian 44,9%. Diversifikasi gerbang & pasar (Tiongkok baru 38% pulih) adalah ruang tumbuh terbesar."),
    ("3 • Domestik adalah pasar sesungguhnya",
     "1,20 miliar perjalanan wisnus (78× wisman) tumbuh 17,55%; TPK yang turun ke 49,30% menandakan pasokan kamar tumbuh lebih cepat dari permintaan."),
]
cy = 2.25
for head, body in items:
    txt(s, 0.7, cy, 11.9, 0.4, head, size=17, bold=True, color=BUTTER)
    txt(s, 0.7, cy + 0.42, 11.9, 0.6, body, size=13.5, color=LIGHT)
    cy += 1.15
box(s, 0.7, 5.85, 11.9, 0.03, fill=BUTTER)
txt(s, 0.7, 6.05, 11.9, 0.4,
    "Data: BPS — BRS Perkembangan Pariwisata (Des 2024 s.d. Agu 2026) & Statistik Kunjungan Wisman 2023 • Rincian: data/SOURCES.md",
    size=11, color=LIGHT)
txt(s, 0.7, 6.55, 11.9, 0.4, "BAGHIZ ASSHIDDIQIE ARASYA — Portofolio Analisis Data",
    size=13, bold=True, color=WHITE)

out = os.path.join(ROOT, "Portofolio-Analisis-Pariwisata.pptx")
prs.save(out)
print("PPT tertulis:", out)
