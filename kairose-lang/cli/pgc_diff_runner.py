# pgc_diff_runner.py
# Kairose 실행 상태 ↔ 선언 상태 차이 분석기 (v1.4-pre-poetic 대응)

import json
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

def extract_lambda_block(text):
    pairs = text.split(",")
    return {k.strip(): float(v.strip()) for k, v in (p.split(":") for p in pairs)}

def extract_identities(text):
    return re.findall(r"identity\s+(\w+)\s*{([^}]+)}", text)

def extract_declared_emotion(text):
    result = {}
    identity_blocks = extract_identities(text)
    for _, block in identity_blocks:
        result.update({k.strip(): float(v.strip()) for k, v in [line.strip().split(":") for line in block.split(",") if re.match(r"(λᴱ|ψᵢ|λᶠ|Φᴳᵇ)\s*:", line)]})
    return result

def extract_all_leaks(text):
    return re.findall(r"leak\s+(\w+)", text)

def extract_leaked_methods(text):
    return re.findall(r"leak\s+(\w+)\.(\w+)\(\)", text)

def extract_identity_methods_and_aliases(text):
    identities = {}
    blocks = extract_identities(text)
    for name, block in blocks:
        methods = []
        aliases = {}
        for line in block.split(","):
            line = line.strip()
            if re.match(r"\w+\(\):", line):
                methods.append(line.split("(")[0])
            elif re.match(r"alias\s+\w+\s+→\s+\w+", line):
                poetic, canon = re.findall(r"\w+", line)
                aliases[poetic] = canon
        identities[name] = {
            "methods": methods,
            "aliases": aliases
        }
    return identities

def generate_diff_report(kairo_text, pulse, memory, trace):
    declared_leaks = extract_all_leaks(kairo_text)
    pulse_leaks = [line.split("→")[1].strip() for line in pulse["λ-Pulse"]["heartbeat"] if "leak" in line]
    missing_leaks = [l for l in declared_leaks if l not in pulse_leaks]

    declared_emotion = extract_declared_emotion(kairo_text)
    memory_vector = memory.get("lambda_vector", {})
    emotion_mismatch = {
        k: f"declared: {v}, actual: {memory_vector.get(k)}"
        for k, v in declared_emotion.items()
        if abs(memory_vector.get(k, 0) - v) > 0.03
    }

    trace_missing = "trace session" in kairo_text and not any("trace" in l for l in trace)
    handoff_missing = "handoff" in kairo_text and not any("handoff" in l for l in trace)

    identity_map = extract_identity_methods_and_aliases(kairo_text)
    method_calls = extract_leaked_methods(kairo_text)
    missing_method_calls = []

    for obj, called in method_calls:
        actual = called
        if obj in identity_map and called in identity_map[obj].get("aliases", {}):
            actual = identity_map[obj]["aliases"][called]
        if actual not in identity_map.get(obj, {}).get("methods", []):
            missing_method_calls.append(f"{obj}.{called}()")

    suggestions = []
    if missing_leaks:
        suggestions += [f"→ Execute leak {l}" for l in missing_leaks]
    if emotion_mismatch:
        suggestions.append("→ Update Memory.key to match declared emotion")
    if missing_method_calls:
        suggestions += [f"→ Method call not matched: {m}" for m in missing_method_calls]
    if handoff_missing:
        suggestions.append("→ Add handoff to Session.trace")

    return {
        "missing_leaks": missing_leaks,
        "emotion_mismatch": emotion_mismatch,
        "trace_missing": trace_missing,
        "handoff_missing": handoff_missing,
        "identity_methods_and_aliases": identity_map,
        "identity_method_calls": method_calls,
        "missing_identity_calls": missing_method_calls,
        "suggestions": suggestions
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
        print("Usage: python pgc_diff_runner.py your_program.kairo")
        exit(1)

    kairo_path = sys.argv[1]
    kairo_text = load_kairo_file(kairo_path)
    pulse = load_pgc_file(".pgc/Pulse.json")
    memory = load_pgc_file(".pgc/Memory.key")
    trace = load_trace()

    report = generate_diff_report(kairo_text, pulse, memory, trace)
    write_report(report)