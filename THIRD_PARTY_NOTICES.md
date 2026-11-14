# 출처 및 이용 조건

## 상류 전자자료

- 저장소: https://github.com/crane1102/iching-llm
- 고정 커밋: `7bb5d7b1fc3a5f0f331b38673ed3b9d2ce882443`
- 추출 대상: `backend/iching_texts.py`의 `ZHOUI`, `backend/iching_coin.py`의 `TRIGRAM` 및 `GUAMAP`
- 이용허락: MIT, Copyright (c) 2026 crane1102
- 이용허락 전문: [licenses/crane1102-MIT.txt](licenses/crane1102-MIT.txt)
- 원본 보관본: `sources/upstream/` (실행하지 않는 `.txt` 파일)
- 상류 문서에서는 한문 내용을 공유 영역인 고전 《周易》의 통행본으로 설명합니다. 이 저장소에서는 그 주장만으로 현대 편집물까지 공유 영역으로 취급하지 않고, 전자자료에 명시된 MIT 고지를 함께 유지합니다.

## 고전 특별문과 참고 자료

건괘 용구 및 곤괘 용육은 아래 공개 페이지에서 확인한 고전 글자열을 무구두점으로 별도 기록했습니다. 해당 사이트의 현대 한국어/중국어 번역·설명, 페이지 구성, 주석은 복제하지 않았습니다. 고전 원문의 출처 표시는 고전과 현대 편집물의 권리를 구분하기 위한 것입니다.

- https://zh.wikisource.org/wiki/周易/乾
- https://zh.wikisource.org/wiki/周易/坤

기본 데이터의 표본 대조 참고:

- https://zh.wikisource.org/wiki/周易/既濟
- https://zh.wikisource.org/wiki/周易/未濟

기호 순서 참고:

- https://www.unicode.org/charts/nameslist/n_4DC0.html

## 이 프로젝트의 추가분

추출·검증 스크립트, 한국어 이름 등 새로 작성한 메타데이터와 문서는 [LICENSE](LICENSE)의 MIT 조건을 적용합니다. 고전 자체에 독점권을 주장하지 않습니다. 사용자가 추후 추가하는 번역·주석·이미지는 해당 자료의 별도 권리를 확인하고 고지해야 합니다.

`translations/ko/`의 한국어 번역·해석·현대 적용은 이 프로젝트에서 새로 작성한 검토 전 초안이며 MIT 조건으로 제공합니다. 참고한 고전 원문·전통 주석의 페이지와 선택한 독법을 각 레코드에 기록합니다. 기존 현대 한국어 번역은 전재하지 않습니다. 생성된 읽기용 문서는 `docs/ko/`에 있습니다.
