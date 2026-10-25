# -*- coding: utf-8 -*-
"""
Modul belajar Analisis Pariwisata Indonesia (PDF landscape, pro pemula,
Bahasa Indonesia sederhana, banyak visual, termasuk bab Power BI).
Jalankan: ~/workspace/mienv/bin/python scripts/build_module.py
"""
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(ROOT, "charts")
OUT = os.path.join(ROOT, "Modul-Analisis-Pariwisata.pdf")

MARINE = HexColor("#0B3C5D"); MARINE_L = HexColor("#3E7CA6")
RED = HexColor("#D7263D"); BUTTER = HexColor("#F4B41A")
OAT = HexColor("#FAF6EF"); SLATE = HexColor("#22303C")
GREY = HexColor("#8A97A5"); LIGHT = HexColor("#E9EFF3")

PAGE_W, PAGE_H = landscape(A4)

H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=21, leading=26,
                    textColor=MARINE, spaceAfter=4)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14.5, leading=19,
                    textColor=MARINE, spaceBefore=6, spaceAfter=3)
BODY = ParagraphStyle("BODY", fontName="Helvetica", fontSize=11.3, leading=16.5,
                      textColor=SLATE, alignment=TA_LEFT, spaceAfter=5)
SMALL = ParagraphStyle("SMALL", fontName="Helvetica", fontSize=9.3, leading=13,
                       textColor=GREY)
CAP = ParagraphStyle("CAP", fontName="Helvetica-Oblique", fontSize=9.3,
                     leading=12.5, textColor=GREY, spaceBefore=2, spaceAfter=8)
KICK = ParagraphStyle("KICK", fontName="Helvetica-Bold", fontSize=10,
                      leading=13, textColor=RED, spaceAfter=2)


def footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(MARINE)
        canvas.rect(0, PAGE_H - 11 * mm, PAGE_W, 11 * mm, stroke=0, fill=1)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica-Bold", 9.5)
        canvas.drawString(14 * mm, PAGE_H - 7.2 * mm,
                          "Modul Analisis Pariwisata Indonesia 2026")
        canvas.setFillColor(BUTTER)
        canvas.drawRightString(PAGE_W - 14 * mm, PAGE_H - 7.2 * mm,
                               f"Halaman {doc.page}")
        canvas.setFillColor(GREY)
        canvas.setFont("Helvetica", 8.3)
        canvas.drawString(14 * mm, 9 * mm,
                          "Sumber data: BPS — BRS Perkembangan Pariwisata & Statistik Kunjungan Wisman 2023 (rincian: data/SOURCES.md)")
    canvas.restoreState()


def img(name, w_mm):
    path = os.path.join(CH, name)
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    return Image(path, width=w_mm * mm, height=w_mm * mm * ih / iw)


def callout(judul, isi, warna=BUTTER):
    t = Table([[Paragraph(f"<b>{judul}</b>", ParagraphStyle(
        "co1", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=MARINE))],
               [Paragraph(isi, ParagraphStyle(
                   "co2", fontName="Helvetica", fontSize=10.8, leading=15, textColor=SLATE))]],
              colWidths=[PAGE_W - 34 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FDF3D8")),
        ("BOX", (0, 0), (-1, -1), 0.8, warna),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


story = []

# ------------------------------------------------------------------ cover
story.append(Spacer(1, 26 * mm))
story.append(Paragraph("MODUL BELAJAR • ANALISIS DATA", KICK))
story.append(Paragraph("Analisis Pariwisata<br/>Indonesia 2026", ParagraphStyle(
    "cover", fontName="Helvetica-Bold", fontSize=37, leading=44, textColor=MARINE)))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph(
    "Memahami kolaps pandemi, tangga pemulihan wisatawan mancanegara, dominasi "
    "Bali sebagai gerbang utama, dan raksasa pasar domestik — semuanya dari data "
    "resmi BPS, dijelaskan langkah demi langkah untuk pemula.",
    ParagraphStyle("cov2", fontName="Helvetica", fontSize=14, leading=20, textColor=SLATE)))
story.append(Spacer(1, 8 * mm))
tbl = Table([[Paragraph("<b>15,39 jt</b><br/><font size=9>wisman 2025</font>", BODY),
              Paragraph("<b>95,5%</b><br/><font size=9>pemulihan vs 2019</font>", BODY),
              Paragraph("<b>1,20 M</b><br/><font size=9>perjalanan wisnus 2025</font>", BODY),
              Paragraph("<b>44,9%</b><br/><font size=9>masuk lewat Ngurah Rai</font>", BODY)]],
            colWidths=[(PAGE_W - 28 * mm) / 4] * 4)
tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
    ("BOX", (0, 0), (-1, -1), 0.9, MARINE_L),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, MARINE_L),
    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(tbl)
