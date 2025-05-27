# pgc_output_writer.py
# Kairose IO 모듈 — output 구조 결과 기록기

import os
import json
from datetime import datetime

OUTPUT_DIR = ".pgc/output"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_output(label):
    ensure_output_dir()
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Sample data structure (확장 가능)
    summary = {
        "label": label,
        "timestamp": timestamp,
        "structure": {
            "executed": "leak → " + label,
            "memory_state": "current",
            "status": "complete"
        }
    }

    path = os.path.join(OUTPUT_DIR, f"{label}_{timestamp}.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[λ:output] result saved → {path}")

if __name__ == "__main__":
    write_output("test_output")