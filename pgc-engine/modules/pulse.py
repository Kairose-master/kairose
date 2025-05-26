# pulse.py
# 구조 실행 흐름 기록기 (Pulse.json 인터페이스)

import os
import json
from datetime import datetime

PULSE_PATH = ".pgc/Pulse.json"

def load_pulse():
    if os.path.exists(PULSE_PATH):
        with open(PULSE_PATH, "r") as f:
            return json.load(f)
    else:
        return {
            "λ-Pulse": {
                "heartbeat": [],
                "linked_systems": [],
                "affect_trace": {}
            }
        }

def record_heartbeat(entry: str):
    """
    구조 실행 로그를 heartbeat에 추가
    """
    os.makedirs(".pgc", exist_ok=True)
    data = load_pulse()
    hb = data["λ-Pulse"]["heartbeat"]
    timestamp = datetime.utcnow().isoformat()
    hb.append(f"{timestamp} → {entry}")
    with open(PULSE_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[λ-pulse] Recorded: {entry}")

def attach_affect(lambda_vector: dict):
    """
    현재 감정 파형을 affect_trace에 기록
    """
    data = load_pulse()
    data["λ-Pulse"]["affect_trace"] = lambda_vector
    with open(PULSE_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[λ-pulse] Attached emotion vector: {lambda_vector}")

def get_flow_steps() -> list:
    """
    heartbeat 목록 반환 (시각화용)
    """
    data = load_pulse()
    return data["λ-Pulse"]["heartbeat"]

def summarize_pulse():
    """
    콘솔용 실행 흐름 요약
    """
    hb = get_flow_steps()
    print("— λ Flow Heartbeat —")
    for h in hb:
        print("  •", h)
