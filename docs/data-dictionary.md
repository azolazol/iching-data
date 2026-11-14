# 데이터 사전

JSON은 UTF-8, CSV는 Excel 호환을 위해 UTF-8 BOM과 표준 CSV 인용 규칙을 사용합니다. `binary_bottom_to_top`은 선행 0을 보존해야 하므로 스프레드시트 가져오기에서 문자열로 지정하세요.

| 필드 | 형식 | 의미 |
| --- | --- | --- |
| `number` | integer 1–64 | 문왕 괘서 |
| `name_ko` | string | 한글 약칭. 중복될 수 있어 식별자로 사용하지 않음 |
| `full_name_ko` | string | 상하괘를 포함한 통상 이름 |
| `name_hanja` | string | 한국어 표시용 한자 괘명 |
| `source_name_zh` | string | 원본 전자자료의 괘명 |
| `aliases_ko` | string[] | 추가 검색 별칭 |
| `symbol` | string | U+4DC0–U+4DFF의 괘상 기호 |
| `unicode_codepoint` | string | Unicode 코드 표기 |
| `upper_trigram` / `lower_trigram` | string | 팔괘 JSON의 `id` 참조 |
| `lines_bottom_to_top` | integer[6] | 아래→위, 0=음, 1=양 |
| `binary_bottom_to_top` | string | 위 배열의 여섯 자리 문자열. 정수 변환 금지 |
| `judgment_zh` | string | 괘사 |
| `lines` | object[6] | 초효→상효의 효사. 각 객체는 `position`, `label_zh`, `polarity`, `text_zh` |
| `image_zh` | string | 대상전. 여섯 개 소상전은 포함하지 않음 |
| `text_language` | string | 기본 전자자료는 `zh-Hans`; 일부 전통 글자가 혼재할 수 있음 |
| `source_id` | string | provenance의 `sources[].id` 참조 |
| `korean_translation` | null | 기본 원문 JSON에서는 유지. 별도 `translations/ko/`의 초안과 구분 |

최상위 `schema_version`은 구조 버전, `dataset_version`은 데이터 릴리스 버전입니다. `special-lines.json`은 용구·용육 두 문장만 담고, 384개의 효사 배열에 일곱째 효로 섞지 않습니다.

효명은 위치만으로 홀짝을 배정하지 않습니다. 해당 효가 양이면 九, 음이면 六이며 첫째는 初九/初六, 여섯째는 上九/上六입니다.

`metadata/`는 직접 작성한 명칭·팔괘·특별문 입력이며, `sources/upstream/*.txt`는 고정된 상류 소스의 보관본입니다. 데이터 수정 시 관련 입력과 출처를 수정하고 다시 생성·검증하세요.

## 한국어 초안

`translations/ko/NNN-name.json`은 해당 괘만의 독립적인 번역 레코드입니다. `hexagram_number`로 기본 데이터에 연결합니다.

| 필드 | 의미 |
| --- | --- |
| `translation_version` | 번역 내용의 버전. 기본 데이터 버전과 별개 |
| `status`, `reviewed_by` | 현재 `draft`, `null`. 검토 전임을 명시 |
| `source_dataset_commit` | 번역 기준으로 삼은 원문 저장소의 커밋 |
| `reference_urls` | 참고한 고전 원문·주석 페이지 |
| `editorial_policy` | 번역·해석·현대 적용의 작성 기준과 범위 |
| `judgment`, `image` | 괘사 및 대상전의 `source_text_zh`, `translation_ko`, `interpretation_ko`, `notes_ko` |
| `lines` | 초효→상효의 여섯 객체. 위 필드 외에 `position`, `label_zh`, `label_ko`, `modern_application_ko` |
| `special_lines` | 용구·용육 등 특별문. 일반 여섯 효와 분리 |
| `summary_ko`, `reading_notes_ko` | 한 줄 요약과 전체 읽기 메모 |

`source_text_zh`는 기본 데이터와 글자·구두점까지 일치시켜 연결을 검사합니다. 다른 구두점이나 독법을 택할 때는 원문 필드를 고치지 않고 `notes_ko`에 설명합니다. 읽기용 Markdown은 `scripts/build_ko.py`로 생성하며 번역 원본은 JSON입니다.
