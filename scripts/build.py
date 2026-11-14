"""고정된 공개 소스의 리터럴만 읽어서 JSON/CSV를 재생성합니다. 외부 코드를 실행하지 않습니다."""
import ast
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def literal(path, name):
    tree = ast.parse((ROOT / path).read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f'Missing literal: {name}')

def write_json(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def write_csv(path, rows, fields):
    with (ROOT / path).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def line_label(position, yang):
    yao = '九' if yang else '六'
    if position == 1:
        return '初' + yao
    if position == 6:
        return '上' + yao
    return yao + '二三四五'[position - 2]

def main():
    provenance = load('sources/provenance.json')
    for source in provenance['files']:
        actual = hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest()
        if actual != source['sha256']:
            raise ValueError(f"Source checksum mismatch: {source['path']}")
    texts = literal('sources/upstream/iching_texts.py.txt', 'ZHOUI')
    guamap = literal('sources/upstream/iching_coin.py.txt', 'GUAMAP')
    trigram_bits = literal('sources/upstream/iching_coin.py.txt', 'TRIGRAM')
    by_number = {number: pair for pair, number in guamap.items()}
    by_zh_bits = {name: list(bits) for bits, name in trigram_bits.items()}
    trigrams = load('metadata/trigrams.json')
    by_bits = {tuple(t['lines_bottom_to_top']): t for t in trigrams}
    korean = {n['number']: n for n in load('metadata/names-ko.json')}
    hexagrams, line_rows = [], []
    for source in texts:
        n = source['n']
        upper_zh, lower_zh = by_number[n]
        lower = by_bits[tuple(by_zh_bits[lower_zh])]
        upper = by_bits[tuple(by_zh_bits[upper_zh])]
        bits = lower['lines_bottom_to_top'] + upper['lines_bottom_to_top']
        meta = korean[n]
        full_name = ('중' + upper['nature_reading_ko'] if upper == lower else upper['nature_reading_ko'] + lower['nature_reading_ko']) + meta['name_ko']
        lines = []
        for position, (text, yang) in enumerate(zip(source['lines'], bits), 1):
            line = {'position': position, 'label_zh': line_label(position, yang), 'polarity': 'yang' if yang else 'yin', 'text_zh': text}
            lines.append(line)
            line_rows.append({'hexagram_number': n, 'hexagram_name_ko': full_name, **line, 'source_id': 'crane1102-zhouyi'})
        hexagrams.append({
            'number': n, 'name_ko': meta['name_ko'], 'full_name_ko': full_name,
            'name_hanja': meta['name_hanja'], 'source_name_zh': source['name'],
            'aliases_ko': meta['aliases_ko'], 'symbol': source['symbol'],
            'unicode_codepoint': f'U+{ord(source["symbol"]):04X}',
            'upper_trigram': upper['id'], 'lower_trigram': lower['id'],
            'lines_bottom_to_top': bits, 'binary_bottom_to_top': ''.join(map(str,bits)),
            'judgment_zh': source['judgment'], 'lines': lines, 'image_zh': source['image'],
            'text_language': 'zh-Hans', 'source_id': 'crane1102-zhouyi',
            'korean_translation': None,
        })
    hexagrams.sort(key=lambda h: h['number'])
    data = {'schema_version': '1.0.0', 'dataset_version': provenance['dataset_version'], 'line_order': 'bottom-to-top', 'polarity_encoding': {'0': 'yin', '1': 'yang'}, 'hexagrams': hexagrams}
    write_json('data/hexagrams.json', data)
    write_json('data/trigrams.json', {'line_order': 'bottom-to-top', 'trigrams': trigrams})
    special = load('metadata/special-lines.json')
    write_json('data/special-lines.json', special)
    fields = ['number','name_ko','full_name_ko','name_hanja','source_name_zh','symbol','unicode_codepoint','upper_trigram','lower_trigram','binary_bottom_to_top','judgment_zh','image_zh','source_id']
    write_csv('data/hexagrams.csv', [{key:h[key] for key in fields} for h in hexagrams], fields)
    write_csv('data/lines.csv', line_rows, ['hexagram_number','hexagram_name_ko','position','label_zh','polarity','text_zh','source_id'])
    write_csv('data/special-lines.csv', special, list(special[0]))
    print(f'Built {len(hexagrams)} hexagrams, {len(line_rows)} ordinary lines, {len(special)} special texts, {len(trigrams)} trigrams')

if __name__ == '__main__':
    main()
