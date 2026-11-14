from pathlib import Path
from collections import Counter, defaultdict
import csv, gzip, json

root = Path(__file__).resolve().parent
def read(name):
    path = root / name
    if not path.exists() and name == 'vahan_2025_working.csv':
        with gzip.open(root / (name + '.gz'), 'rt', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write(name, header, rows):
    with (root / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

rows = read('vahan_2025_working.csv')
checks = read('monthly_checks.csv')
months = [f'2025-{i:02d}-01' for i in range(1, 13)]
total, annual = Counter(), defaultdict(Counter)
by = defaultdict(Counter)
sources, keys = defaultdict(set), set()
for r in rows:
    m, maker, fuel, n, s = (r[k] for k in ('month','maker','fuel','registrations','source_file'))
    key = m, maker, fuel
    assert all(x.strip() for x in r.values()) and key not in keys and m in months
    keys.add(key)
    n = int(n)
    assert n >= 0
    total[m] += n
    sources[m].add(s)
    for kind, label in [('maker',maker), ('fuel',fuel), ('maker_fuel',(maker,fuel))]:
        by[kind,m][label] += n
        annual[kind][label] += n
assert set(total) == set(months)
for m, c in zip(months, checks, strict=True):
    assert total[m] == int(c['registrations']) and sources[m] == {c['source_file']}
grand = sum(total.values())
def growth(a,b):
    return (b-a)/a*100 if a else None

monthly = []
for i,m in enumerate(months):
    p = months[i-1] if i else None
    monthly.append([m,total[m],total[m]-total[p] if p else None,growth(total[p],total[m]) if p else None,len(by['maker',m]),len(by['fuel',m])])
write('monthly_growth.csv',['month','registrations','change','growth_pct','maker_labels','fuel_labels'],monthly)
quarters = [sum(total[m] for m in months[i:i+3]) for i in range(0,12,3)]
write('quarterly_growth.csv',['quarter','registrations','change','growth_pct'],[[i+1,n,n-quarters[i-1] if i else None,growth(quarters[i-1],n) if i else None] for i,n in enumerate(quarters)])
for kind in ['maker','fuel']:
    write(f'{kind}_annual.csv',[kind,'registrations','share_pct'],[[k,n,n/grand*100] for k,n in annual[kind].most_common()])
    detail = []
    for p,m in zip(months,months[1:]):
        a,b = by[kind,p],by[kind,m]
        assert sum(b[k]-a[k] for k in a.keys()|b.keys()) == total[m]-total[p]
        for k in sorted(a.keys()|b.keys()):
            x,y = a.get(k),b.get(k)
            paired = x is not None and y is not None
            detail.append([m,k,x,y,y-x if paired else None,growth(x,y) if paired else None,(y/total[m]-x/total[p])*100 if paired else None,b[k]-a[k], 'both present' if paired else 'absent in one export'])
    write(f'{kind}_movement.csv',['month',kind,'previous','current','matched_change','growth_pct','share_change_pp','export_contribution','coverage'],detail)
write('maker_fuel_mix.csv',['month','maker','fuel','registrations','share_within_maker_pct'],[[m,k,f,n,n/by['maker',m][k]*100 if by['maker',m][k] else None] for m in months for (k,f),n in sorted(by['maker_fuel',m].items()) if n])
write('concentration.csv',['month','top_5_share_pct','top_10_share_pct'],[[m,*[sum(v for _,v in by['maker',m].most_common(i))/total[m]*100 for i in (5,10)]] for m in months])
sensitivity=[]
for threshold in (100,1000,10000):
    for p,m in zip(months,months[1:]):
        a,b=by['maker',p],by['maker',m]
        ranked=sorted(((growth(a[k],b[k]),k,a[k],b[k]) for k in a.keys()&b.keys() if a[k]>=threshold),key=lambda x:(-x[0],x[1]))
        sensitivity.extend([m,threshold,i,k,x,y,g] for i,(g,k,x,y) in enumerate(ranked[:10],1))
write('growth_rank_sensitivity.csv',['month','minimum_prior_count','rank','maker','previous','current','growth_pct'],sensitivity)
for kind in ('maker','fuel'):
    for p,m in [('2025-09-01','2025-10-01'),('2025-11-01','2025-12-01')]:
        a,b=by[kind,p],by[kind,m]
        d=Counter({k:b[k]-a[k] for k in a.keys()|b.keys()})
        print(kind,m,d.most_common(4),d.most_common()[-4:])
print(json.dumps(dict(rows=len(rows), makers=len(annual['maker']), fuels=len(annual['fuel']), total=grand, monthly=monthly, quarters=quarters, top_makers=annual['maker'].most_common(5),top_fuels=annual['fuel'].most_common(8))))
