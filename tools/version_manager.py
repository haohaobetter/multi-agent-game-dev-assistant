import json
from datetime import datetime
from pathlib import Path

VERSION_FILE = Path("./game_projects/versions.json")

def init_version_file():
    if not VERSION_FILE.exists():
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def add_version_record(game_name, path, stage, description):
    record = {
        "game_name": game_name,
        "path": str(path),
        "stage": stage,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(VERSION_FILE, "r+", encoding="utf-8") as f:
        versions = json.load(f)
        versions.append(record)
        f.seek(0)
        json.dump(versions, f, ensure_ascii=False, indent=2)

# 初始化
init_version_file()