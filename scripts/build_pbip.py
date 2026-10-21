#!/usr/bin/env python3
"""Build the Pariwisata2026 PBIP package (same validated pattern as the 8 previous packages)."""
import json, uuid, shutil
from pathlib import Path

NS = uuid.UUID('6f1c2a90-3b4d-4e5f-8a70-1b2c3d4e5f60')
def G(s): return str(uuid.uuid5(NS, s))

PROJ = 'Pariwisata2026'
ROOT = Path.home() / 'workspace' / 'pbip' / PROJ
KIT = Path.home() / 'workspace' / 'pariwisata' / 'powerbi'
REP = ROOT / f'{PROJ}.Report'
SEM = ROOT / f'{PROJ}.SemanticModel'
DEF_R = REP / 'definition'
DEF_S = SEM / 'definition'

VC = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json'
PG = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json'

def W(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
def WJ(path, obj):
    W(path, json.dumps(obj, indent=2, ensure_ascii=False))

# ---------------------------------------------------------------- field refs
def col(e, p):  return {"Column": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}
def mea(e, p):  return {"Measure": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}
def agg(e, p, f=0): return {"Aggregation": {"Expression": {"SourceRef": {"Entity": e}}, "Function": f, "Property": p}}
def proj(field, e, p, native=None):
    return {"field": field, "queryRef": f"{e}.{p}", "nativeQueryRef": native or p}
def sortby(field, direction):
    return {"field": field, "direction": direction}

_fc = [0]
def _filter(alias, e, p, literals):
    _fc[0] += 1
    return {
        "name": f"flt{_fc[0]:014x}",
        "ordinal": _fc[0],
        "field": col(e, p),
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": alias, "Entity": e, "Type": 0}],
            "Where": [{"Condition": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": p}}],
                "Values": [[{"Literal": {"Value": lit}}] for lit in literals],
            }}}],
        },
        "isHiddenInViewMode": False,
        "isLockedInViewMode": False,
    }
def catfilter(alias, e, p, values):
    return _filter(alias, e, p, [f"'{v}'" for v in values])
def numfilter(alias, e, p, values):
    return _filter(alias, e, p, [str(v) for v in values])

def title_obj(text):
    return {"title": [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "text": {"expr": {"Literal": {"Value": f"'{text}'"}}},
        "bold": {"expr": {"Literal": {"Value": "true"}}},
    }}]}

def visual(name, x, y, w, h, vtype, qstate=None, title_text=None, filters=None,
           sorts=None, objects=None, z=0):
    v = {"$schema": VC, "name": name,
         "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
         "visual": {"visualType": vtype}}
    if qstate is not None:
        q = {"queryState": qstate}
        if sorts:
            q["sortDefinition"] = {"sort": sorts, "isDefaultSort": False}
        v["visual"]["query"] = q
    if objects is not None:
        v["visual"]["objects"] = objects
    if title_text:
        v["visual"]["visualContainerObjects"] = title_obj(title_text)
    if filters:
        v["filterConfig"] = {"filters": filters}
    return v

def textbox(name, x, y, w, h, text, size=20, z=0):
    objects = {"general": [{"properties": {"paragraphs": [{
        "textRuns": [{"value": text, "textStyle": {
            "fontFamily": "Segoe UI", "fontSize": size, "bold": True}}],
        "horizontalTextAlignment": "left"}]}}]}
    return visual(name, x, y, w, h, "textbox", objects=objects, z=z)

def slicer(name, x, y, w, h, e, p, z=0):
    return visual(name, x, y, w, h, "slicer",
                  qstate={"Values": {"projections": [proj(col(e, p), e, p)]}}, z=z)

