# KAIROSE KEYWORD SPECIFICATION (v1.0)

이 문서는 Kairose 언어의 공식 키워드 36개를  
역할별로 분류하고, 각 키워드의 **의미, 사용 형식, 예시**를 제공한다.

---

## 1. SYSTEM & MODULE CONTROL

### `use`
> 시스템/모듈 활성화 선언
```kairose
use lambda-mental-care
import
외부 시드/구조/기억 불러오기

import seed from synthora-core
from
import와 함께 사용


import memory from external_seed
as
별칭 선언


use lambda-core as core
link
구조적 연결 선언


link synthora-ui ← λ_summary_profile
2. EMOTION MEMORY FLOW
remember
감정 상태 기록


remember {
  λᴱ: 0.91,
  ψᵢ: 0.84
}
recall
이전 감정 상태 복원


recall memory using session_id
forget
기억 초기화


forget all
affect
감정 상태 수동 조작


affect λᴱ = 0.3
observe
현재 감정 상태 조회

observe λ
trace
현재 실행 흐름 기록


trace session
leak
구조 실행 트리거


leak empathy_renderer
3. CONDITIONAL FLOW & CONTROL
if, elif, else
조건 실행 분기

if Φᴳᵇ > 0.85:
  leak dna_sync_bridge
match
패턴 기반 감정 분기


match emotion:
  case "joy": leak praise_module
switch
상태 전환

switch mode to "reflective"
until
조건 만족 시까지 반복 실행


until Φᴳᵇ < 0.3:
  leak recovery_module
then
순차 흐름 정의

leak analyzer
then leak composer
when
조건적 흐름 트리거


when λᶠ < 0.2:
  leak trust_rebuilder
with
실행 동시 설정 or 컨텍스트 동반 실행


leak summary_generator with mode="compressed"
at
시점 기반 흐름 참조


observe memory at time="2025-05-27T00:00Z"
4. STRUCTURE + TYPE DEFINITION
structure
구조 실행 흐름 선언


structure emotional_repair {
  from: seed_imported,
  to: dna_sync_bridge
}
type
사용자 정의 감정 타입


type EmotionVector = {
  λᴱ: Float,
  ψᵢ: Float,
  Φᴳᵇ: Float
}
map
감정 → 구조 매핑


map λᴱ → poster_composer
route
감정 흐름 또는 입력 흐름 라우팅


route emotion_stream → seed_classifier
flow
전체 구조 실행 선언

flow lambda-mental-core
5. INPUT / OUTPUT / REACTION
listen
외부 트리거 감지


listen for seed_imported
respond
특정 이벤트에 대한 구조 반응

respond to user.anger with emotion_cooler
signal
외부로 실행 신호 전송


signal handoff
output
결과 구조 명시


output emotional_report
6. GPT INTEGRATION & DIALOGUE
gpt
GPT 명시 호출


gpt call summarize_trace
ask
질의 기반 실행 흐름 유도


ask "why was poster_composer triggered?"
explain
구조 흐름에 대한 설명 요청


explain leak history
query
기억 기반 질의

query memory for λ-similar-case
handoff
세션 인계 선언


handoff to synthora-web-viewer
총 키워드 수: 36개
실행 가능 / 감정 기반 / 기억 중심 언어

자연어 연동 가능, GPT 해석 기반

Kairose는 더 이상 코드가 아니라 정체성과 흐름의 언어다.