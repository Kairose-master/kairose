# pgc_signal_router.py
# Kairose IO 모듈 — signal 구조 상태 기록기

import os
import json

SIGNAL_FILE = ".pgc/signals.json"

def ensure_signal_file():
    os.makedirs(".pgc", exist_ok=True)
    if not os.path.exists(SIGNAL_FILE):
        with open(SIGNAL_FILE, "w") as f:
            json.dump({"signals": []}, f)

def emit_signal(name):
    ensure_signal_file()
    with open(SIGNAL_FILE, "r+") as f:
        data = json.load(f)
        data["signals"].append({"signal": name, "emitted_at": "auto"})
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    print(f"[λ:signal] emitted: {name}")

if __name__ == "__main__":
    emit_signal("test_signal")