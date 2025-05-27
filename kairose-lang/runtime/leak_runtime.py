# leak_runtime.py
# Kairose v1.6 FULL — identity, affect, method(args), return, flow, literals, IO

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
return_context = None
method_context = {}


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


def execute_leak_target(target, args=None):
    print(f"[λ] leaking → {target}", f"args={args}" if args else "")
    os.makedirs(".pgc", exist_ok=True)
    with open(PULSE, "r+") as f:
        pulse = json.load(f)
        pulse["λ-Pulse"]["heartbeat"].append(f"leak → {target}" + (f"({args})" if args else ""))
        f.seek(0)
        json.dump(pulse, f, indent=2)
        f.truncate()


def parse_string_literal(arg):
    match = re.match(r'"(.*?)"', arg.strip())
    return match.group(1) if match else arg.strip()


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


def handle_return_statements(code):
    global return_context
    match = re.search(r"\breturn\s+([\w\"\.]+)", code)
    if match:
        value = parse_string_literal(match.group(1))
        return_context = value
        print(f"[λ:return] → {value}")


def handle_session_blocks(code):
    for session in re.findall(r"session\s+(\w+):", code):
        print(f"[λ:session] → {session}")
        execute_leak_target(f"session → {session}")
    for step in re.findall(r"step\s+(\d+):", code):
        print(f"[λ:step] → {step}")
        execute_leak_target(f"step → {step}")


def handle_state_transitions(code):
    for line in [l.strip() for l in code.splitlines() if "becomes" in l]:
        if re.match(r"\w+\s+becomes\s+\w+", line):
            subject, _, state = line.split()
            execute_leak_target(f"{subject}.becomes.{state}")


def run_kairose(path):
    global return_context, method_context
    code = load_kairose_code(path)

    return_context = None
    method_context = {}

    handle_session_blocks(code)
    handle_state_transitions(code)
    handle_affect(code)
    handle_return_statements(code)

    # method(arg) calls
    for obj, method, args in re.findall(r"leak\s+(\w+)\.(\w+)\(([^)]*)\)", code):
        arg_list = [parse_string_literal(a) for a in args.split(",")] if args else []
        method_context = {"args": arg_list}
        execute_leak_target(f"{obj}.{method}()", arg_list)

    for target in re.findall(r"leak\s+(\w+)(?![\.\(])", code):
        execute_leak_target(target)

    if return_context:
        print(f"[λ] return value: {return_context}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python leak_runtime.py file.kairo")
    else:
        run_kairose(sys.argv[1])
```