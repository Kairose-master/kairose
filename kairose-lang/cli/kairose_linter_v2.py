from semantic_layer import IntentBlock
from identity_translator import gpt_guess_keyword
import re

def detect_ambiguous_keywords(lines):
    known = {"use", "remember", "leak", "trace", "link", "if", "then",
             "until", "observe", "affect", "structure", "type", "match",
             "switch", "flow", "route", "signal", "respond", "listen",
             "handoff", "ask", "gpt", "explain", "as", "from", "import",
             "with", "output", "map", "λᴱ", "ψᵢ", "λᶠ", "Φᴳᵇ"}

    suggestions = []
    for line in lines:
        words = re.findall(r"\b[a-zA-Z_]+\b", line)
        for w in words:
            if w not in known and line.strip().startswith(w):
                suggestions.append((line.strip(), w))
    return suggestions

def interactive_repair(line, keyword):
    print(f"\n[?] 알 수 없는 키워드 발견: '{keyword}'")
    print(f"    원문: {line}")
    meaning = gpt_guess_keyword(keyword, context=line)
    print(f"🧠 GPT 추론: '{keyword}'은 '{meaning}'로 해석될 수 있습니다.")
    confirm = input(f"→ 이 키워드를 '{meaning}'으로 처리할까요? (y/n): ")
    return meaning if confirm.lower() == 'y' else None

def gpt_guess_keyword(keyword, context=""):
    # 실제로는 GPT API를 써야 함
    # 예시용 하드코딩 추론
    if "save" in keyword:
        return "remember"
    elif "send" in keyword or "emit" in keyword:
        return "signal"
    elif "connect" in keyword:
        return "link"
    return "leak"

def run_linter(path):
    with open(path, "r") as f:
        lines = f.readlines()

    ambiguous = detect_ambiguous_keywords(lines)

    if not ambiguous:
        print("✅ 문법적으로 문제 없음.")
        return

    print("⚠️ 구조 해석이 필요한 키워드가 있습니다:")

    for line, kw in ambiguous:
        replacement = interactive_repair(line, kw)
        if replacement:
            print(f"→ 제안: '{kw}' → '{replacement}'로 자동 수정 가능")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python kairose_linter_v2.py file.kairo")
    else:
        run_linter(sys.argv[1])