story.append(Spacer(1, 10 * mm))
story.append(Paragraph("Disusun oleh <b>BAGHIZ ASSHIDDIQIE ARASYA</b> — Data Analyst",
                       ParagraphStyle("cov3", fontName="Helvetica", fontSize=12,
                                      leading=16, textColor=SLATE)))
story.append(Paragraph("Pendamping proyek portofolio github.com/baghizash/pariwisata-indonesia-2026",
                       SMALL))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 0
story.append(Paragraph("SEBELUM MULAI", KICK))
story.append(Paragraph("Cara Memakai Modul Ini", H1))
story.append(Paragraph(
    "Modul ini menemani proyek portofolio <b>Analisis Pariwisata Indonesia 2026</b>. "
    "Setiap bab memakai angka yang sama dengan yang ada di repositori GitHub proyek, "
    "sehingga kamu bisa memeriksa ulang semua hitungan dari berkas CSV-nya. "
    "Tidak ada prasyarat matematika — cukup rasa ingin tahu.", BODY))
story.append(Paragraph("Istilah kunci (dipakai di seluruh modul)", H2))
istilah = [
    ["<b>Wisman</b>", "Wisatawan mancanegara — tamu asing yang berkunjung ke Indonesia."],
    ["<b>Wisnus</b>", "Wisatawan nusantara — warga Indonesia yang bepergian di dalam negeri. Satu orang bisa tercatat berkali-kali; yang dihitung adalah <i>perjalanan</i>."],
    ["<b>Wisnas</b>", "Wisatawan nasional — warga Indonesia yang bepergian ke luar negeri (tidak dibahas mendalam di modul ini)."],
    ["<b>TPK</b>", "Tingkat Penghunian Kamar hotel — persentase kamar yang terisi. Modul ini memakai TPK hotel klasifikasi bintang."],
    ["<b>RLM / RLMT</b>", "Rata-rata lama menginap tamu, dalam satuan malam."],
    ["<b>BRS</b>", "Berita Resmi Statistik — rilis berkala BPS, sumber utama angka di proyek ini."],
    ["<b>YTD</b>", "<i>Year to date</i> — kumulatif dari Januari sampai bulan terakhir yang tersedia."],
]
t = Table([[Paragraph(a, BODY), Paragraph(b, BODY)] for a, b in istilah],
          colWidths=[30 * mm, PAGE_W - 58 * mm])
t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("LINEBELOW", (0, 0), (-1, -2), 0.4, LIGHT),
                       ("LEFTPADDING", (0, 0), (-1, -1), 4),
                       ("TOPPADDING", (0, 0), (-1, -1), 3),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
story.append(t)
story.append(Spacer(1, 3 * mm))
story.append(callout("Janji modul ini",
                     "Semua angka dapat ditelusuri ke publikasi BPS. Jika sebuah angka "
                     "tidak ditemukan di publikasi BPS, angka itu <b>tidak dipakai</b> — "
                     "prinsip yang sama dipakai analis data profesional agar hasil kerjanya bisa dipertanggungjawabkan."))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 1
