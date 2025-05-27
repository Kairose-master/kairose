# kairose_cli.py
# 자연어 입력 → .kairo 파일 생성 → 실행 및 .eid 자동 생성 (v1.7)

import argparse
import os
from runtime.identity_translator import gpt_extract_intent
from runtime.semantic_layer import to_kairose_code
from runtime.leak_runtime import execute_intent_block, write_eid

def save_kairo_code(code: str, filename: str = "output.kairo") -> str:
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w") as f:
        f.write(code)
    print(f"[λeak] Kairose code saved to {path}")
    return path

def run_kairo_from_nl(nl: str, export_eid: bool = False):
    print(f"[λ] Interpreting natural input: \"{nl}\"")
    block = gpt_extract_intent(nl)
    code = to_kairose_code(block)
    save_kairo_code(code)
    execute_intent_block(block)
    if export_eid and block.emotion:
        write_eid(block.emotion, trace=[], affect=[], eid_id="eid_from_nl")

def main():
    parser = argparse.ArgumentParser(prog="kairose")
    parser.add_argument("--from-nl", type=str, help="자연어로부터 실행 흐름 생성")
    parser.add_argument("--export-eid", action="store_true", help=".eid 파일로 감정 구조 저장")

    args = parser.parse_args()

    if args.from_nl:
        run_kairo_from_nl(args.from_nl, export_eid=args.export_eid)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()