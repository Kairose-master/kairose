# pgc_flow_viz.py
# Pulse.json 기반 구조 실행 다이어그램 생성기

import json

def load_pulse(path=".pgc/Pulse.json"):
    with open(path, "r") as f:
        return json.load(f)

def to_mermaid(heartbeat):
    mermaid = ["graph TD"]
    nodes = []
    for i, entry in enumerate(heartbeat):
        label = entry.strip()
        node_id = chr(65 + i)
        nodes.append(f"{node_id}[{label}]")
        if i > 0:
            mermaid.append(f"{chr(65 + i - 1)} --> {node_id}")
    return "\n".join(["    " + n for n in nodes] + mermaid)

if __name__ == "__main__":
    pulse = load_pulse()
    hb = pulse["λ-Pulse"]["heartbeat"]
    output = to_mermaid(hb)
    with open("kairo.flowchart.mmd", "w") as f:
        f.write("```mermaid\n" + output + "\n```")
    print("[λ] Flowchart saved to kairo.flowchart.mmd")