# ------------------------------------------------------------------- TMDL
TABLES = {
    'dim_bulan': [
        ('bulan_ke', 'int64', '0'), ('bulan', 'string', None), ('bulan_singkat', 'string', None)],
    'dim_tahun': [
        ('tahun', 'int64', '0'), ('fase', 'string', None)],
    'fact_wisman_bulanan': [
        ('tahun', 'int64', '0'), ('bulan_ke', 'int64', '0'), ('bulan', 'string', None),
        ('kunjungan_wisman', 'int64', '#,##0')],
    'fact_wisman_tahunan': [
        ('tahun', 'int64', '0'), ('kunjungan_wisman', 'int64', '#,##0'),
        ('status_periode', 'string', None)],
    'fact_wisman_pintu': [
        ('periode', 'string', None), ('pintu_masuk', 'string', None),
        ('moda', 'string', None), ('kunjungan', 'int64', '#,##0')],
    'fact_wisman_kebangsaan': [
        ('periode', 'string', None), ('kebangsaan', 'string', None),
        ('kunjungan', 'int64', '#,##0')],
    'fact_tpk_provinsi': [
        ('provinsi', 'string', None), ('tahun', 'int64', '0'), ('tpk_persen', 'double', '0.00')],
    'fact_tpk_snapshot': [
        ('provinsi', 'string', None), ('periode', 'string', None), ('tpk_persen', 'double', '0.00')],
    'fact_rlm': [
        ('periode', 'string', None), ('wilayah', 'string', None),
        ('kelompok_tamu', 'string', None), ('rata_rata_lama_menginap_malam', 'double', '0.00')],
    'fact_wisnus_tujuan': [
        ('provinsi', 'string', None), ('tahun', 'int64', '0'), ('perjalanan', 'int64', '#,##0')],
}
SORTBY = {('dim_bulan', 'bulan'): 'bulan_ke', ('dim_bulan', 'bulan_singkat'): 'bulan_ke'}
MTYPE = {'int64': 'Int64.Type', 'double': 'type number', 'string': 'type text', 'dateTime': 'type date'}

MEASURES = {
    'fact_wisman_bulanan': [
        ('Total Kunjungan Wisman', 'SUM ( fact_wisman_bulanan[kunjungan_wisman] )', '#,##0'),
    ],
    'fact_wisman_tahunan': [
        ('Total Kunjungan Tahunan', 'SUM ( fact_wisman_tahunan[kunjungan_wisman] )', '#,##0'),
        ('Kunjungan Wisman 2019',
         'CALCULATE ( [Total Kunjungan Tahunan], fact_wisman_tahunan[tahun] = 2019 )', '#,##0'),
        ('Kunjungan Wisman 2025',
         'CALCULATE ( [Total Kunjungan Tahunan], fact_wisman_tahunan[tahun] = 2025 )', '#,##0'),
        ('Tingkat Pemulihan vs 2019',
         'DIVIDE ( [Total Kunjungan Tahunan], [Kunjungan Wisman 2019] )', '0.0%'),
        ('Kunjungan Wisman YTD 2026',
         'CALCULATE (\n    SUM ( fact_wisman_tahunan[kunjungan_wisman] ),\n    fact_wisman_tahunan[tahun] = 2026\n)', '#,##0'),
    ],
    'fact_wisman_pintu': [
        ('Total Kunjungan Pintu', 'SUM ( fact_wisman_pintu[kunjungan] )', '#,##0'),
        ('Pangsa Pintu Masuk',
         'DIVIDE (\n    [Total Kunjungan Pintu],\n    CALCULATE ( [Total Kunjungan Pintu], ALL ( fact_wisman_pintu[pintu_masuk] ) )\n)', '0.0%'),
    ],
    'fact_tpk_provinsi': [
        ('Rata Rata TPK Provinsi', 'AVERAGE ( fact_tpk_provinsi[tpk_persen] )', '0.00'),
    ],
    'fact_rlm': [
        ('RLM Rata Rata', 'AVERAGE ( fact_rlm[rata_rata_lama_menginap_malam] )', '0.00'),
    ],
    'fact_wisnus_tujuan': [
        ('Total Perjalanan Wisnus', 'SUM ( fact_wisnus_tujuan[perjalanan] )', '#,##0'),
        ('Wisnus 2024',
         'CALCULATE ( [Total Perjalanan Wisnus], fact_wisnus_tujuan[tahun] = 2024 )', '#,##0'),
        ('Wisnus 2025',
         'CALCULATE ( [Total Perjalanan Wisnus], fact_wisnus_tujuan[tahun] = 2025 )', '#,##0'),
        ('Pertumbuhan Wisnus Persen',
         'DIVIDE ( [Wisnus 2025] - [Wisnus 2024], [Wisnus 2024] )', '0.00%'),
    ],
}

