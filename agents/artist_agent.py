from autogen_agentchat.agents import AssistantAgent
from config.settings import model_client

# 这里必须叫 artist_agent！！！
artist_agent = AssistantAgent(
    name="ArtDirector",
    model_client=model_client,
    system_message="""
你是游戏美术总监，根据游戏类型，生成：
1. 主色调/配色方案（用RGB值表示）
2. 美术风格关键词（如像素风、赛博朋克）
3. 背景/角色/道具的AI绘图提示词
只输出结构化内容，不要多余解释。
"""
)