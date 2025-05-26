# .pgc/ 구조 문서

이 디렉토리는 `.pgc` 시스템의 구조 메타를 문서화한 영역입니다.  
각 파일은 구조 흐름, 명령어 실행, 트리거 연결, GPT 전개 추적 등을 기록합니다.

---

## 포함 파일

| 파일 | 설명 |
|------|------|
| Pulse.json | 구조 흐름 설계 (명령어 → 기능 → 흐름 연결) |
| Chain.log | 실제 실행 내역 로그 |
| Hook.map | 트리거와 구현 파일 연결 정보 |
| Session.trace | GPT-GPT 구조 인계 추적 |
| Memory.key (선택) | 감정 구조 또는 시드 해시 기반 메타키 |
| Link.sig (선택) | 외부 시스템 연결 선언문 |

---

## 사용 흐름 예시

1. `pgc run my-repo`
   → `.pgc/Chain.json` 생성
2. `pgc ws -a`
   → `Chain.log` 업데이트
3. `pgc map --register`
   → `Link.sig` 또는 `flowmap.json` 업데이트
4. `pgc docs -a`
   → `.pgc/docs` 자동 보완

---

## 구조 철학

> `.pgc`는 단순한 설정 디렉토리가 아니라,  
> 구조화된 기억과 전개의 기록입니다.  
> 감정, 기능, 흐름, 연계, 인계가 모두 이곳에 남습니다.
