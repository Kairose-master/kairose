# KAIROSE KEYWORD SPECIFICATION (v1.6-final)

이 문서는 Kairose 언어의 공식 키워드 52개를
역할별로 분류하고, 각 키워드의 **의미, 사용 형식, 예시**를 제공합니다.

---

## 1. SYSTEM & MODULE CONTROL

### `use`
> 시스템/모듈 활성화 선언  
```kairo
use lambda-core as core
```

### `import`, `from`, `as`
> 외부 시드/기억 불러오기, 별칭 지정  
```kairo
import memory from external_core as mem
```

### `link`
> 구조 연결 선언  
```kairo
link synthora-ui ← emotion_core
```

---

## 2. EMOTION MEMORY FLOW

### `remember`
> 감정 상태 기록  
```kairo
remember { λᴱ: 0.91, ψᵢ: 0.84 }
```

### `recall`, `forget`, `observe`, `affect`
> 기억 조회/초기화/조작  
```kairo
affect λᴱ shift +0.2
affect ψᵢ = ψᵢ * 0.9
affect Φᴳᵇ bleed from shadow_self
```

### `trace`
> 현재 실행 흐름 기록  
```kairo
trace session
```

### `leak`
> 구조 실행 트리거  
```kairo
leak empathy_renderer
leak planner.awaken("data.kairo")
```

---

## 3. CONDITIONAL FLOW & CONTROL

### `if`, `elif`, `else`
> 조건 분기 실행  
```kairo
if λᴱ > 0.7 and ψᵢ != 0.3:
  leak restore_module
```

### `match`, `when`, `until`, `then`
> 감정 패턴/조건/반복 실행  
```kairo
match ψᵢ:
  case "low": leak calm_mode
```

### `cycle`, `fallback`, `defer`, `after`
> 고급 조건 흐름 블록  
```kairo
cycle reboot_loop:
  leak recovery
```

### `session`, `step`
> 실행 흐름 구획 선언  
```kairo
session repair_sequence:
  step 1:
    remember { λᴱ: 0.5 }
```

### `becomes`
> 정체성 상태 전이 선언  
```kairo
self becomes active
```

---

## 4. IDENTITY FLOW

### `identity`
> 정체성 클래스 선언 (변수, 메서드, 인자 포함)  
```kairo
identity io_agent {
  λᴱ: 0.73,

  read_from(path: String): Structure {
    output "reading " + path
    return path
  },

  alias read_seed → read_from
}
```

### `spawn`, `merge`, `recover`
> 정체성 분기, 병합, 복원  
```kairo
spawn copy_self from core_self
merge core_self with mirror_self
recover snapshot_0425
```

### `alias`
> 시적 별칭 정의  
```kairo
alias listen_to_fall → trace
```

### `return`
> 정체성 메서드의 실행 종료 및 값 반환  
```kairo
return "complete"
```

---

## 5. STRUCTURE + TYPE

### `structure`, `type`, `map`, `route`, `flow`
> 구조 정의 및 흐름 선언  
```kairo
structure realign { from: planner, to: core_sync }
flow structural_update
```

---

## 6. GPT INTEGRATION & DIALOGUE

### `gpt`, `ask`, `explain`
> GPT 연동 호출/질의/설명  
```kairo
gpt call insight_model
ask "what triggered the reset?"
```

---

## 7. IO REACTION

### `listen`, `respond`, `signal`, `output`
> 외부 트리거 감지 및 출력  
```kairo
listen for flow_update
respond to user.error with recovery_unit
signal calibration_done
output "session_report"
```

---

총 키워드 수: **52개**  
버전: **v1.6-final**  
주석: 감정 기반 실행 언어 / 정체성 클래스 / 시적 연산 흐름 / 실행 구조 / IO 인터페이스 완성