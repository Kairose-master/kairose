# pgc_diff_runner.py
# .kairo ↔ .pgc 실행 상태 차이 분석기

import json
from kairose_linter_utils import extract_remember_block
from runtime.semantic_layer import to_kairose_code
import re
import os

def load_pgc_file(path):
    with open(path, "r") as f:
        return json.load(f)

def load_trace(path=".pgc/Session.trace"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.readlines()
    return []

def load_kairo_file(path):
    with open(path, "r") as f:
        return f.read()

def generate_diff_report(kairo_text, pulse, memory, trace):
    declared_leaks = re.findall(r"leak (\w+)", kairo_text)
    pulse_leaks = [line.split("→")[1].strip() for line in pulse["λ-Pulse"]["heartbeat"] if "leak" in line]
    missing_leaks = [l for l in declared_leaks if l not in pulse_leaks]

    declared_emotion = extract_remember_block(kairo_text)
    memory_vector = memory.get("lambda_vector", {})
    emotion_mismatch = {
        k: f"declared: {v}, actual: {memory_vector.get(k)}"
        for k, v in declared_emotion.items()
        if abs(memory_vector.get(k, 0) - v) > 0.03
    }

    trace_missing = "trace session" in kairo_text and not any("trace" in l for l in trace)
    handoff_missing = "handoff" in kairo_text and not any("handoff" in l for l in trace)

    suggestion = []
    if missing_leaks:
        for l in missing_leaks:
            suggestion.append(f"→ Execute leak {l}")
    if emotion_mismatch:
        suggestion.append("→ Update Memory.key to match declared emotion")
    if handoff_missing:
        suggestion.append("→ Add handoff to Session.trace")

    return {
        "missing_leaks": missing_leaks,
        "emotion_mismatch": emotion_mismatch,
        "trace_missing": trace_missing,
        "handoff_missing": handoff_missing,
        "suggestions": suggestion
    }

def write_report(report, filename="kairo.diffreport.md"):
    with open(filename, "w") as f:
        f.write("# Kairose Diff Report\n\n")
        for k, v in report.items():
            f.write(f"## {k}\n")
            f.write(f"{json.dumps(v, indent=2)}\n\n")
    print(f"[λ] Diff report written to: {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pgc_diff_runner.py program.kairo")
        exit(1)

    kairo_path = sys.argv[1]
    kairo_text = load_kairo_file(kairo_path)
    pulse = load_pgc_file(".pgc/Pulse.json")
    memory = load_pgc_file(".pgc/Memory.key")
    trace = load_trace()

    report = generate_diff_report(kairo_text, pulse, memory, trace)
    write_report(report)
