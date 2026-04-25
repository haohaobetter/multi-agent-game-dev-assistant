# main.py 
import os
os.environ["AUTOGEN_ENABLE_TELEMETRY"] = "0"

import asyncio
import time
from autogen_core import CancellationToken

# ========================
# 智能体（完全用你现有的）
# ========================
from agents.planner_agent import planner_agent
from agents.programmer_agent import programmer_agent
from agents.tester_agent import tester_agent
from agents.decider_agent import decider_agent
from agents.artist_agent import artist_agent  # <-- 直接用你的名字！

# ========================
# 工具（完全不变）
# ========================
from tools.code_executor import code_executor
from tools.file_manager import file_manager
from tools.rag_retriever import rag_tool
from tools.logger import dev_logger
from tools.version_manager import add_version_record

# ------------------------------
# 内存语法检查（不生成 temp_test.py）
# ------------------------------
def check_code_syntax_in_memory(code: str) -> dict:
    try:
        compile(code, "<string>", "exec")
        return {"success": True, "error": ""}
    except SyntaxError as e:
        return {"success": False, "error": str(e)}

# ------------------------------
# 通用Agent调用
# ------------------------------
async def run_agent(agent, task):
    dev_logger.info(f"调用智能体：{agent.name}")
    async for result in agent.run_stream(
        task=task,
        cancellation_token=CancellationToken()
    ):
        if hasattr(result, "messages") and result.messages:
            content = result.messages[-1].content.strip()
            dev_logger.info(f"{agent.name} 输出完成")
            return content
    return ""

# ------------------------------
# 主程序
# ------------------------------
async def main():
    dev_logger.info("=" * 60)
    dev_logger.info("🚀 多智能体游戏开发｜第五阶段 完整版")
    dev_logger.info("=" * 60)

    user_requirement = input("\n请输入游戏需求：")
    dev_logger.info(f"用户需求：{user_requirement}")

    # 安全加载RAG
    try:
        from rag.vector_store import init_chroma_db
        init_chroma_db()
        dev_logger.info("RAG知识库加载成功")
    except Exception as e:
        dev_logger.warning(f"RAG加载失败：{e}")

    # 核心状态
    state = "plan"
    plan = ""
    code = ""
    test_report = ""
    art_info = ""
    game_name = f"game_{int(time.time())}"

    # 防死循环
    max_fix_times = 2
    fix_count = 0

    while state != "done":
        dev_logger.info(f"当前阶段：{state} | 已修复：{fix_count}/{max_fix_times}")

        # 1. 策划
        if state == "plan":
            plan = await run_agent(planner_agent, user_requirement)
            dev_logger.info("游戏设计文档生成完成")
            state = "art"

        # 2. 美术设计（直接用你的 artist_agent）
        elif state == "art":
            art_info = await run_agent(artist_agent, f"根据游戏需求生成美术方案：{user_requirement}")
            dev_logger.info("美术方案生成完成")
            state = "code"

        # 3. 编写代码
        elif state == "code":
            rag_context = ""
            try:
                rag_context = rag_tool.search_knowledge("pygame开发规范 边界 事件循环")
            except Exception:
                rag_context = ""

            prompt = f"""
严格参考Pygame规范，结合美术方案写完整可运行代码。
- 配色方案必须体现在代码中
- 只输出Python代码，用```python ```包裹
- 禁止输出任何中文解释、禁止【】、禁止多余文本

设计文档：
{plan}
美术方案：
{art_info}
参考规范：
{rag_context}
"""
            code = await run_agent(programmer_agent, prompt)

            # 纯净提取代码
            if "```python" in code:
                code = code.split("```python")[-1].split("```")[0].strip()
            code_lines = code.splitlines()
            clean_lines = []
            for line in code_lines:
                if line.strip().startswith(("【", "】", "===", "---")):
                    continue
                clean_lines.append(line)
            code = "\n".join(clean_lines)

            # 语法检查
            syntax_check = check_code_syntax_in_memory(code)
            if not syntax_check["success"]:
                dev_logger.warning(f"语法错误：{syntax_check['error']}")
                test_report = syntax_check["error"]
                state = "fix"
                continue

            state = "test"

        # 4. 测试
        elif state == "test":
            test_report = await run_agent(tester_agent, f"检查下面Pygame代码的bug、运行错误、逻辑问题：\n{code}")
            if "代码合格" in test_report or "无问题" in test_report:
                state = "done"
            else:
                if fix_count >= max_fix_times:
                    dev_logger.warning("已达最大修复次数，强制结束")
                    state = "done"
                else:
                    state = "fix"

        # 5. 修复
        elif state == "fix":
            fix_count += 1
            fix_prompt = f"""
根据测试报告修复bug，只输出完整可运行Python代码：
问题：{test_report}
代码：{code}
"""
            fixed_code = await run_agent(programmer_agent, fix_prompt)
            if "```python" in fixed_code:
                fixed_code = fixed_code.split("```python")[-1].split("```")[0].strip()
            code = fixed_code
            state = "test"

        # 兜底
        if state not in ["plan", "art", "code", "test", "fix", "done"]:
            dev_logger.warning(f"未知状态：{state}，强制结束")
            state = "done"

    # 保存最终代码
    code_path = file_manager.save_game_code(game_name + "_最终成品", code)
    add_version_record(
        game_name=game_name,
        path=code_path,
        stage="final",
        description=user_requirement[:30]
    )
    dev_logger.info(f"最终游戏已保存：{code_path}")

    # 运行游戏
    print("\n🎮 正在启动游戏...")
    run_res = code_executor.run_code(code_path)
    if run_res["success"]:
        dev_logger.info("✅ 游戏运行成功")
    else:
        dev_logger.error(f"游戏运行失败：{run_res['stderr']}")

    dev_logger.info("开发流程全部结束！")

if __name__ == "__main__":
    asyncio.run(main())