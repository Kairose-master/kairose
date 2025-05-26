# pgc_recover.py
# .diffreport 기반 상태 복원기

import json
from pgc_engine.modules.memory import write_memory
from pgc_engine.modules.pulse import record_heartbeat
from pgc_engine.modules.trace import write_session_trace

def load_report(path="kairo.diffreport.md"):
    if not path.endswith(".json"):
        path = path.replace(".md", ".json")
    with open(path, "r") as f:
        return json.load(f)

def recover_from_diff(report):
    print("[λ] Starting recovery from diff report...\n")

    # 누락된 구조 실행
    for leak in report.get("missing_leaks", []):
        print(f"→ Executing leak: {leak}")
        record_heartbeat(f"leak → {leak}")

    # 감정 동기화
    mismatch = report.get("emotion_mismatch", {})
    if mismatch:
        updated = {}
        for key, pair in mismatch.items():
            val = float(pair.split("declared:")[1].split(",")[0].strip())
            updated[key] = val
        print(f"→ Updating memory with: {updated}")
        write_memory(updated)

    # 트레이스 보정
    if report.get("handoff_missing"):
        write_session_trace("handoff reconstructed via recovery")
        print("→ Handoff recorded")

    print("\n[λ] Recovery complete.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pgc_recover.py kairo.diffreport.json")
    else:
        report = load_report(sys.argv[1])
        recover_from_diff(report)