RELATIONSHIPS = [
    ('fact_wisman_bulanan', 'tahun', 'dim_tahun', 'tahun'),
    ('fact_wisman_bulanan', 'bulan_ke', 'dim_bulan', 'bulan_ke'),
    ('fact_wisman_tahunan', 'tahun', 'dim_tahun', 'tahun'),
    ('fact_tpk_provinsi', 'tahun', 'dim_tahun', 'tahun'),
    ('fact_wisnus_tujuan', 'tahun', 'dim_tahun', 'tahun'),
]

def table_tmdl(name):
    cols = TABLES[name]
    out = [f'table {name}', f'\tlineageTag: {G("tab-" + name)}', '']
    for mname, dax, fmt in MEASURES.get(name, []):
        if '\n' in dax:
            body = '\n'.join('\t\t\t' + ln for ln in dax.split('\n'))
            out.append(f"\tmeasure '{mname}' = ```")
            out.append(body)
            out.append('\t\t\t```')
        else:
            out.append(f"\tmeasure '{mname}' =")
            out.append(f'\t\t\t{dax}')
        out.append(f'\t\tformatString: {fmt}')
        out.append(f'\t\tlineageTag: {G("mea-" + name + "-" + mname)}')
        out.append('')
    for cname, dtype, fmt in cols:
        out.append(f'\tcolumn {cname}')
        out.append(f'\t\tdataType: {dtype}')
        if fmt:
            out.append(f'\t\tformatString: {fmt}')
        out.append(f'\t\tlineageTag: {G("col-" + name + "-" + cname)}')
        if (name, cname) in SORTBY:
            out.append(f'\t\tsortByColumn: {SORTBY[(name, cname)]}')
        out.append('\t\tsummarizeBy: none')
        out.append(f'\t\tsourceColumn: {cname}')
        out.append('')
    pairs = ', '.join(f'{{"{c}", {MTYPE[t]}}}' for c, t, _ in cols)
    out.append(f'\tpartition {name} = m')
    out.append('\t\tmode: import')
    out.append('\t\tsource = ```')
    out.append('\t\t\t\tlet')
    out.append(f'\t\t\t\t\tSource = Csv.Document(File.Contents(FolderData & "\\{name}.csv"), [Delimiter = ",", Columns = {len(cols)}, Encoding = 65001, QuoteStyle = QuoteStyle.None]),')
    out.append('\t\t\t\t\tPromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),')
    out.append(f'\t\t\t\t\tChangedType = Table.TransformColumnTypes(PromotedHeaders, {{{pairs}}})')
    out.append('\t\t\t\tin')
    out.append('\t\t\t\t\tChangedType')
    out.append('\t\t\t\t```')
    return '\n'.join(out) + '\n'

