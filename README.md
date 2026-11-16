# 주역 데이터 · I Ching Data

공개 자료에서 추출한 주역 64괘의 기본 데이터입니다. 웹앱·학습 도구에서 JSON 또는 CSV로 사용할 수 있습니다.

**버전 0.1.0 · 수집 기준일 2026-11-15**

## 수록 범위

| 항목 | 수량 | 내용 |
| --- | ---: | --- |
| 64괘 | 64 | 문왕 순서, 한국어·한자 괘명, Unicode 기호, 상괘·하괘, 음양 배열 |
| 괘사 | 64 | 공개 전자자료의 한문 원문(주로 간체자) |
| 효사 | 384 | 초효→상효 순서, 효명, 음양, 원문 |
| 대상전 | 64 | 각 괘의 `象曰` 대표 구절. 소상전과 구분 |
| 용구·용육 | 2 | 일반 384효와 별도인 건·곤의 특별문 |
| 팔괘 | 8 | 이름, 자연 상징, 기호, 세 효 배열 |

기본 원문 JSON의 `korean_translation`은 `null`로 유지합니다. 새로 작성하는 한국어 번역·풀이는 아래 별도 초안 파일에서 제공합니다. 십익 전체를 수록한 주역 완역본은 아닙니다.

## 한국어 번역·풀이 · 천천히 한 괘씩

현재 **1/64괘, 검토 전 초안**입니다. 작성자 표시명은 채리이며, 기존 현대 한국어 번역을 옮기지 않고 이 프로젝트에서 직접 작성합니다. **원문 → 한글 독음 → 번역 → 해석 → 현대 적용** 순서로 읽을 수 있으며, 뜻이 갈리는 부분에는 선택한 독법을 설명합니다.

한글 독음은 중국어 발음을 옮긴 병음이 아니라 **한국 한자음**입니다. 예: 潛龍勿用 → 잠룡물용. 토·조사를 붙이지 않고, 문맥에 따라 見龍의 見은 '현', 利見의 見은 '견'으로 읽습니다.

| 괘 | 읽기용 문서 | 앱용 JSON | 상태 |
| --- | --- | --- | --- |
| 제1괘 중천건(乾) | [독음·번역·풀이 읽기](docs/ko/001-qian.md) | [번역 JSON](translations/ko/001-qian.json) | 초안 0.1.1 |

나머지 괘에는 아직 번역을 작성하지 않았습니다. 기존 한문 데이터 버전은 0.1.0이며, 번역은 별도 `translation_version`으로 관리합니다. `status: draft`인 내용을 검토 완료 번역과 구분해서 사용하세요.

```bash
python scripts/build_ko.py
python scripts/validate_ko.py
```

한문 원문 연결, 여섯 효 순서, 특별문, 독음 누락·음절 수, 초안 상태, 읽기용 문서의 재생성을 검사합니다. 이 검사는 번역이나 독음의 인문학적 타당성을 자동으로 판정하지 않습니다.

## 파일

| 파일 | 사용 목적 |
| --- | --- |
| [data/hexagrams.json](data/hexagrams.json) | 앱에서 읽는 기본 파일. `hexagrams` 배열에 64괘 |
| [data/hexagrams.csv](data/hexagrams.csv) | 엑셀·구글 시트용 64괘 표 |
| [data/lines.csv](data/lines.csv) | 384효를 한 행씩 저장한 표 |
| [data/trigrams.json](data/trigrams.json) | 팔괘 8개 |
| [data/special-lines.json](data/special-lines.json) | 건괘 용구·곤괘 용육 |
| [sources/provenance.json](sources/provenance.json) | 출처 URL, 고정 커밋, SHA-256, 범위·검증 한계 |
| [docs/data-dictionary.md](docs/data-dictionary.md) | 필드 및 배열 방향 설명 |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | 이용 조건 및 출처 고지 |

## JavaScript에서 읽기

GitHub에서 `data/hexagrams.json`을 열고 **Raw** 주소를 복사해 `fetch()`에 사용하세요. 서비스에서는 브랜치 주소보다 특정 커밋에 고정한 주소를 권장합니다.

```js
const response = await fetch(DATA_URL); // 복사한 Raw JSON 주소
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const { hexagrams } = await response.json();
const first = hexagrams.find(h => h.number === 1);
console.log(first.full_name_ko); // 중천건
console.log(first.lines[0].label_zh); // 初九
```

로컬 예제: `node examples/read.mjs`

## 배열 규칙

`lines_bottom_to_top`과 `binary_bottom_to_top`은 **아래→위**, `0=음`, `1=양`입니다. 문자열을 일반적인 위→아래 도식으로 오해하지 마세요. 화면에 그릴 때는 배열의 복사본을 뒤집습니다.

예: 제3괘 수뢰둔은 `[1,0,0,0,1,0]`입니다. 처음 3효는 하괘 진(震), 뒤 3효는 상괘 감(坎)입니다.

한글 괘명에는 표기 차이가 있습니다. 제3괘 `둔/준`, 제33괘 `둔/돈` 등은 `aliases_ko`에 함께 기록합니다. 한자 명칭은 한국어 표시용 메타데이터이며, 본문 전체를 번체자로 변환한 것은 아닙니다.

## 재생성·검증

Python 3.10+ 표준 라이브러리만 필요하며, 다음 과정에는 인터넷 연결이 필요하지 않습니다.

```bash
python scripts/build.py
python scripts/validate.py
```

추출 스크립트는 보관된 원본의 SHA-256을 확인한 뒤 Python AST의 리터럴 상수만 읽습니다. 원본 코드를 import하거나 실행하지 않습니다. 검증은 64괘·384효의 누락/중복, 상하괘 방향, 효명, Unicode 순서, 출처, CSV-JSON 일치, 재생성 결과를 확인합니다.

## 출처·정확도

기본 한문 데이터와 상하괘 매핑은 [crane1102/iching-llm](https://github.com/crane1102/iching-llm)의 MIT 자료에서 추출했고, 커밋 `7bb5d7b1fc3a5f0f331b38673ed3b9d2ce882443`에 고정했습니다. 원본과 이용허락 문구를 함께 보관합니다.

건·곤·기제·미제의 공개 원문 페이지를 표본 참고했습니다. **전 괘의 고판본 대조 및 글자별 교감은 완료하지 않았습니다.** 상류 자료의 간체자·이체자·구두점을 보존한 개발용 초판입니다. 한국어 이름 추가나 구조 검사 통과를 본문 전체의 학술적 정확성 검증으로 해석해서는 안 됩니다.

고전 원문과 현대 번역·주석은 이용 조건이 다를 수 있습니다. 인터넷에 공개되어 있다는 이유만으로 현대 한국어 번역을 복사하지 않았습니다. 재배포 시 MIT 고지와 출처 기록을 유지하세요.

## 다음 확장

1. 괘별 교감 기록과 수정 이력 추가
2. 자체 작성 한국어 직역·풀이를 원문 필드와 분리해 추가
3. 단전·소상전 및 나머지 십익 자료를 출처별로 추가
4. 데이터 구조 확정 후 검색·학습·괘상 시각화 앱에서 사용
