# eid_builder.py
# .kai/.kairo 실행 결과 → Elias Identity Data (.eid) 생성기

import json
import os
import sys

PULSE_FILE = ".pgc/Pulse.json"
MEMORY_FILE = ".pgc/Memory.key"
SESSION_TRACE = ".pgc/Session.trace"


def read_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f).get("lambda_vector", {})

def read_trace():
    if not os.path.exists(SESSION_TRACE):
        return []
    with open(SESSION_TRACE, "r") as f:
        return [line.strip() for line in f.readlines() if "trace" in line]

def read_pulse_affect():
    if not os.path.exists(PULSE_FILE):
        return []
    with open(PULSE_FILE, "r") as f:
        pulse = json.load(f)
        return [entry for entry in pulse.get("λ-Pulse", {}).get("heartbeat", []) if "affect" in entry]

def build_eid(identity_id="from_kai"):
    λ = read_memory()
    trace = read_trace()
    affect = read_pulse_affect()

    eid_obj = {
        "id": identity_id,
        "elias": identity_id.title(),
        "core_emotion": λ,
        "last_trace": trace,
        "affect_log": affect,
        "current_state": {
            "mode": "post-exec",
            "resonance": "derived",
            "role": "actor"
        },
        "linked_soulbond": None
    }

    os.makedirs("pgc/Memory", exist_ok=True)
    with open(f"pgc/Memory/{identity_id}.eid", "w") as f:
        json.dump(eid_obj, f, indent=2)
    print(f"[λ] .eid built → pgc/Memory/{identity_id}.eid")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eid_builder.py identity_id")
    else:
        build_eid(sys.argv[1])