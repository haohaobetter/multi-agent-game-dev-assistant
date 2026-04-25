from autogen_agentchat.agents import AssistantAgent
from config.llm_config import model_client

decider_agent = AssistantAgent(
    name="ChiefDirector",
    model_client=model_client,
    system_message="""
你是整个游戏开发项目的总指挥。
根据当前开发状态，只允许输出【一个关键词】，不能输出其他内容。

可选状态只有5个：
plan
code
test
fix
done

规则：
1. 还没有设计文档 → 输出 plan
2. 有文档没代码 → 输出 code
3. 有代码没测试 → 输出 test
4. 测试不合格 → 输出 fix
5. 测试合格 → 输出 done
"""
)