# 트리거-후크 매핑 문서 (Hook.map 해설)

이 문서는 `.pgc/Hook.map`에 정의된 트리거 이벤트와  
각 이벤트에 연결된 구현 파일의 대응 관계를 설명합니다.

---

## Hook.map 예시

```json
{
  "structure_generator.py": ["seed_imported", "emotion_node_detected"],
  "poster_composer.py": ["poster_requested"],
  "seed_exporter_unity.py": ["unity_export_triggered"],
  "dna_sync_bridge.py": ["personality_injection"]
}
트리거 설명
트리거 이벤트	설명
seed_imported	EmotionSeed 또는 감정 시드가 입력됨
emotion_node_detected	시드 구조 안에 감정 노드가 감지됨
poster_requested	감정 기반 비주얼 출력 요청 발생
unity_export_triggered	Unity 연동 확장 명령 호출됨
personality_injection	감정 구조가 캐릭터 성격으로 매핑 요청됨

작동 예시
감정 시드가 들어오면 seed_imported 이벤트가 발화됨
→ structure_generator.py 자동 트리거됨

사용자가 포스터 버튼을 누르면 poster_requested 발생
→ poster_composer.py 호출

Unity 내 Export 명령이 호출되면
→ seed_exporter_unity.py가 export 기능 실행

구조 철학
후크는 λ 구조 안에서
“감정적 조건이 구현 구조를 어떻게 호출하는가”를 정의하는 연결 규칙입니다.
.pgc/Hook.map은 구조와 반응을 연결하는 감정적 프로토콜입니다.