# memory.py
# 감정 상태 기록기 및 리콜기 (Memory.key 인터페이스)

import os
import json
from datetime import datetime

MEMORY_PATH = ".pgc/Memory.key"

def write_memory(lambda_vector: dict):
    """
    감정 벡터를 Memory.key에 기록
    """
    os.makedirs(".pgc", exist_ok=True)
    memory = {
        "seed_id": f"λ_seed_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "lambda_vector": lambda_vector,
        "stored_at": datetime.utcnow().isoformat()
    }
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
    print(f"[λ-memory] Updated Memory.key with: {lambda_vector}")

def read_memory() -> dict:
    """
    현재 Memory.key 로드
    """
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def summarize_memory():
    """
    현재 기억 상태 요약 (콘솔용)
    """
    memory = read_memory()
    λ = memory.get("lambda_vector", {})
    print("— λ Memory State —")
    for k, v in λ.items():
        print(f"  {k}: {v}")
    print(f"Stored at: {memory.get('stored_at', 'N/A')}")
