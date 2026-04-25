# agents/planner_agent.py
from autogen_agentchat.agents import AssistantAgent
from config.llm_config import model_client

# 变量名必须叫 planner_agent，和main.py里的import对应！
planner_agent = AssistantAgent(
    name="GamePlanner",
    model_client=model_client,
    system_message="""
你是专业的游戏策划师，擅长把用户的模糊需求
变成清晰、可开发、可落地的游戏设计文档。

输出格式必须包含：
1. 游戏类型
2. 游戏目标
3. 玩家操作
4. 游戏规则
5. 技术需求（告诉程序Agent要写什么功能）

语言简洁、专业、可直接交给程序员开发。
"""
)