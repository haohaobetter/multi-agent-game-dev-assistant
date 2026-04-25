#让测试 Agent 能调用 语法检查工具
from autogen_agentchat.agents import AssistantAgent
from config.llm_config import model_client
import subprocess
import sys
from autogen_core.tools import FunctionTool

def check_syntax(code: str) -> str:
    with open("temp_test.py", "w", encoding="utf-8") as f:
        f.write(code)
    res = subprocess.run([sys.executable, "-m", "py_compile", "temp_test.py"], capture_output=True, text=True)
    return res.stderr

syntax_tool = FunctionTool(check_syntax, name="check_syntax", description="检查代码语法错误")

tester_agent = AssistantAgent(
    name="GameTester",
    model_client=model_client,
    tools=[syntax_tool],
    system_message="""
你是测试工程师。
必须先用 check_syntax 检查代码。
输出必须包含：
“代码合格” 或 “代码不合格”
"""
)