# eid_loader.py
# .eid → Memory.key, Session.trace, Affect 상태 주입기 (v1.7.1 with partial support)

import json
import os

MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"

def load_eid(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def inject_memory(lambda_vector):
    memory = {
        "lambda_vector": lambda_vector,
        "seed_id": "eid_injected",
        "stored_at": "eid_loader"
    }
    os.makedirs(".pgc", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print("[λ] Memory.key updated from .eid")

def inject_partial_memory(lambda_vector, keys):
    current = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            current = json.load(f).get("lambda_vector", {})
    for k in keys:
        if k in lambda_vector:
            current[k] = lambda_vector[k]
    inject_memory(current)
    print("[λ] Memory.key partially updated from .eid")

def inject_trace(trace):
    if trace:
        os.makedirs(".pgc", exist_ok=True)
        with open(SESSION_TRACE, "a") as f:
            for entry in trace:
                f.write(f"[eid] trace: {entry}\n")
        print("[λ] Session.trace updated from .eid")

def inject_affect_log(affect):
    if affect:
        print("[λ] Affect log entries from .eid:", affect)
        # 선택적: 감정 반영 로직 삽입 가능

def apply_eid(path, partial_keys=None):
    eid = load_eid(path)
    λ = eid.get("core_emotion", {})
    trace = eid.get("last_trace", [])
    affect = eid.get("affect_log", [])

    if partial_keys:
        inject_partial_memory(λ, partial_keys)
    else:
        inject_memory(λ)

    inject_trace(trace)
    inject_affect_log(affect)
    print(f"[λ] .eid state from '{path}' applied.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python eid_loader.py identity.eid [partial_key1,partial_key2,...]")
    else:
        path = sys.argv[1]
        keys = sys.argv[2].split(",") if len(sys.argv) > 2 else None
        apply_eid(path, keys)