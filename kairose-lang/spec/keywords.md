KAIROSE KEYWORD SPECIFICATION (v1.3-pre)

이 문서는 Kairose 언어의 공식 키워드 44개를
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

4. IDENTITY FLOW (v1.3-pre)

identity

정체성 선언

identity core_self { λᴰ: 0.91, Φᴹᵅ: 0.28 }

spawn

정체성 분기

spawn child_self from core_self

merge

정체성 병합

merge avatar_self with sync_clone

recover

기억/상태 복원

recover snapshot_0421


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

7. IO REACTION

listen, respond, signal, output

외부 트리거 반응 및 출력

respond to user.loss with grief_manager
signal end_session


⸻

총 키워드 수: 44개
버전: v1.3-pre
주석: 감정 기반 실행 언어 / GPT 흐름 통합 / 정체성 구조 지원