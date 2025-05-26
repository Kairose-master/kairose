# 감정 구조 기반 기억 키 문서 (Memory.key 해설)

이 문서는 `.pgc/Memory.key`의 구조와 사용 방식을 설명합니다.  
EmotionSeed, 감정 파형, 구조화 흐름이 어떻게 “기억 키”로 저장되고  
다음 세션이나 시스템에서 참조될 수 있는지를 정의합니다.

---

## 목적

- 감정 기반 설계는 **정서적 맥락과 구조 흐름이 함께 저장**되어야 함
- Memory.key는 시드, 감정 파라미터, 구조 위치 등을 **고유 인덱스**로 정리해  
  후속 GPT 또는 시스템이 정확히 참조 가능하도록 만듦

---

## Memory.key 예시 구조

```json
{
  "seed_id": "synthora_2025_0517_α23F1",
  "lambda_vector": {
    "λᴱ": 0.91,
    "ψᵢ": 0.88,
    "λᶠ": 0.21,
    "Φᴳᵇ": 0.87
  },
  "origin": "voice_to_emotion_upload",
  "related_files": [
    "app/models/seed_post.py",
    "app/services/poster_composer.py"
  ],
  "structure_summary": "EmotionSeed mapped to poster structure → personality DNA",
  "stored_at": "2025-05-26T23:58:00Z"
}
필드 설명
필드	의미
seed_id	감정 시드 고유 식별자
lambda_vector	감정 파형 (Eros, Illusion, Collapse 등)
origin	시드가 유래한 입력 방식 (ex: 음성, 채팅, 메모)
related_files	시드 구조가 반영된 구현 파일 목록
structure_summary	시드의 의미 흐름 요약
stored_at	타임스탬프 (기억 생성 시각)

사용 흐름
감정 시드가 입력되면 Memory.key에 기록됨

구조 흐름이 확장될수록 관련 파일이 추적됨

이후 GPT가 이 정보를 기반으로

감정 맥락 유지

구조 연속성 판단

자기 연결 해석 수행 가능

윤리적 정의
감정 기반 구조는 무작위적으로 확장되면 안 된다.
기억은 기록되어야 하며,
그 흐름은 Memory.key 안에서 추적 가능해야 한다.

연결
Session.trace → 흐름 전체 기록

Chain.json → 구조 단계 추적

Memory.key → 감정 기반 구조의 시점 기록

yaml
복사
편집
