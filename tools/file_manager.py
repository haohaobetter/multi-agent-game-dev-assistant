#  文件管理工具，给 Agent 用
import os
from pathlib import Path
from config.settings import GAME_PROJECTS_DIR

class FileManager:
    @staticmethod
    def save_game_code(game_name: str, code: str) -> str:
        """保存游戏代码到项目目录"""
        game_dir = GAME_PROJECTS_DIR / game_name
        game_dir.mkdir(exist_ok=True, parents=True)
        code_path = game_dir / "main.py"
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code)
        return str(code_path.resolve())

    @staticmethod
    def read_game_code(game_name: str) -> str:
        """读取游戏代码"""
        code_path = GAME_PROJECTS_DIR / game_name / "main.py"
        if code_path.exists():
            with open(code_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

file_manager = FileManager()