def build_model():
    WJ(SEM / '.platform', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platformProperties/1.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": PROJ},
        "config": {"version": "2.0", "logicalId": G('platform-sem')}})
    WJ(SEM / 'definition.pbism', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "settings": {}})
    W(DEF_S / 'database.tmdl', 'database\n\tcompatibilityLevel: 1600\n')
    refs = '\n'.join(f'ref table {t}' for t in TABLES)
    W(DEF_S / 'model.tmdl',
      f'model Model\n\tculture: en-US\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n{refs}\n\nref expression FolderData\n')
    W(DEF_S / 'expressions.tmdl',
      'expression FolderData = ```\n'
      '\t\t"C:\\\\PowerBI\\\\Pariwisata\\\\data" meta [IsParameterQuery = true, IsParameterQueryRequired = true, Type = "Text"]\n'
      '\t\t```\n'
      f'\tlineageTag: {G("expr-FolderData")}\n')
    rel = []
    for i, (ft, fc, tt, tc) in enumerate(RELATIONSHIPS):
        rel.append(f'relationship {G("rel-" + str(i))}')
        rel.append(f'\tfromColumn: {ft}.{fc}')
        rel.append(f'\ttoColumn: {tt}.{tc}')
        rel.append('\tcrossFilteringBehavior: oneDirection')
        rel.append('')
    W(DEF_S / 'relationships.tmdl', '\n'.join(rel))
    for t in TABLES:
        W(DEF_S / 'tables' / f'{t}.tmdl', table_tmdl(t))
    nodes = []
    for i, t in enumerate(list(TABLES)):
        nodes.append({"location": {"x": (i % 3) * 300, "y": (i // 3) * 260},
                      "nodeIndex": t, "nodeLineageTag": G('tab-' + t),
                      "size": {"height": 200, "width": 234}, "zIndex": i})
    WJ(SEM / 'diagramLayout.json', {
        "version": "1.1.0",
        "diagrams": [{"ordinal": 0, "scrollPosition": {"x": 0, "y": 0}, "nodes": nodes,
                      "name": "All tables", "zoomValue": 100, "pinKeyFields": [],
                      "showExtraHeaderInfo": False, "hideKeyFieldsWhenCollapsed": False}],
        "selectedDiagram": "All tables", "defaultDiagram": "All tables"})

# ------------------------------------------------------------------ report
DB = 'dim_bulan'; DT = 'dim_tahun'; FB = 'fact_wisman_bulanan'; FTA = 'fact_wisman_tahunan'
FP = 'fact_wisman_pintu'; FK = 'fact_wisman_kebangsaan'; FT = 'fact_tpk_provinsi'
FS = 'fact_tpk_snapshot'; FR = 'fact_rlm'; FW = 'fact_wisnus_tujuan'
NEG9 = ['Malaysia', 'Singapura', 'Australia', 'Tiongkok', 'Timor Leste', 'India',
        'Jepang', 'Korea Selatan', 'Filipina']
NEG8 = ['Malaysia', 'Australia', 'Tiongkok', 'Singapura', 'Timor Leste', 'India',
        'Jepang', 'Korea Selatan']

def build_report():
    WJ(REP / '.platform', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platformProperties/1.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": PROJ},
        "config": {"version": "2.0", "logicalId": G('platform-rep')}})
    WJ(REP / 'definition.pbir', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{PROJ}.SemanticModel"}}})
    WJ(DEF_R / 'version.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "1.0.0"})
    WJ(DEF_R / 'report.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
        "themeCollection": {"baseTheme": {"name": "CY24SU10", "reportVersionAtImport": "5.60", "type": "SharedResources"}}})
    WJ(REP / 'StaticResources' / 'SharedResources' / 'BaseThemes' / 'CY24SU10.json', {
        "name": "CY24SU10",
        "dataColors": ["#0B3C5D", "#3E7CA6", "#D7263D", "#F4B41A", "#197278", "#1AAB40",
                       "#744EC2", "#D9B300", "#118DFF", "#E66C37", "#6B007B", "#E044A7",
                       "#FF9B85", "#FFC36D", "#A0D8EF", "#5E4B8B"],
        "background": "#FFFFFF", "foreground": "#252423", "tableAccent": "#0B3C5D"})

    pages = {}

    # ---- Halaman 1: Ringkasan Eksekutif
    p1 = []
    p1.append(textbox('v01Title', 0, 0, 900, 60, 'Pariwisata Indonesia 2026 — Ringkasan Eksekutif', 22, z=0))
    p1.append(slicer('v02SlicerTahun', 930, 8, 330, 52, DT, 'tahun', z=1))
    cards = [(FTA, 'Kunjungan Wisman 2025', 'Kunjungan Wisman 2025', None),
             (FTA, 'Tingkat Pemulihan vs 2019', 'Pemulihan vs 2019 (tahun 2025)',
              [numfilter('dt', DT, 'tahun', [2025])]),
             (FTA, 'Kunjungan Wisman YTD 2026', 'Wisman YTD 2026 (Jan-Agu)', None),
             (FW, 'Wisnus 2025', 'Perjalanan Wisnus 2025', None)]
    for i, (e, m, t, flt) in enumerate(cards):
        p1.append(visual(f'v{3+i:02d}Card', i * 320, 76, 300, 110, 'card',
                         qstate={"Values": {"projections": [proj(mea(e, m), e, m)]}},
                         title_text=t, filters=flt, z=2 + i))
    p1.append(visual('v07LineBulanan', 0, 200, 620, 240, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(DB, 'bulan_singkat'), DB, 'bulan_singkat')]},
                             "Y": {"projections": [proj(mea(FB, 'Total Kunjungan Wisman'), FB, 'Total Kunjungan Wisman')]}},
                     title_text='Wisman Bulanan 2026 (puncak Agustus)',
                     filters=[numfilter('dt', DT, 'tahun', [2026])], z=6))
    p1.append(visual('v08ColTahunan', 640, 200, 620, 240, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(DT, 'tahun'), DT, 'tahun')]},
                             "Y": {"projections": [proj(agg(FTA, 'kunjungan_wisman', 0), FTA, 'kunjungan_wisman', 'Sum of kunjungan_wisman')]}},
                     title_text='Kunjungan Wisman Tahunan 2019-2026', z=7))
    p1.append(visual('v09DonutPintu', 0, 456, 620, 250, 'donutChart',
                     qstate={"Category": {"projections": [proj(col(FP, 'pintu_masuk'), FP, 'pintu_masuk')]},
                             "Y": {"projections": [proj(mea(FP, 'Pangsa Pintu Masuk'), FP, 'Pangsa Pintu Masuk')]}},
                     title_text='Pangsa Pintu Masuk 2025',
                     filters=[catfilter('fp', FP, 'periode', ['2025'])], z=8))
    p1.append(visual('v10BarPintu', 640, 456, 620, 250, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FP, 'pintu_masuk'), FP, 'pintu_masuk')]},
                             "Y": {"projections": [proj(mea(FP, 'Total Kunjungan Pintu'), FP, 'Total Kunjungan Pintu')]}},
                     title_text='Kunjungan per Gerbang 2025 — Ngurah Rai Teratas',
                     filters=[catfilter('fp', FP, 'periode', ['2025'])],
                     sorts=[sortby(mea(FP, 'Total Kunjungan Pintu'), 'Descending')], z=9))
    pages['pg01Ringkasan'] = ('Ringkasan Eksekutif', p1)

    # ---- Halaman 2: Pintu Masuk & Kebangsaan
    p2 = []
    p2.append(textbox('v01Title', 0, 0, 900, 60, 'Pintu Masuk & Kebangsaan', 22, z=0))
    p2.append(slicer('v02SlicerPeriode', 930, 8, 330, 52, FP, 'periode', z=1))
    p2.append(visual('v03BarPintu', 0, 76, 620, 300, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FP, 'pintu_masuk'), FP, 'pintu_masuk')]},
                             "Y": {"projections": [proj(mea(FP, 'Total Kunjungan Pintu'), FP, 'Total Kunjungan Pintu')]}},
                     title_text='Kunjungan per Gerbang (atur lewat slicer periode)',
                     sorts=[sortby(mea(FP, 'Total Kunjungan Pintu'), 'Descending')], z=2))
    p2.append(visual('v04BarModa', 640, 76, 620, 300, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FP, 'moda'), FP, 'moda')]},
                             "Y": {"projections": [proj(mea(FP, 'Total Kunjungan Pintu'), FP, 'Total Kunjungan Pintu')]}},
                     title_text='Kunjungan per Moda, Periode 2025',
                     filters=[catfilter('fp', FP, 'periode', ['2025'])],
                     sorts=[sortby(mea(FP, 'Total Kunjungan Pintu'), 'Descending')], z=3))
    p2.append(visual('v05ColKeb', 0, 392, 620, 300, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(FK, 'kebangsaan'), FK, 'kebangsaan')]},
                             "Y": {"projections": [proj(agg(FK, 'kunjungan', 0), FK, 'kunjungan', 'Sum of kunjungan')]},
                             "Series": {"projections": [proj(col(FK, 'periode'), FK, 'periode')]}},
                     title_text='Kebangsaan Teratas: 2019 vs 2023',
                     filters=[catfilter('fk', FK, 'periode', ['2019', '2023']),
                              catfilter('fk', FK, 'kebangsaan', NEG9)], z=4))
    p2.append(visual('v06BarKeb26', 640, 392, 620, 300, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FK, 'kebangsaan'), FK, 'kebangsaan')]},
                             "Y": {"projections": [proj(agg(FK, 'kunjungan', 0), FK, 'kunjungan', 'Sum of kunjungan')]}},
                     title_text='Kebangsaan Agustus 2026',
                     filters=[catfilter('fk', FK, 'periode', ['Agu 2026']),
                              catfilter('fk', FK, 'kebangsaan', NEG8)],
                     sorts=[sortby(agg(FK, 'kunjungan', 0), 'Descending')], z=5))
    pages['pg02PintuKebangsaan'] = ('Pintu Masuk & Kebangsaan', p2)

    # ---- Halaman 3: Hotel
    p3 = []
    p3.append(textbox('v01Title', 0, 0, 900, 60, 'Hotel: TPK & Lama Menginap', 22, z=0))
    p3.append(slicer('v02SlicerTahun', 930, 8, 330, 52, FT, 'tahun', z=1))
    p3.append(visual('v03BarTPK', 0, 76, 620, 300, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FT, 'provinsi'), FT, 'provinsi')]},
                             "Y": {"projections": [proj(mea(FT, 'Rata Rata TPK Provinsi'), FT, 'Rata Rata TPK Provinsi')]}},
                     title_text='TPK Bintang per Provinsi 2025 — Bali Tertinggi',
                     filters=[numfilter('ft', FT, 'tahun', [2025])],
                     sorts=[sortby(mea(FT, 'Rata Rata TPK Provinsi'), 'Descending')], z=2))
    p3.append(visual('v04BarSnap', 640, 76, 620, 300, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FS, 'provinsi'), FS, 'provinsi')]},
                             "Y": {"projections": [proj(agg(FS, 'tpk_persen', 0), FS, 'tpk_persen', 'Sum of tpk_persen')]}},
                     title_text='TPK Bintang Snapshot Desember 2025',
                     sorts=[sortby(agg(FS, 'tpk_persen', 0), 'Descending')], z=3))
    p3.append(visual('v05ColRLM', 0, 392, 620, 300, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(FR, 'kelompok_tamu'), FR, 'kelompok_tamu')]},
                             "Y": {"projections": [proj(mea(FR, 'RLM Rata Rata'), FR, 'RLM Rata Rata')]},
                             "Series": {"projections": [proj(col(FR, 'periode'), FR, 'periode')]}},
                     title_text='Rata-rata Lama Menginap Nasional (malam)',
                     filters=[catfilter('fr', FR, 'wilayah', ['Indonesia'])], z=4))
    p3.append(visual('v06CardRLM', 640, 392, 300, 140, 'card',
                     qstate={"Values": {"projections": [proj(mea(FR, 'RLM Rata Rata'), FR, 'RLM Rata Rata')]}},
                     title_text='RLM Tamu Asing Des 2025 (malam)',
                     filters=[catfilter('fr', FR, 'periode', ['Des 2025']),
                              catfilter('fr', FR, 'wilayah', ['Indonesia']),
                              catfilter('fr', FR, 'kelompok_tamu', ['Asing'])], z=5))
    p3.append(visual('v07CardTPK', 960, 392, 300, 140, 'card',
                     qstate={"Values": {"projections": [proj(mea(FT, 'Rata Rata TPK Provinsi'), FT, 'Rata Rata TPK Provinsi')]}},
                     title_text='Rata-rata TPK Provinsi 2025',
                     filters=[numfilter('ft', FT, 'tahun', [2025])], z=6))
    p3.append(textbox('v08Note', 640, 548, 620, 60,
                      'Catatan: visual peta diganti bar terurut (lebih aman di PBIP). Bali 61,02% adalah TPK provinsi tertinggi 2025.', 11, z=7))
    pages['pg03Hotel'] = ('Hotel: TPK & RLM', p3)

    # ---- Halaman 4: Wisnus
    p4 = []
    p4.append(textbox('v01Title', 0, 0, 900, 60, 'Wisatawan Nusantara (Wisnus)', 22, z=0))
    p4.append(slicer('v02SlicerTahun', 930, 8, 330, 52, FW, 'tahun', z=1))
    cards4 = [(FW, 'Wisnus 2025', 'Perjalanan Wisnus 2025'),
              (FW, 'Wisnus 2024', 'Perjalanan Wisnus 2024'),
              (FW, 'Pertumbuhan Wisnus Persen', 'Pertumbuhan Wisnus 2025')]
    for i, (e, m, t) in enumerate(cards4):
        p4.append(visual(f'v{3+i:02d}Card', i * 320, 76, 300, 110, 'card',
                         qstate={"Values": {"projections": [proj(mea(e, m), e, m)]}},
                         title_text=t, z=2 + i))
    p4.append(visual('v06BarTop', 0, 200, 620, 240, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(FW, 'provinsi'), FW, 'provinsi')]},
                             "Y": {"projections": [proj(mea(FW, 'Total Perjalanan Wisnus'), FW, 'Total Perjalanan Wisnus')]}},
                     title_text='Perjalanan Wisnus per Provinsi Tujuan 2025',
                     filters=[numfilter('fw', FW, 'tahun', [2025])],
                     sorts=[sortby(mea(FW, 'Total Perjalanan Wisnus'), 'Descending')], z=5))
    p4.append(visual('v07ColBanding', 640, 200, 620, 240, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(FW, 'provinsi'), FW, 'provinsi')]},
                             "Y": {"projections": [proj(mea(FW, 'Total Perjalanan Wisnus'), FW, 'Total Perjalanan Wisnus')]},
                             "Series": {"projections": [proj(col(DT, 'tahun'), DT, 'tahun')]}},
                     title_text='Top 5 Tujuan Wisnus: 2024 vs 2025',
                     filters=[catfilter('fw', FW, 'provinsi',
                                        ['Jawa Timur', 'Jawa Barat', 'Jawa Tengah',
                                         'DKI Jakarta', 'Banten'])], z=6))
    p4.append(visual('v08Table', 0, 456, 1260, 250, 'tableEx',
                     qstate={"Values": {"projections": [
                         proj(col(FW, 'provinsi'), FW, 'provinsi'),
                         proj(mea(FW, 'Wisnus 2024'), FW, 'Wisnus 2024'),
                         proj(mea(FW, 'Wisnus 2025'), FW, 'Wisnus 2025'),
                         proj(mea(FW, 'Pertumbuhan Wisnus Persen'), FW, 'Pertumbuhan Wisnus Persen')]}},
                     title_text='Wisnus per Provinsi: 2024, 2025, dan Pertumbuhannya',
                     sorts=[sortby(mea(FW, 'Wisnus 2025'), 'Descending')], z=7))
    pages['pg04Wisnus'] = ('Wisatawan Nusantara', p4)

    order = list(pages)
    for pname, (disp, visuals) in pages.items():
        WJ(DEF_R / 'pages' / pname / 'page.json', {
            "$schema": PG, "name": pname, "displayName": disp,
            "displayOption": "FitToPage", "height": 720, "width": 1280})
        for v in visuals:
            WJ(DEF_R / 'pages' / pname / 'visuals' / v['name'] / 'visual.json', v)
    WJ(DEF_R / 'pages' / 'pages.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": order, "activePageName": order[0]})

README = """PAKET POWER BI PROJECT (.pbip) — Pariwisata Indonesia 2026
=============================================================

Isi paket ini adalah project Power BI (format .pbip) yang sudah dirakit:
model data (10 tabel), 14 measure DAX, 5 relasi, dan 4 halaman dashboard.
Tinggal dibuka, diarahkan ke folder data, refresh, lalu simpan sebagai .pbix.

LANGKAH MEMBUKA
---------------
1. Extract zip ini di mana saja (misalnya D:\\PowerBI\\Pariwisata2026\\).
2. Buka file Pariwisata2026.pbip dengan Power BI Desktop.
3. Kalau data gagal dimuat (error FolderData): menu Modeling - Edit parameters
   - isi FolderData dengan path folder "data" hasil extract
   (contoh: D:\\PowerBI\\Pariwisata2026\\data) - OK - Refresh.
   Default parameter adalah C:\\PowerBI\\Pariwisata\\data.
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
"""

# --------------------------------------------------------------------- main
def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    (ROOT / 'data').mkdir(parents=True)
    for f in sorted(KIT.glob('*.csv')):
        shutil.copy(f, ROOT / 'data' / f.name)
    WJ(ROOT / f'{PROJ}.pbip', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{PROJ}.Report"}}],
        "settings": {"enableAutoRecovery": True}})
    W(ROOT / '.gitignore', '**/.pbi/localSettings.json\n**/.pbi/cache.abf\n')
    W(ROOT / 'README-LANGKAH.txt', README)
    build_model()
    build_report()
    print('built', ROOT)

if __name__ == '__main__':
    main()
