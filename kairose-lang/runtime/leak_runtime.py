# leak_runtime.py
# Runtime for executing Kairose code (v1.2.1 — λeak engine 확장)

import json
import os
import re

MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"
LINK_SIG = ".pgc/Link.sig"
PULSE = ".pgc/Pulse.json"

def load_kairose_code(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_remember_block(code):
    match = re.search(r"remember\s*{([^}]+)}", code)
    if match:
        content = match.group(1)
        lines = [line.strip() for line in content.split(",")]
        return {k.strip(): float(v.strip()) for k, v in (line.split(":") for line in lines)}
    return {}

def write_memory(lambda_vector):
    memory = {
        "seed_id": "kairose_λeak_001",
        "lambda_vector": lambda_vector,
        "stored_at": "auto"
    }
    os.makedirs(".pgc", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print("[λeak] remembered:", lambda_vector)

def execute_leak_target(target):
    print(f"[λeak] leaking structure: {target}")
    with open(PULSE, "r+") as f:
        pulse = json.load(f)
        pulse["λ-Pulse"]["heartbeat"].append(f"leak → {target}")
        f.seek(0)
        json.dump(pulse, f, indent=2)
        f.truncate()

def trace_session():
    os.makedirs(".pgc", exist_ok=True)
    with open(SESSION_TRACE, "a") as f:
        f.write("[λeak] session traced via kairose\n")

def link_system(to, via):
    os.makedirs(".pgc", exist_ok=True)
    sig = {
        "λ-Link-Signature": {
            "this_repo": "kairose-runtime",
            "outputs": [via],
            "links_to": [to],
            "registered_at": "auto"
        }
    }
    with open(LINK_SIG, "w") as f:
        json.dump(sig, f, indent=2)
    print(f"[λeak] linked: {to} ← {via}")

def extract_all_leak_targets(code):
    # 모든 leak 키워드를 추출 (블록 내 포함)
    return re.findall(r"leak\s+(\w+)", code)

def run_kairose(path):
    code = load_kairose_code(path)

    # Memory
    if "remember" in code:
        λ = parse_remember_block(code)
        write_memory(λ)

    # Leak 전체 추출
    for target in extract_all_leak_targets(code):
        execute_leak_target(target)

    # Trace
    if "trace session" in code:
        trace_session()

    # Link
    link_matches = re.findall(r"link\s+(\w+)\s+←\s+(\w+)", code)
    for to, via in link_matches:
        link_system(to, via)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python leak_runtime.py your_program.kairo")
    else:
        run_kairose(sys.argv[1])