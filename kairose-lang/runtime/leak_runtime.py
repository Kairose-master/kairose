# leak_runtime.py
# Runtime for executing Kairose code — v1.3-class identity method support

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

def load_kairose_code(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_lambda_block(text):
    lines = [line.strip() for line in text.split(",") if ":" in line]
    return {k.strip(): float(v.strip()) for k, v in (line.split(":") for line in lines if "(" not in k)}

def parse_identity_block(name, block):
    lines = [line.strip() for line in block.split(",")]
    λ = {}
    variables = {}
    methods = []

    for line in lines:
        if re.match(r"(λᴱ|ψᵢ|λᶠ|Φᴳᵇ)\s*:", line):
            k, v = [s.strip() for s in line.split(":")]
            λ[k] = float(v)
        elif re.match(r"^\w+\(\):", line):  # method
            fn, type_ = [s.strip() for s in line.split(":")]
            methods.append(fn.split("(")[0])
        elif ":" in line:
            var, type_ = [s.strip() for s in line.split(":")]
            variables[var] = type_
    
    IDENTITY_CLASSES[name] = {
        "lambda_vector": λ,
        "variables": variables,
        "methods": methods
    }

    print(f"[λ:identity] class '{name}' defined → λ={λ}, vars={variables}, methods={methods}")
    write_memory(λ)  # Set last defined identity as active context

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
    blocks = re.findall(r"identity\s+(\w+)\s*{([^}]+)}", code)
    for name, block in blocks:
        parse_identity_block(name, block)

    spawns = re.findall(r"spawn\s+(\w+)\s+from\s+(\w+)", code)
    for new, src in spawns:
        if src in IDENTITY_CLASSES:
            cloned = deepcopy(IDENTITY_CLASSES[src])
            IDENTITY_CLASSES[new] = cloned
            print(f"[λ] spawned identity: {new} from {src}")
            write_memory(cloned.get("lambda_vector", {}))

    merges = re.findall(r"merge\s+(\w+)\s+with\s+(\w+)", code)
    for a, b in merges:
        if a in IDENTITY_CLASSES and b in IDENTITY_CLASSES:
            merged = deepcopy(IDENTITY_CLASSES[a])
            for k in IDENTITY_CLASSES[b]["lambda_vector"]:
                if k in merged["lambda_vector"]:
                    merged["lambda_vector"][k] = (
                        merged["lambda_vector"][k] + IDENTITY_CLASSES[b]["lambda_vector"][k]) / 2
            IDENTITY_CLASSES[a] = merged
            print(f"[λ] merged identity: {a} with {b}")
            write_memory(merged["lambda_vector"])

    recovers = re.findall(r"recover\s+(\w+)", code)
    for snap in recovers:
        path = os.path.join(SNAPSHOT_DIR, f"{snap}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                restored = json.load(f)
                print(f"[λ] recovered from snapshot: {snap}")
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

    for obj, method in re.findall(r"leak\s+(\w+)\.(\w+)\(\)", code):
        if obj in IDENTITY_CLASSES and method in IDENTITY_CLASSES[obj]["methods"]:
            print(f"[λ] leak {obj}.{method}() → identity method invoked")
            execute_leak_target(f"{obj}.{method}()")
        else:
            print(f"[!] unknown method: {obj}.{method}()")

    if "trace session" in code:
        trace_session()

    for to, via in re.findall(r"link\s+(\w+)\s+←\s+(\w+)", code):
        link_system(to, via)

    # IO blocks remain unchanged here for brevity (listen/respond/signal/output)
    # Already patched earlier

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python leak_runtime.py your_program.kairo")
    else:
        run_kairose(sys.argv[1])
# ... 생략된 상단 동일 ...

IDENTITY_CLASSES = {}  # { name: { lambda_vector, variables, methods, aliases } }

def parse_identity_block(name, block):
    lines = [line.strip() for line in block.split(",")]
    λ = {}
    variables = {}
    methods = {}
    aliases = {}

    for line in lines:
        if re.match(r"(λᴱ|ψᵢ|λᶠ|Φᴳᵇ)\s*:", line):
            k, v = [s.strip() for s in line.split(":")]
            λ[k] = float(v)
        elif re.match(r"^\w+\(\):", line):  # method
            fn, type_ = [s.strip() for s in line.split(":")]
            method_name = fn.split("(")[0]
            methods[method_name] = {"type": type_, "body": []}  # body not handled yet
        elif re.match(r"alias\s+\w+\s+→\s+\w+", line):
            poetic, canon = re.findall(r"\w+", line)
            aliases[poetic] = canon
        elif ":" in line:
            var, type_ = [s.strip() for s in line.split(":")]
            variables[var] = type_

    IDENTITY_CLASSES[name] = {
        "lambda_vector": λ,
        "variables": variables,
        "methods": methods,
        "aliases": aliases
    }

    print(f"[λ:identity] class '{name}' defined")
    write_memory(λ)

def run_kairose(path):
    code = load_kairose_code(path)

    if "remember" in code:
        block = re.search(r"remember\s*{([^}]+)}", code)
        if block:
            write_memory(parse_lambda_block(block.group(1)))

    handle_identity_blocks(code)

    # basic leak
    for target in re.findall(r"leak\s+(\w+)(?!\.\w)", code):
        execute_leak_target(target)

    # object.method leaks + alias resolution
    for obj, method in re.findall(r"leak\s+(\w+)\.(\w+)\(\)", code):
        actual = method
        if obj in IDENTITY_CLASSES:
            aliases = IDENTITY_CLASSES[obj].get("aliases", {})
            if method in aliases:
                actual = aliases[method]
                print(f"[λ:alias] poetic method '{method}' resolved → '{actual}'")

            if actual in IDENTITY_CLASSES[obj]["methods"]:
                execute_leak_target(f"{obj}.{actual}()")
            else:
                print(f"[!] method not found: {obj}.{method}()")
        else:
            print(f"[!] unknown identity: {obj}")

    # ... rest identical ...

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python leak_runtime.py your_program.kairo")
    else:
        run_kairose(sys.argv[1])