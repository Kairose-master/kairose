# pgc_flow_viz.py
# Pulse.json 기반 실행 구조 다이어그램 생성기 (v1.2.1 대응)

import json

def load_pulse(path=".pgc/Pulse.json"):
    with open(path, "r") as f:
        return json.load(f)

def to_mermaid(heartbeat):
    mermaid = ["graph TD"]
    nodes = []
    edges = []

    for i, entry in enumerate(heartbeat):
        label = entry.strip()
        node_id = f"N{i}"
        style = ""

        # 분기 라벨링
        if "→" in label:
            parts = label.split("→")
            kind = parts[0].strip()
            name = parts[1].strip()

            if "cycle" in kind:
                style = ":::cycle"
            elif "fallback" in kind:
                style = ":::fallback"
            elif "after" in kind:
                style = ":::after"

            node_label = f"{kind} → {name}" if kind else name
        else:
            node_label = label

        nodes.append(f'{node_id}["{node_label}"]')
        if i > 0:
            edges.append(f"N{i-1} --> {node_id}")

    return "\n".join(
        ["    " + n for n in nodes + edges] +
        [
            "    classDef cycle fill:#f9f,stroke:#333,stroke-width:2px;",
            "    classDef fallback fill:#fdd,stroke:#900;",
            "    classDef after fill:#ddf,stroke:#00f;"
        ]
    )

if __name__ == "__main__":
    pulse = load_pulse()
    hb = pulse["λ-Pulse"]["heartbeat"]
    output = to_mermaid(hb)
    with open("kairo.flowchart.mmd", "w") as f:
        f.write("```mermaid\n" + output + "\n```")
    print("[λ] Flowchart saved to kairo.flowchart.mmd")