story.append(Paragraph("BAB 1", KICK))
story.append(Paragraph("Gambaran Besar: Pariwisata yang Hampir Pulih", H1))
story.append(Paragraph(
    "Pada 2019 Indonesia menerima <b>16,11 juta</b> kunjungan wisman — rekor yang menjadi "
    "patokan (baseline) seluruh analisis. Pandemi memangkasnya menjadi hanya "
    "<b>1,56 juta</b> pada 2021. Setelah itu kunjungan naik setiap tahun: 5,89 juta (2022), "
    "11,68 juta (2023), 13,89 juta (2024), dan <b>15,39 juta pada 2025</b>. Delapan bulan "
    "pertama 2026 sudah mencapai 10,58 juta kunjungan.", BODY))
story.append(img("01_tren_tahunan.png", 168))
story.append(Paragraph("Gambar 1.1 — Kunjungan wisman per tahun. Bar merah = titik terendah 2021; bar kuning = 2026 yang baru berjalan 8 bulan.", CAP))
story.append(Paragraph(
    "Cara membaca grafik batang seperti ini: tinggi bar menunjukkan jumlah. Garis putus-putus "
    "merah adalah tinggi baseline 2019. Bar yang belum menyentuh garis berarti pemulihan "
    "belum tuntas — pada 2025 jaraknya tinggal 4,5%.", BODY))
story.append(callout("Angka untuk diingat",
                     "Pemulihan 2025 = 15,39 ÷ 16,11 = <b>95,5%</b>. Jan–Agu 2026 dibanding "
                     "periode sama 2019 = <b>98,7%</b> — artinya secara laju bulanan, pariwisata "
                     "Indonesia praktis sudah kembali ke level prapandemi."))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 2
story.append(Paragraph("BAB 2", KICK))
story.append(Paragraph("Data & Metode: Kompilasi dari Publikasi BPS", H1))
story.append(Paragraph(
    "Berbeda dari proyek yang memakai satu berkas CSV mentah, data pariwisata tersebar di "
    "banyak rilis BPS. Proyek ini <b>mengompilasi</b> angka dari tabel-tabel pada publikasi "
    "berikut, lalu menyusunnya menjadi CSV rapi di folder <font face='Courier'>data/</font>:", BODY))
