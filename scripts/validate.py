"""누락/중복, 음양 순서, 효명, 출처, CSV 일치 및 재현성을 검사합니다."""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def csv_rows(path):
    with (ROOT/path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def main():
    data = load('data/hexagrams.json')
    hs = data['hexagrams']
    ts = load('data/trigrams.json')['trigrams']
    require(len(hs)==64 and [h['number'] for h in hs]==list(range(1,65)), '64괘 문왕 순서')
    require(len(ts)==8 and len({tuple(t['lines_bottom_to_top']) for t in ts})==8, '팔괘 중복/누락')
    trigrams = {t['id']:t for t in ts}
    patterns = {h['binary_bottom_to_top']:h['number'] for h in hs}
    require(len(patterns)==64 and sum(len(h['lines']) for h in hs)==384, '64 패턴/384효')
    sources = {s['id'] for s in load('sources/provenance.json')['sources']}
    for h in hs:
        n = h['number']; bits = h['lines_bottom_to_top']
        require(len(bits)==6 and all(type(b) is int and b in (0,1) for b in bits), f'{n}: 음양')
        require(h['symbol']==chr(0x4DC0+n-1), f'{n}: Unicode 순서')
        require(h['unicode_codepoint']==f'U+{ord(h["symbol"]):04X}', f'{n}: Unicode 코드')
        require(h['binary_bottom_to_top']==''.join(map(str,bits)), f'{n}: 비트 문자열')
        require(bits[:3]==trigrams[h['lower_trigram']]['lines_bottom_to_top'], f'{n}: 하괘 순서')
        require(bits[3:]==trigrams[h['upper_trigram']]['lines_bottom_to_top'], f'{n}: 상괘 순서')
        require(len(h['lines'])==6 and [x['position'] for x in h['lines']]==list(range(1,7)), f'{n}: 효 순서')
        for pos,line in enumerate(h['lines'],1):
            y = '九' if bits[pos-1] else '六'
            expected = '初'+y if pos==1 else '上'+y if pos==6 else y+'二三四五'[pos-2]
            require(line['label_zh']==expected and line['polarity']==('yang' if bits[pos-1] else 'yin'), f'{n}: 효명/음양')
            require(bool(line['text_zh'].strip()), f'{n}: 빈 효사')
        require(bool(h['judgment_zh'].strip()) and bool(h['image_zh'].strip()), f'{n}: 빈 괘사/대상전')
        require(h['source_id'] in sources and h['korean_translation'] is None, f'{n}: 출처/번역 상태')
    # 서로 다른 팔괘가 결합되는 대표 사례로 위아래 순서 혼동 방지.
    require(patterns['100010']==3 and patterns['010001']==4, '둔/몽 방향')
    require(patterns['101010']==63 and patterns['010101']==64, '기제/미제 방향')
    for pattern in patterns:
        require(''.join('1' if b=='0' else '0' for b in pattern) in patterns, '착괘 누락')
        require(pattern[::-1] in patterns, '종괘 누락')
    require(len(csv_rows('data/hexagrams.csv'))==64, '괘 CSV 행수')
    require(len(csv_rows('data/lines.csv'))==384, '효 CSV 행수')
    for row in csv_rows('data/hexagrams.csv'):
        h = hs[int(row['number'])-1]
        require(all(str(h[k])==v for k,v in row.items()), '괘 CSV/JSON 불일치')
    for row in csv_rows('data/lines.csv'):
        h = hs[int(row['hexagram_number'])-1]; line = h['lines'][int(row['position'])-1]
        require(row['text_zh']==line['text_zh'] and row['label_zh']==line['label_zh'] and row['polarity']==line['polarity'], '효 CSV/JSON 불일치')
    special=load('data/special-lines.json')
    require(len(special)==2 and [s['hexagram_number'] for s in special]==[1,2], '용구/용육')
    require(all(s['source_id'] in sources for s in special), '특별문 출처')
    require([{k:str(v) for k,v in row.items()} for row in special]==csv_rows('data/special-lines.csv'), '특별문 CSV/JSON 불일치')
    for source in load('sources/provenance.json')['files']:
        require(hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256'], '원본 체크섬')
    outputs = sorted((ROOT/'data').glob('*'))
    before={p.name:p.read_bytes() for p in outputs}
    subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True)
    require(before=={p.name:p.read_bytes() for p in outputs}, '재생성 결과 불일치')
    print('PASS: 64괘 / 384효 / 용구·용육 2문 / 8팔괘 / 출처 체크섬 / CSV-JSON 일치 / 재현성')

if __name__=='__main__':
    main()
