# 구조 흐름 설계: Chain.json 참조 기반

이 문서는 `.pgc/Chain.json`에 명시된 구조 흐름을 설명합니다.

---

## 예시 흐름

```json
"flow": [
  "run → scaffold",
  "ws -a → auto-implement",
  "ws -t → testgen",
  "docs -a → doc augmentation",
  "map --infer → auto linking"
]
