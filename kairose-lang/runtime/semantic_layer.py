# semantic_layer.py
# Kairose 중간 해석 계층 (KML) - 자연어 의미 → 키워드 매핑

from dataclasses import dataclass
from typing import Optional, Dict

# ------------------------------
# IntentBlock 구조 정의
# ------------------------------

@dataclass
class IntentBlock:
    intent: str                # 예: "execute", "remember", "link"
    target: Optional[str]      # 실행 대상 (ex: poster_composer)
    emotion: Optional[Dict]    # λ 파형 (ex: {"λᴱ": 0.91, "ψᵢ": 0.88})
    source_text: str           # 원문 자연어 문장
    origin_eid: Optional[str] = None  # .eid에서 상속된 정체성 기반 실행
    confidence: float = 1.0    # 해석 신뢰도