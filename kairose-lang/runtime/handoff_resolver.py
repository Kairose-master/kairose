# handoff_resolver.py
# Executes `handoff_partial` blocks by selectively syncing memory and trace

import json
import os

MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"
PULSE_FILE = ".pgc/Pulse.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f).get("lambda_vector", {})
    return {}

def write_memory(vector):
    memory = {
        "lambda_vector": vector,
        "seed_id": "handoff_partial",
        "stored_at": "handoff_resolver"
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def append_trace(entry):
    with open(SESSION_TRACE, "a") as f:
        f.write(f"[handoff_partial] trace: {entry}\n")

def process_handoff_partial(block):
    print(f"[λ] Executing handoff_partial: {block['from']} → {block['to']}")

    current_memory = load_memory()
    new_memory = {}

    for item in block["transfer"]:
        if item in current_memory:
            new_memory[item] = current_memory[item]
        elif item.startswith("trace:"):
            label = item.split(":")[1]
            append_trace(label)
        elif item.startswith("affect:"):
            print(f"[λ] Affect transferred: {item}")  # Optional external affect resolver

    if new_memory:
        write_memory(new_memory)
        print("[λ] Partial memory transferred:", new_memory)

    if block.get("signal"):
        print(f"[λ] Signal emitted: {block['signal']}")

    if block.get("link"):
        to = block["link"]["to"]
        frm = block["link"]["from"]
        print(f"[λ] Link created: {to} ← {frm}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python handoff_resolver.py handoff_block.json")
    else:
        with open(sys.argv[1], "r") as f:
            block = json.load(f)
        process_handoff_partial(block)