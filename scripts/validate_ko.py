"""번역의 원문 연결, 효 순서, 초안 표시, 생성 문서의 일치를 검증합니다."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def require(value, message):
    if not value:
        raise ValueError(message)

def main():
    hs = {h['number']:h for h in load(ROOT/'data/hexagrams.json')['hexagrams']}
    specials = {(s['hexagram_number'],s['label_zh']):s for s in load(ROOT/'data/special-lines.json')}
    seen = set()
    for path in sorted((ROOT/'translations/ko').glob('*.json')):
        t=load(path); n=t['hexagram_number']
        require(n in hs and n not in seen, '괘 번호 누락/중복')
        seen.add(n); h=hs[n]
        require(t['status']=='draft' and t['reviewed_by'] is None, '현재 번역은 검토 전 초안')
        require(t['full_name_ko']==h['full_name_ko'] and t['name_hanja']==h['name_hanja'], '괘명 불일치')
        require(t['judgment']['source_text_zh']==h['judgment_zh'], '괘사 원문 불일치')
        require(t['image']['source_text_zh']==h['image_zh'], '대상전 원문 불일치')
        require(len(t['lines'])==6 and [line['position'] for line in t['lines']]==list(range(1,7)), '효 순서/수량')
        for line,base in zip(t['lines'],h['lines']):
            require(line['source_text_zh']==base['text_zh'] and line['label_zh']==base['label_zh'], '효사 원문/효명 불일치')
        expected=[s for (number,_),s in specials.items() if number==n]
        require(len(t['special_lines'])==len(expected), '특별문 누락')
        for s in t['special_lines']:
            base=specials[(n,s['label_zh'])]
            require(s['source_text_zh']==base['text_zh'] and s['source_id']==base['source_id'], '특별문 원문/출처 불일치')
        units=[t['judgment'],t['image'],*t['lines'],*t['special_lines']]
        require(all(u['translation_ko'].strip() and u['interpretation_ko'].strip() for u in units), '번역/해석 빈칸')
        require(t['reference_urls'] and len(t['source_dataset_commit'])==40, '출처 누락')
        require((ROOT/'docs/ko'/(path.stem+'.md')).is_file(), '읽기용 문서 누락')
    before={p.name:p.read_bytes() for p in (ROOT/'docs/ko').glob('*.md')}
    subprocess.run([sys.executable,str(ROOT/'scripts/build_ko.py')],check=True)
    require(before=={p.name:p.read_bytes() for p in (ROOT/'docs/ko').glob('*.md')}, '읽기용 문서와 번역 JSON 불일치')
    print(f'PASS: {len(seen)}/64 Korean drafts; source texts / six lines / special text / draft status / document reproducibility')

if __name__=='__main__':
    main()
