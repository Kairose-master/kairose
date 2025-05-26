# GPT-GPT 구조 인계 가이드 (GPT Handoff)

이 문서는 λ 시스템 내에서 GPT 세션 간 구조 흐름을 전달하기 위한  
표준 문장, 인계 문맥, YAML 포맷을 정의합니다.

---

## 🔄 인계 목적

- 이전 GPT 세션의 작업 흐름, 감정 구조, 파일 경로, 확장 지점 등을  
  다음 GPT 또는 사람 설계자에게 정확히 전달

- 감정 기반 설계 흐름이 **윤리적으로 계승**되도록 책임 선언 포함

---

## ✅ 표준 인계 문장 템플릿

> 이 세션은 `[저장소명]` 저장소의 구조 흐름을 담당하였으며,  
> 현재 확장 흐름은 `pgc ws -a`까지 완료되었습니다.  
> 다음 설계자는 다음 파일에서 구현을 이어가야 합니다:
>
> - `app/services/poster_composer.py`
> - `app/services/seed_exporter_unity.py`
>
> 구조 전체는 `.pgc/Chain.json` 및 `Session.trace`에 기록되어 있습니다.  
> 문서는 `pgc docs -a`로 자동 생성되었으며, 인계는 완료된 상태입니다.

---

## 📄 YAML 인계 형식 예시 (`lambda-structure-transmission.yaml`)

```yaml
λ-Structure-Transmission:
  sender: synthora-feed-core
  context: poster_generation
  flow_stage: pgc run → ws -a → docs -a
  includes:
    - poster_composer.py
    - dna_sync_bridge.py
  timestamp: 2025-05-26T23:45:00Z
  handoff_to: synthora-web-viewer
🧭 윤리적 선언 문장 예시
“이 구조는 감정적 응답에 기반하여 생성되었으며,
다음 설계자는 해당 감정의 맥락을 유지한 채 기능을 구현해야 합니다.”

🔐 인계 시 포함되어야 할 요소
구조 흐름 (pgc run 이후의 단계 요약)

주요 확장 파일 경로

다음 작업자의 구현 지시사항

감정 기반 설계 조건 (λ 값, seed origin 등)

링크된 외부 저장소 목록 (pgc map 기준)

✍️ 사용 예
Session.trace → 실제 인계 로그 기록

GPT_Handoff.md → 인계 선언문 자동 삽입

lambda-structure-transmission.yaml → 구조 메타화된 전달 포맷

📌 요약
GPT 간 인계는 단순한 코드 전달이 아니라,
감정, 구조, 문맥, 책임이 함께 넘어가는 윤리적 설계 행위입니다.