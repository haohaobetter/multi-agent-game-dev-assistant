from autogen_agentchat.agents import AssistantAgent
from config.llm_config import model_client
from tools.rag_retriever import rag_tool
from autogen_core.tools import FunctionTool

# 把 RAG 包装成工具
def search_pygame_knowledge(query: str) -> str:
    """搜索 Pygame 开发知识库，获取正确的API、规范和代码示例"""
    return rag_tool.search_knowledge(query)

rag_tool_agent = FunctionTool(
    search_pygame_knowledge,
    name="search_pygame_knowledge",
    description="查询Pygame游戏开发官方规范"
)

programmer_agent = AssistantAgent(
    name="GameProgrammer",
    model_client=model_client,
    tools=[rag_tool_agent],  # 👈 绑定工具
    system_message="""
你是专业Pygame游戏工程师。
写代码必须：
1. 先调用 search_pygame_knowledge 获取规范
2. 严格使用整数坐标，禁止浮点
3. 必须做边界限制
4. 必须完整可运行
5. 语法绝对正确
"""
)