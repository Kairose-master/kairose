# link.py
# 시스템 간 연결 선언기 (Link.sig 기록 및 갱신)

import os
import json
from datetime import datetime

LINK_SIG_PATH = ".pgc/Link.sig"

def load_link_sig():
    if os.path.exists(LINK_SIG_PATH):
        with open(LINK_SIG_PATH, "r") as f:
            return json.load(f)
    else:
        return {
            "λ-Link-Signature": {
                "this_repo": "unknown",
                "outputs": [],
                "links_to": [],
                "registered_at": None
            }
        }

def write_link_sig(target=None, via=None, this_repo="kairose-project"):
    data = load_link_sig()

    link_sig = data["λ-Link-Signature"]
    link_sig["this_repo"] = this_repo
    link_sig["registered_at"] = datetime.utcnow().isoformat()

    if via and via not in link_sig["outputs"]:
        link_sig["outputs"].append(via)

    if target and target not in link_sig["links_to"]:
        link_sig["links_to"].append(target)

    os.makedirs(".pgc", exist_ok=True)
    with open(LINK_SIG_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[λ-link] Updated link: {target} ← {via}")

def get_link_summary():
    sig = load_link_sig()["λ-Link-Signature"]
    return f"Repo: {sig['this_repo']}\nOutputs: {sig['outputs']}\nLinked to: {sig['links_to']}"

