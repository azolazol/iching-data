"""한국어 번역 JSON에서 읽기용 문서를 생성합니다."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def section(title, unit):
    rows = [f'## {title}', '', f'원문: {unit["source_text_zh"]}', '', f'**번역:** {unit["translation_ko"]}', '', f'**해석:** {unit["interpretation_ko"]}', '']
    if unit.get('modern_application_ko'):
        rows += [f'**현대 적용:** {unit["modern_application_ko"]}', '']
    if unit.get('notes_ko'):
        rows += ['읽기 메모:', ''] + [f'- {note}' for note in unit['notes_ko']] + ['']
    return rows

def main():
    folder = ROOT/'docs/ko'
    folder.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted((ROOT/'translations/ko').glob('*.json')):
        t = json.loads(path.read_text(encoding='utf-8'))
        rows = [f'# 제{t["hexagram_number"]}괘 {t["full_name_ko"]}({t["name_hanja"]}) · 한국어 번역과 풀이', '',
                f'작성: {t["author_display_name"]} · {t["created_on"]} · 번역 버전 {t["translation_version"]} · **검토 전 초안**', '',
                f'**한 문장으로:** {t["summary_ko"]}', '',
                '## 이번 글의 범위', '']
        rows += [f'- {value}' for value in t['editorial_policy'].values()] + ['']
        rows += section('괘사', t['judgment'])
        for line in t['lines']:
            rows += section(f'{line["label_ko"]}({line["label_zh"]}) · 제{line["position"]}효', line)
        rows += section('대상전', t['image'])
        for line in t['special_lines']:
            rows += section(f'{line["label_ko"]}({line["label_zh"]}) · 특별문', line)
        rows += ['## 전체를 읽을 때', ''] + [f'- {note}' for note in t['reading_notes_ko']] + ['']
        rows += ['## 출처와 작성 방식', '',
                 f'한문 기준: 기본 데이터 커밋 `{t["source_dataset_commit"]}`. 원문의 간체자와 구두점을 기록하고 한국어 문장에서는 선택한 독법을 별도로 설명했습니다.', '',
                 '고전 원문과 문언전·상전의 설명을 참고해 한국어 문장을 새로 작성했습니다. 기존 현대 한국어 번역을 전재하지 않았습니다. 현대 적용은 이 프로젝트에서 덧붙인 예시입니다.', '']
        rows += [f'- [참고 원문 {i+1}]({url})' for i,url in enumerate(t['reference_urls'])]
        rows += ['', f'[기계가 읽는 번역 JSON](../../translations/ko/{path.name})', '', '이 프로젝트의 번역·해석·문서는 MIT 조건으로 제공합니다.']
        (folder/(path.stem+'.md')).write_text('\n'.join(rows)+'\n', encoding='utf-8')
        count += 1
    print(f'Built {count} Korean draft document(s)')

if __name__ == '__main__':
    main()
