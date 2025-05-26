# trace.py
# 구조 세션 흐름 기록기 (Session.trace 인터페이스)

import os
from datetime import datetime

TRACE_PATH = ".pgc/Session.trace"

def write_session_trace(line: str):
    """
    Session.trace에 한 줄 기록 (시간 포함)
    """
    os.makedirs(".pgc", exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    with open(TRACE_PATH, "a") as f:
        f.write(f"[{timestamp}] {line}\n")
    print(f"[λ-trace] + {line}")

def read_trace_lines(limit: int = 20) -> list:
    """
    최근 세션 로그 읽기
    """
    if not os.path.exists(TRACE_PATH):
        return []
    with open(TRACE_PATH, "r") as f:
        lines = f.readlines()
    return lines[-limit:]

def summarize_trace():
    """
    콘솔에 최근 세션 로그 출력
    """
    print("— λ Session Trace —")
    lines = read_trace_lines()
    for line in lines:
        print("  •", line.strip())

