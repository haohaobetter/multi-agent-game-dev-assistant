# tools/code_executor.py
import subprocess
import sys
import subprocess
from pathlib import Path

# 加一个静态检查函数
def lint_code(code_path: str) -> dict:
    """用pylint检查代码规范"""
    try:
        result = subprocess.run(
            ["pylint", str(code_path), "--disable=all", "--enable=E,W,C"],
            capture_output=True,
            text=True
        )
        return {
            "success": result.returncode == 0,
            "errors": result.stdout
        }
    except Exception as e:
        return {"success": False, "errors": str(e)}

class CodeExecutor:
    def __init__(self, base_work_dir="./game_projects"):
        # 所有游戏项目的根目录，就在你项目文件夹里
        self.base_work_dir = Path(base_work_dir)
        # 如果文件夹不存在，自动创建
        self.base_work_dir.mkdir(exist_ok=True, parents=True)
        print(f"✅ 游戏项目根目录已创建：{self.base_work_dir.resolve()}")

    def save_code(self, code: str, game_name: str = "demo_game") -> str:
        """
        只做一件事：把大模型生成的代码保存到文件里
        返回：代码文件的绝对路径（方便你找到它）
        """
        # 每个游戏单独一个文件夹，避免混乱
        game_dir = self.base_work_dir / game_name
        game_dir.mkdir(exist_ok=True, parents=True)
        
        # 代码文件就叫main.py，放在游戏文件夹根目录
        code_path = game_dir / "main.py"

        # 把代码写进文件
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"💾 代码已保存到：{code_path.resolve()}")
        return str(code_path.resolve())

    def run_code(self, code_path: str) -> dict:
        """
        运行指定路径的Python代码
        返回：是否成功、标准输出、错误信息
        """
        code_path = Path(code_path)
        game_dir = code_path.parent  # 代码所在的文件夹，作为运行的工作目录

        try:
            # 用Python解释器运行这个文件
            result = subprocess.run(
                [sys.executable, str(code_path)],
                cwd=game_dir,  # 必须在游戏目录下运行，避免资源路径问题
                capture_output=True,
                text=True,
                timeout=30  # 防止死循环卡死
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "❌ 代码运行超时，可能存在死循环"
            }

# 实例化工具
code_executor = CodeExecutor(base_work_dir="./game_projects")