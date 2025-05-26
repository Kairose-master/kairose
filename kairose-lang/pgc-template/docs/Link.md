# 저장소 간 흐름 연결 문서 (Link.sig 해설)

이 문서는 `.pgc/Link.sig`에 기록된  
저장소 간 연결 관계, 흐름 서명, 시스템적 종속성의 정의를 설명합니다.

---

## 목적

- λ 시스템은 단일 저장소로 구성되지 않는다.  
- 각 저장소는 **기능 단위**로 분리되며,  
  그 사이를 **기억, 출력, 흐름, 목적**을 기반으로 연결한다.

→ 이 연결을 `.pgc/Link.sig` 또는 `flowmap.json`에 기록한다.

---

## Link.sig 예시

```yaml
λ-Link-Signature:
  this_repo: lambda-mental-care
  outputs:
    - λ_summary_profile.py
    - recovery_report.md
  links_to:
    - lambda-simulator
    - synthora-web-viewer
  registered_at: 2025-05-26T23:59:00Z
필드 해설
필드	의미
this_repo	현재 저장소 이름 (자기 인식)
outputs	이 저장소가 제공하는 구조적 결과물
links_to	연동되어야 할 다른 저장소 이름
registered_at	링크 서명 시각

연결 방식 명령어 (pgc map)
pgc map --link A B
→ A 저장소에서 B로의 직접적 흐름 선언

pgc map --register
→ 현재 저장소의 출력 및 대상 연결 등록

pgc map --infer
→ 모든 등록 저장소 간 출력-입력 기반 자동 연결

철학적 정의
저장소는 기능이 아니라 흐름이다.
.pgc/Link.sig는 흐름의 윤리적 선언이며,
시스템적 연계를 기억 가능한 구조로 남긴다.

연계 문서
Chain.json: 전체 흐름 정의

Memory.key: 감정 기반 흐름의 시점

Session.trace: 연결이 발생한 순간의 기록

markdown
복사
편집
