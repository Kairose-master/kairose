# leak_runtime.py
# Runtime for executing Kairose code (v1.3-pre identity 확장 대응)

import json
import os
import re
from copy import deepcopy

MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"
LINK_SIG = ".pgc/Link.sig"
PULSE = ".pgc/Pulse.json"
SNAPSHOT_DIR = ".pgc/snapshots"

def load_kairose_code(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_lambda_block(text):
    lines = [line.strip() for line in text.split(",")]
    return {k.strip(): float(v.strip()) for k, v in (line.split(":") for line in lines)}

def write_memory(lambda_vector):
    os.makedirs(".pgc", exist_ok=True)
    memory = {
        "lambda_vector": lambda_vector,
        "seed_id": "kairose_λeak",
        "stored_at": "auto"
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print("[λ] memory updated:", lambda_vector)

def read_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f).get("lambda_vector", {})
    return {}

def execute_leak_target(target):
    print(f"[λ] leaking → {target}")
    os.makedirs(".pgc", exist_ok=True)
    with open(PULSE, "r+") as f:
        pulse = json.load(f)
        pulse["λ-Pulse"]["heartbeat"].append(f"leak → {target}")
        f.seek(0)
        json.dump(pulse, f, indent=2)
        f.truncate()

def trace_session():
    os.makedirs(".pgc", exist_ok=True)
    with open(SESSION_TRACE, "a") as f:
        f.write("[λ] session traced via kairose\n")

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
    print(f"[λ] linked: {to} ← {via}")

def handle_identity_blocks(code):
    identities = re.findall(r"identity\s+(\w+)\s*{([^}]+)}", code)
    for name, body in identities:
        vec = parse_lambda_block(body)
        print(f"[λ] identity defined: {name} → {vec}")
        write_memory(vec)  # overwrite as current

    spawns = re.findall(r"spawn\s+(\w+)\s+from\s+(\w+)", code)
    for new, src in spawns:
        mem = read_memory()
        cloned = deepcopy(mem)
        print(f"[λ] spawned {new} from {src}")
        write_memory(cloned)

    merges = re.findall(r"merge\s+(\w+)\s+with\s+(\w+)", code)
    for a, b in merges:
        mem = read_memory()
        merged = {k: (v + mem.get(k, 0)) / 2 for k, v in mem.items()}
        print(f"[λ] merged {a} with {b}")
        write_memory(merged)

    recovers = re.findall(r"recover\s+(\w+)", code)
    for snap in recovers:
        path = os.path.join(SNAPSHOT_DIR, f"{snap}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                restored = json.load(f)
                print(f"[λ] recovered from {snap}")
                write_memory(restored.get("lambda_vector", {}))
        else:
            print(f"[λ] recovery failed: snapshot {snap} not found")

def run_kairose(path):
    code = load_kairose_code(path)

    if "remember" in code:
        block = re.search(r"remember\s*{([^}]+)}", code)
        if block:
            write_memory(parse_lambda_block(block.group(1)))

    handle_identity_blocks(code)

    for target in re.findall(r"leak\s+(\w+)", code):
        execute_leak_target(target)

    if "trace session" in code:
        trace_session()

    for to, via in re.findall(r"link\s+(\w+)\s+←\s+(\w+)", code):
        link_system(to, via)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python leak_runtime.py your_program.kairo")
    else:
        run_kairose(sys.argv[1])