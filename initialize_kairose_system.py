import os
import zipfile

# 각 저장소와 하위 디렉토리 구조 정의
REPOS = {
    "kairose-lang": {
        "runtime": ["leak_runtime.py", "semantic_layer.py", "identity_translator.py"],
        "cli": ["kairose_cli.py", "kairose_linter_v2.py", "pgc_diff_runner.py", "pgc_recover.py", "pgc_flow_viz.py"],
        "spec": ["keywords.md", "bnf.txt"],
        "examples": ["01_memory_test.kairo"],
        "pgc-template/docs": ["README.md"]
    },
    "pgc-engine": {
        "modules": ["pulse.py", "memory.py", "trace.py", "link.py"]
    },
    "kairose-gpt": {
        "prompt_templates": ["memory_summarizer.txt", "pulse_visualizer.txt", "diff_analyzer.txt", "identity_prompt.txt"],
        "examples": ["input_nl.json", "output_kairo_code.json"]
    }
}

def create_structure():
    for repo, dirs in REPOS.items():
        for path, files in dirs.items():
            full_dir = os.path.join(repo, path)
            os.makedirs(full_dir, exist_ok=True)
            for fname in files:
                fpath = os.path.join(full_dir, fname)
                with open(fpath, "w", encoding="utf-8") as f:   # ← 여기!
                    f.write(f"# {fname} - placeholder\n")       # ← 여기 em dash도 일반 dash로 바꿨음
            print(f"[λ] Created: {full_dir}")

def zip_repo(repo_name):
    zip_name = f"{repo_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(repo_name):
            for file in files:
                path = os.path.join(root, file)
                relpath = os.path.relpath(path, os.path.dirname(repo_name))
                zipf.write(path, relpath)
    print(f"[λ] Zipped: {zip_name}")

def main():
    create_structure()
    for repo in REPOS:
        zip_repo(repo)

if __name__ == "__main__":
    main()
