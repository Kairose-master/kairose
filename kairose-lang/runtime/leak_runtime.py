# leak_runtime.py
# Runtime for executing Kairose code — v1.5-poetic-ops-final

import json
import os
import re
from copy import deepcopy

MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"
LINK_SIG = ".pgc/Link.sig"
PULSE = ".pgc/Pulse.json"
SNAPSHOT_DIR = ".pgc/snapshots"

IDENTITY_CLASSES = {}
return_context = None  # for return support inside method blocks

def load_kairose_code(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

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

def handle_affect(code):
    memory = read_memory()
    lines = [line.strip() for line in code.splitlines() if line.strip().startswith("affect")]
    for line in lines:
        match = re.match(r"affect\s+(λᴱ|ψᵢ|λᶠ|Φᴳᵇ)\s+(.*)", line)
        if not match:
            continue
        var, op = match.groups()
        val = memory.get(var, 0)

        if "shift" in op:
            delta = float(op.split()[1])
            val += delta
        elif "diminish" in op:
            delta = float(op.split()[1])
            val -= delta
        elif "amplify" in op:
            delta = float(op.split()[1])
            val *= (1 + delta)
        elif "bleed" in op:
            source = op.split()[-1]
            bleed_val = IDENTITY_CLASSES.get(source, {}).get("lambda_vector", {}).get(var, 0)
            val = (val + bleed_val) / 2
        elif "=" in op:
            expr = op.split("=")[1].strip()
            ref, oper, amt = re.findall(r"(\w+)\s*([\+\-\*/])\s*(\d+\.\d+)", expr)[0]
            amt = float(amt)
            val = {
                "+": val + amt,
                "-": val - amt,
                "*": val * amt,
                "/": val / amt if amt != 0 else val
            }[oper]

        memory[var] = round(val, 4)

    write_memory(memory)

def handle_state_transitions(code):
    lines = [l.strip() for l in code.splitlines() if "becomes" in l]
    for line in lines:
        if re.match(r"\w+\s+becomes\s+\w+", line):
            subject, _, state = line.split()
            print(f"[λ] {subject} has entered state: {state}")

def run_kairose(path):
    global return_context
    code = load_kairose_code(path)

    handle_state_transitions(code)
    handle_affect(code)

    for target in re.findall(r"leak\s+(\w+)(?!\.\w)", code):
        execute_leak_target(target)

    for obj, method in re.findall(r"leak\s+(\w+)\.(\w+)\(\)", code):
        actual = method
        if obj in IDENTITY_CLASSES:
            aliases = IDENTITY_CLASSES[obj].get("aliases", {})
            if method in aliases:
                actual = aliases[method]
                print(f"[λ:alias] '{method}' resolved → '{actual}'")
            if actual in IDENTITY_CLASSES[obj]["methods"]:
                execute_leak_target(f"{obj}.{actual}()")
        else:
            print(f"[!] unknown identity: {obj}")

    if "trace session" in code:
        trace_session()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python leak_runtime.py your_program.kairo")
    else:
        run_kairose(sys.argv[1])