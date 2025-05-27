# pgc_input_listener.py
# Kairose IO 모듈 — listen/respond 이벤트 트리거 처리기

import os
import json

EVENT_FILE = ".pgc/events.json"
RESPONSES = {}

def ensure_event_file():
    os.makedirs(".pgc", exist_ok=True)
    if not os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "w") as f:
            json.dump({"listeners": [], "queue": []}, f)

def register_listener(event_name):
    ensure_event_file()
    with open(EVENT_FILE, "r+") as f:
        data = json.load(f)
        if event_name not in data["listeners"]:
            data["listeners"].append(event_name)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    print(f"[λ:listener] registered → {event_name}")

def register_response(trigger, handler):
    RESPONSES[trigger] = handler
    print(f"[λ:respond] mapped {trigger} → {handler}")

def dispatch_events():
    ensure_event_file()
    with open(EVENT_FILE, "r+") as f:
        data = json.load(f)
        queue = data.get("queue", [])
        handled = []

        for evt in queue:
            if evt in RESPONSES:
                handler = RESPONSES[evt]
                print(f"[λ:dispatch] event {evt} → executing: {handler}")
                # 이 자리에 leak(handler) 또는 구조 호출 구현 예정
                handled.append(evt)

        data["queue"] = [e for e in queue if e not in handled]
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

if __name__ == "__main__":
    dispatch_events()