sumber = [
    ["Statistik Kunjungan Wisman 2023", "Publikasi tahunan BPS", "Bulanan 2019–2023, pintu masuk & kebangsaan 2019/2023"],
    ["BRS Des 2024", "No. 11/02/Th. XXVIII, 3 Feb 2025", "Total & pintu masuk 2024, wisnus provinsi 2024"],
    ["BRS Des 2025", "No. 13/02/Th. XXIX, 2 Feb 2026", "Total 2025, revisi 2024, TPK provinsi, RLM, wisnus provinsi 2025"],
    ["BRS Jan–Agu 2026", "No. 26/03, 56/06, 73/08, 98/10 Th. XXIX", "Rantai bulanan 2026, pintu & kebangsaan 2026, TPK & wisnus 2026"],
]
t = Table([[Paragraph(f"<b>{a}</b>", BODY), Paragraph(b, BODY), Paragraph(c, BODY)]
           for a, b, c in sumber],
          colWidths=[52 * mm, 62 * mm, PAGE_W - 142 * mm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                       ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("LINEBELOW", (0, 0), (-1, -2), 0.4, LIGHT),
                       ("LEFTPADDING", (0, 0), (-1, -1), 5),
                       ("TOPPADDING", (0, 0), (-1, -1), 4),
                       ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
story.append(t)
story.append(Paragraph("Tiga hal yang wajib diperhatikan saat memakai data kompilasi", H2))
story.append(Paragraph(
    "<b>1. Revisi itu normal.</b> Total 2024 pertama kali dirilis sebagai 13.902.420, lalu "
    "direvisi BPS menjadi 13.886.678 pada BRS Des 2025. Proyek ini memakai angka revisi "
    "terbaru dan mencatat perubahan itu di SOURCES.md.<br/>"
    "<b>2. Semua nilai bulanan wisman kini eksak.</b> Pada kompilasi awal, lima bulan "
    "(Jan &amp; Feb 2025, Mei 2025, Jul 2025, Jan 2026) hanya bisa diperoleh sebagai angka "
    "turunan — hasil pengurangan antar kumulatif resmi — karena BPS sempat hanya merilis "
    "data pintu utama. Pada verifikasi 24 Oktober 2026 kelimanya diganti atau dikonfirmasi "
    "dengan angka eksak dari BRS dan publikasi tahunan BPS; Jan 2025 terkoreksi dari "
    "1.155.978 menjadi 1.156.012 dan Feb 2025 dari 1.022.928 menjadi 1.022.894 — dua "
    "koreksi yang saling meniadakan sehingga total tahunan tidak berubah.<br/>"
    "<b>3. Yang tidak terverifikasi dibuang.</b> Wisman bulanan Jan–Okt 2024 tidak "
    "dikompilasi karena tidak dapat dipisahkan secara eksak dari publikasi yang tersedia. "
    "Sep–Okt 2025 yang semula dikecualikan kini sudah dilengkapi dari publikasi tahunan "
    "BPS 2025 (25 Oktober 2026), sehingga seri bulanan 2025 lengkap 12 bulan dan jumlahnya "
    "persis sama dengan total tahunan resmi 15.386.646. Lebih baik seri berlubang yang "
    "jujur daripada seri mulus yang mengarang.", BODY))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 3
story.append(Paragraph("BAB 3", KICK))
story.append(Paragraph("Kolaps & Pemulihan, Tahun demi Tahun", H1))
story.append(Paragraph(
    "Mengubah jumlah kunjungan menjadi <b>persentase terhadap 2019</b> membuat cerita "
    "pemulihan mudah dibaca: 100% berarti sudah menyamai prapandemi.", BODY))
story.append(img("02_kurva_pemulihan.png", 160))
story.append(Paragraph("Gambar 3.1 — Tingkat pemulihan wisman terhadap baseline 2019.", CAP))
story.append(Paragraph(
    "Perhatikan bentuknya yang seperti tangga: setiap tahun naik, tidak pernah turun. "
    "Kenaikan terbesar terjadi pada 2022 (+278,10% dari titik terendah) dan 2023 (+98,29%). "
    "Setelah itu laju melambat wajar — semakin dekat ke 100%, semakin sulit menambah persen.", BODY))
story.append(img("03_bulanan_2019_2023.png", 168))
story.append(Paragraph("Gambar 3.2 — Pola bulanan memperlihatkan jurang 2020–2021 dan pendakian 2022–2023.", CAP))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 4
story.append(Paragraph("BAB 4", KICK))
story.append(Paragraph("Musiman: Kapan Indonesia Paling Ramai?", H1))
story.append(Paragraph(
    "<b>Indeks musiman</b> merata-ratakan pangsa tiap bulan terhadap total setahun, lalu "
    "dibakukan agar rata-rata = 100. Indeks 115 berarti bulan itu 15% lebih ramai dari "
    "bulan rata-rata; indeks 85 berarti 15% lebih sepi.", BODY))
story.append(img("05_indeks_musiman.png", 158))
story.append(Paragraph("Gambar 4.1 — Indeks musiman dari rata-rata 2019 & 2023: Agustus teratas (115), Februari terendah (85).", CAP))
story.append(Paragraph(
    "Pola ini berulang di 2026: kunjungan naik dari lembah Maret (1,09 juta, terdampak "
    "Ramadan) menuju puncak Agustus (1,60 juta) yang bertepatan dengan libur musim panas "
    "belahan bumi utara dan libur sekolah. Bagi pelaku usaha, indeks ini adalah alat "
    "perencanaan paling sederhana: stok, jadwal karyawan, dan promosi mengikuti kurva ini.", BODY))
story.append(img("04_bulanan_2026_vs_2025.png", 158))
story.append(Paragraph("Gambar 4.2 — Bulanan 2026 (marine) vs 2025 (abu). Seri 2025 kini lengkap 12 bulan; seri 2026 baru tersedia sampai Agustus — lihat Bab 2.", CAP))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 5
story.append(Paragraph("BAB 5", KICK))
story.append(Paragraph("Pintu Masuk: Dominasi Satu Bandara", H1))
story.append(Paragraph(
    "Dari 15,39 juta kunjungan 2025, sebanyak <b>6,91 juta (44,9%)</b> masuk melalui Bandara "
    "Ngurah Rai, Bali. Tambahkan Soekarno-Hatta (2,76 juta) dan dua gerbang ini menampung "
    "<b>62,8%</b> dari seluruh wisman. Enam gerbang utama menampung 78,9%.", BODY))
story.append(img("06_pintu_masuk_2025.png", 164))
story.append(Paragraph("Gambar 5.1 — Enam gerbang utama wisman 2025. Batam adalah gerbang laut terbesar berkat kedekatan dengan Singapura.", CAP))
story.append(Paragraph(
    "Konsentrasi setinggi ini efisien (infrastruktur terpusat) tetapi rapuh: gangguan di "
    "Bali — cuaca, abu vulkanik, atau kapasitas bandara — langsung terasa pada angka "
    "nasional. Itulah sebabnya pangsa gerbang adalah indikator yang dipantau terus.", BODY))
story.append(img("07_komposisi_pintu_2025.png", 118))
story.append(Paragraph("Gambar 5.2 — Komposisi pintu kedatangan 2025. Pintu utama menampung 87,4%; pintu perbatasan 12,6%.", CAP))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 6
story.append(Paragraph("BAB 6", KICK))
story.append(Paragraph("Kebangsaan: Siapa yang Sudah Kembali, Siapa yang Belum", H1))
story.append(Paragraph(
    "Pemulihan tidak terjadi serentak di semua pasar. Pada 2023, wisatawan <b>Australia</b> "
    "sudah mencapai 103,2% dari level 2019-nya — satu-satunya pasar besar yang melampaui "
    "prapandemi. Sebaliknya wisatawan <b>Tiongkok</b> baru 38,0% dan Jepang 48,5%.", BODY))
story.append(img("08_kebangsaan_2019_2023.png", 166))
story.append(Paragraph("Gambar 6.1 — Enam kebangsaan teratas, 2019 vs 2023.", CAP))
story.append(Paragraph(
    "Malaysia tetap pasar nomor satu di semua periode: pangsa 17,2% pada 2025 dan 18,5% "
    "pada Agustus 2026. Pangsa ASEAN menguat dari 36,4% (2023) menjadi 41,3% (2025) — "
    "pasar jarak pendek pulih lebih dulu dan kini menopang pertumbuhan.", BODY))
story.append(img("09_kebangsaan_agu2026.png", 158))
story.append(Paragraph("Gambar 6.2 — Kebangsaan teratas pada Agustus 2026, bulan tersibuk 2026.", CAP))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 7
story.append(Paragraph("BAB 7", KICK))
story.append(Paragraph("Hotel: TPK Turun, Tamu Asing Menginap Lebih Lama", H1))
story.append(Paragraph(
    "Kunjungan naik bukan berarti hotel ikut penuh. TPK hotel bintang nasional justru "
    "turun dari 52,57% (2024) menjadi <b>49,30% (2025)</b> — pasokan kamar tumbuh lebih "
    "cepat daripada permintaan. Bali tetap tertinggi (61,02%), Aceh terendah (25,01%).", BODY))
story.append(img("10_tpk_provinsi_2025.png", 162))
story.append(Paragraph("Gambar 7.1 — TPK bintang 2025: sepuluh provinsi tertinggi dan lima terendah.", CAP))
story.append(Paragraph(
    "Sementara itu, tamu asing menginap lebih lama daripada tamu Indonesia: 2,65 malam "
    "berbanding 1,46 malam pada Desember 2025. Di Bali, rata-rata totalnya 2,91 malam — "
    "tertinggi di antara wilayah yang dibandingkan.", BODY))
story.append(img("14_rlm_tamu.png", 150))
story.append(Paragraph("Gambar 7.2 — Rata-rata lama menginap tamu hotel bintang (malam).", CAP))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 8
story.append(Paragraph("BAB 8", KICK))
story.append(Paragraph("Wisnus: Pasar Domestik yang 78 Kali Lebih Besar", H1))
story.append(Paragraph(
    "Perjalanan wisatawan nusantara mencapai <b>1.200.332.559 perjalanan pada 2025</b>, "
    "naik 17,55% dari 2024. Bandingkan dengan wisman 15,39 juta — pasar domestik "
    "<b>78 kali</b> lebih besar. Dua dari tiga perjalanan (64,8%) bertujuan ke Pulau Jawa, "
    "terutama Jawa Timur (217,2 juta) dan Jawa Barat (211,8 juta).", BODY))
story.append(img("12_wisnus_tujuan_2025.png", 164))
story.append(Paragraph("Gambar 8.1 — Sepuluh provinsi tujuan wisnus teratas 2025. Bali (kuning) berada di peringkat tujuh.", CAP))
story.append(Paragraph(
    "Mengapa Jawa mendominasi? Karena wisnus mengukur <i>perjalanan</i>, bukan wisatawan "
    "unik: provinsi berpenduduk besar otomatis menghasilkan dan menerima perjalanan "
    "terbanyak. Bali yang ikonik untuk wisman hanya menampung 26,6 juta perjalanan "
    "wisnus (2,2%). Membaca angka tanpa memahami definisinya adalah kesalahan klasik "
    "analis pemula — selalu cek apa yang sebenarnya dihitung.", BODY))
story.append(img("13_wisnus_vs_wisman.png", 148))
story.append(Paragraph("Gambar 8.2 — Perbandingan skala 2025 memakai sumbu logaritmik agar kedua bar terlihat.", CAP))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 9
story.append(Paragraph("BAB 9", KICK))
story.append(Paragraph("Membangun Dashboard di Power BI", H1))
story.append(Paragraph(
    "Folder <font face='Courier'>powerbi/</font> pada repositori berisi kit lengkap: "
    "9 berkas CSV star schema, dokumen measure DAX, layout 4 halaman, dan panduan "
    "membangun. Nama berkas akhir yang disarankan: "
    "<b>Pariwisata-Indonesia-2026.pbix</b>.", BODY))
story.append(Image(os.path.join(ROOT, "powerbi", "dashboard_preview_halaman1.png"),
                   width=185 * mm, height=185 * mm * 0.5625))
story.append(Paragraph("Gambar 9.1 — Pratinjau halaman 1 (Ringkasan Eksekutif) dari kit Power BI.", CAP))
story.append(Paragraph("Langkah singkat", H2))
story.append(Paragraph(
    "1. Muat ke-9 CSV dari folder <font face='Courier'>powerbi/</font> lewat Get Data → Text/CSV.<br/>"
    "2. Buat relasi: <font face='Courier'>dim_tahun[tahun]</font> ke semua tabel fact bertahun, "
    "dan <font face='Courier'>dim_bulan[bulan_ke]</font> ke fact_wisman_bulanan.<br/>"
    "3. Buat 14 measure dari <font face='Courier'>measures_dax.md</font> — namanya teks polos, "
    "misalnya <b>Total Kunjungan Wisman</b> = <font face='Courier'>SUM ( fact_wisman_bulanan[kunjungan_wisman] )</font>.<br/>"
    "4. Uji dengan <b>Tabel Verifikasi</b> di dokumen yang sama: total 2019 harus "
    "16.106.954 dan pangsa Ngurah Rai 2025 harus 44,9%. Jika cocok, modelmu benar.<br/>"
    "5. Susun visual mengikuti <font face='Courier'>dashboard_layout.md</font>, lalu simpan sebagai .pbix.<br/>"
    "6. Alternatif cepat: buka paket <b>PBIP</b> yang menyertai proyek, arahkan parameter "
    "FolderData ke folder data paket, refresh, lalu Save As .pbix.", BODY))
story.append(callout("Jebakan yang harus dihindari",
                     "Tabel bulanan 2024 hanya berisi November–Desember dan 2025 berisi 10 bulan. "
                     "Untuk angka setahun penuh selalu pakai <font face='Courier'>fact_wisman_tahunan</font>. "
                     "Menjumlahkan tabel yang tidak lengkap adalah penyebab angka dashboard paling sering meleset."))
story.append(PageBreak())

# ------------------------------------------------------------------ bab 10
story.append(Paragraph("BAB 10", KICK))
story.append(Paragraph("Latihan & Kesimpulan", H1))
story.append(Paragraph("Uji pemahamanmu (jawaban di akhir bab)", H2))
story.append(Paragraph(
    "1. Berapa persen pemulihan wisman pada 2024 terhadap 2019?<br/>"
    "2. Bulan apa yang menjadi puncak kunjungan 2026, dan berapa jumlahnya?<br/>"
    "3. Dua gerbang apa yang bersama-sama menampung 62,8% wisman 2025?<br/>"
    "4. Pasar kebangsaan mana yang pada 2023 sudah melampaui level 2019-nya?<br/>"
    "5. Provinsi mana dengan TPK bintang tertinggi dan terendah pada 2025?<br/>"
    "6. Berapa kali lebih besar perjalanan wisnus dibanding kunjungan wisman pada 2025?<br/>"
    "7. Mengapa total wisman tahunan sebaiknya tidak dihitung dari tabel bulanan untuk 2024?", BODY))
story.append(Paragraph("Kesimpulan", H2))
story.append(Paragraph(
    "Pariwisata Indonesia berada di ujung pemulihan: kunjungan asing 2025 mencapai 95,5% "
    "dari baseline 2019 dan laju 2026 menyentuh 98,7%. Cerita di balik angka totalnya "
    "lebih kaya — konsentrasi ekstrem di Bali, pasar Tiongkok yang belum kembali, TPK "
    "yang menurun, dan pasar domestik raksasa yang tumbuh 17,55%. Analis yang baik "
    "tidak berhenti pada angka total; ia membongkar komposisinya.", BODY))
story.append(Paragraph(
    "<b>Kunci jawaban:</b> 1) 86,2%. 2) Agustus, 1.599.660 kunjungan. 3) Ngurah Rai dan "
    "Soekarno-Hatta. 4) Australia (103,2%). 5) Bali (61,02%) dan Aceh (25,01%). "
    "6) 78 kali. 7) Karena tabel bulanan 2024 hanya memuat November–Desember; "
    "bulan lain tidak dikompilasi dari publikasi BPS.", BODY))
story.append(Spacer(1, 4 * mm))
story.append(callout("Langkah berikutnya",
                     "Buka repositori proyek, jalankan <font face='Courier'>scripts/compile_data.py</font> lalu "
                     "<font face='Courier'>scripts/analysis.py</font>, dan cocokkan hasilnya dengan modul ini. "
                     "Setelah itu rakit dashboard-nya dari kit Power BI — dan kamu punya satu proyek portofolio utuh.",
                     warna=MARINE_L))

doc = SimpleDocTemplate(OUT, pagesize=landscape(A4),
                        leftMargin=14 * mm, rightMargin=14 * mm,
                        topMargin=16 * mm, bottomMargin=13 * mm,
                        title="Modul Analisis Pariwisata Indonesia 2026",
                        author="Baghiz Asshiddiqie Arasya")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Modul tertulis:", OUT)
