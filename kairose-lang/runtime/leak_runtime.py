# leak_runtime.py
# Runtime for executing Kairose code — v1.7 ('.kai' compatible, .eid supported)

import json
import os
import re
from copy import deepcopy

from pgc_engine.modules.pulse import record_heartbeat
from pgc_engine.modules.trace import write_session_trace
from pgc_engine.modules.link import write_link_sig
from .semantic_layer import IntentBlock

MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"
LINK_SIG = ".pgc/Link.sig"
PULSE = ".pgc/Pulse.json"
SNAPSHOT_DIR = ".pgc/snapshots"

IDENTITY_CLASSES = {}
return_context = None
method_context = {}

def load_kairose_code(path):
    if not (path.endswith(".kai") or path.endswith(".kairo")):
        raise ValueError("Unsupported file type. Use .kai or .kairo")
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
    write_eid(lambda_vector, trace=[], affect=[])  # NEW: .eid write

def write_eid(lambda_vector, trace=None, affect=None, eid_id="eid_autogen"):
    eid_obj = {
        "id": eid_id,
        "elias": eid_id.title(),
        "core_emotion": lambda_vector,
        "last_trace": trace or [],
        "affect_log": affect or [],
        "current_state": {
            "mode": "boot",
            "resonance": "undefined",
            "role": "undefined"
        },
        "linked_soulbond": None
    }
    os.makedirs("pgc/Memory", exist_ok=True)
    with open(f"pgc/Memory/{eid_id}.eid", "w") as f:
        json.dump(eid_obj, f, indent=2)
    print(f"[λ] .eid written: pgc/Memory/{eid_id}.eid")

def read_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f).get("lambda_vector", {})
    return {}


def execute_intent_block(block: IntentBlock):
    """Execute a basic IntentBlock, updating PGC files accordingly."""

    if block.intent == "remember" and block.emotion:
        write_memory(block.emotion)
        record_heartbeat("remember")
        return

    if block.intent == "execute" and block.target:
        record_heartbeat(f"leak → {block.target}")
        write_session_trace(f"leak → {block.target}")
        return

    if block.intent == "link" and block.target:
        write_link_sig(target=block.target, via="cli")
        record_heartbeat(f"link → {block.target}")
        return

    if block.intent == "trace":
        record_heartbeat("trace session")
        write_session_trace("trace session")
        return

    print(f"[λ] Unknown intent: {block.intent}")

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