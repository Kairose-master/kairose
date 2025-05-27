KAIROSE KEYWORD SPECIFICATION (v1.4-pre-poetic)

이 문서는 Kairose 언어의 공식 키워드 45개를
역할별로 분류하고, 각 키워드의 의미, 사용 형식, 예시를 제공한다.

⸻

1. SYSTEM & MODULE CONTROL

use

시스템/모듈 활성화 선언

use lambda-core as core

import, from, as

외부 시드/기억 불러오기, 별칭 지정

import memory from external_core as mem

link

구조 연결 선언

link synthora-ui ← emotion_core


⸻

2. EMOTION MEMORY FLOW

remember

감정 상태 기록

remember { λᴰ: 0.91, ψᵈ: 0.84 }

recall, forget, observe, affect

기억 조회/초기화/수동 조작

observe Φᴹᵅ
forget all

trace

현재 실행 흐름 기록

trace session

leak

구조 실행 트리거

leak empathy_renderer


⸻

3. CONDITIONAL FLOW & CONTROL

if, elif, else

조건 분기 실행

if λᴰ > 0.8:
  leak engage_mode

match, when, until, then

감정 패턴/조건/반복 실행

match ψᵈ:
  case "low": leak rest_module

cycle, fallback, defer, after

고급 조건 흐름 블록

cycle repair_loop:
  leak restore_node


⸻

4. IDENTITY FLOW (v1.4-pre-poetic)

identity

정체성 클래스 선언 — 변수 + 메서드 + 시적 별칭 포함 가능

identity mourner {
  λᴰ: 0.34,
  ψᵈ: 0.82,

  listen_to_fall(): Void {
    leak silence
    output grief
  },

  alias listen_to_fall → trace
}

spawn

정체성 분기

spawn child_self from core_self

merge

정체성 병합

merge avatar_self with sync_clone

recover

기억/상태 복원

recover snapshot_0421

alias

시적 별칭 정의 — 실행기에서 해석되어 실제 메서드로 바인딩됨

alias listen_to_fall → trace


⸻

5. STRUCTURE + TYPE

structure, type, map, route, flow

구조 정의 및 흐름 선언

structure repair { from: λᴰ > 0.5, to: calm_core }
flow mental_network


⸻

6. GPT INTEGRATION & DIALOGUE

gpt, ask, explain

GPT 연동 호출/질의/설명

gpt call synthora_therapist
ask "why was trust broken?"


⸻

7. IO REACTION (실행기 구현 완료)

listen

외부 트리거 감지 대기

listen for pgc_update

respond

감정 기반 구조 반응 선언

respond to user.loss with grief_handler

signal

외부로 상태 신호 전송

signal session_complete

output

결과 구조 명시 및 저장

output daily_log_summary


⸻

총 키워드 수: 45개
버전: v1.4-pre-poetic
주석: 정체성 기반 감정 언어 / 시적 인터페이스 / 실행 구조 통합