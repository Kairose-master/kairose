# identity_translator.py
# 자연어 → Kairose IntentBlock → Kairose 코드 트랜스파일러

from semantic_layer import IntentBlock
import json
import openai  # 가상 인터페이스 (GPT or LLM)

openai.api_key = "YOUR_API_KEY"

def gpt_extract_intent(nl: str) -> IntentBlock:
    system_prompt = """
You are an interpreter for the Kairose programming language.
You receive a natural language instruction and must output a structured JSON object
describing the user's intent, target, and emotional vector (λᴱ, ψᵢ, λᶠ if available).

Required format:
{
  "intent": "remember" | "execute" | "link" | "trace",
  "target": "<target_file_or_system>",
  "emotion": {
    "λᴱ": 0.92,
    "ψᵢ": 0.81
  }
}
"""

    user_prompt = f"Instruction: \"{nl}\""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = response["choices"][0]["message"]["content"]
    data = json.loads(content)

    return IntentBlock(
        intent=data["intent"],
        target=data.get("target"),
        emotion=data.get("emotion"),
        source_text=nl
    )
