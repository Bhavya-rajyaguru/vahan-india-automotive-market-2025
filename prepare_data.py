from pathlib import Path
import csv, re, zipfile, json, sys
import xml.etree.ElementTree as ET

folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'upload'
output = Path(__file__).resolve().parent
selected = {1:'-2.csv',2:'-3.csv',3:'-4.csv',4:'-5.csv',5:'-6.csv',6:'-7.csv',8:'-8.csv',9:'-13.csv',10:'-14.csv',11:'-15.csv',12:'-12(2).csv'}
records = []
checks = []
for month in range(1,13):
    if month == 7:
        file = folder / 'maker_vehicleFuel_2026_all_records.xlsx'
        ns = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        with zipfile.ZipFile(file) as z:
            strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                strings = [''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
            rows = []
            for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('m:sheetData/m:row',ns):
                cells = {}
                for cell in row:
                    letters = re.match('[A-Z]+',cell.attrib['r'])[0]
                    index = 0
                    for letter in letters: index = index*26 + ord(letter)-64
                    value = cell.find('m:v',ns)
                    inline = cell.find('m:is',ns)
                    text = value.text if value is not None else ''
                    if cell.get('t') == 's': text = strings[int(text)]
                    elif inline is not None: text = ''.join(inline.itertext())
                    cells[index-1] = text
                rows.append([cells.get(i,'') for i in range(max(cells,default=-1)+1)])
    else:
        file = folder / ('maker_vehicleFuel_2026_all_records'+selected[month])
        with file.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.reader(f))
    header_index = next(i for i,r in enumerate(rows) if r and r[0]=='Maker')
    header = rows[header_index]
    makers = set()
    total = 0
    for row in rows[header_index+1:]:
        if not row or not any(row): continue
        assert len(row)==len(header),(file.name,row)
        assert row[0] not in makers,(file.name,row[0])
        makers.add(row[0])
        values=[int(v.replace(',','')) for v in row[1:]]
        assert all(v>=0 for v in values)
        assert sum(values[:-1])==values[-1]
        total+=values[-1]
        for fuel,count in zip(header[1:-1],values[:-1]):
            records.append([f'2025-{month:02d}-01',row[0],fuel,count,file.name])
    checks.append([month,file.name,rows[0][0],len(makers),len(header)-2,total])
with (output/'vahan_2025_working.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['month','maker','fuel','registrations','source_file']);w.writerows(records)
with (output/'monthly_checks.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['month','source_file','report_title','maker_rows','fuel_columns','registrations']);w.writerows(checks)
assert len({(r[0],r[1],r[2]) for r in records})==len(records)
print(json.dumps({'months':len(checks),'rows':len(records),'makers':len(set(r[1] for r in records)),'registrations':sum(r[3] for r in records),'monthly':checks}))
