# config/llm_config.py
import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai._model_info import ModelInfo

# 加载环境变量
load_dotenv()

# 模型配置（以通义千问为例，你可以换成自己的）
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL_NAME = os.getenv("LLM_MODEL_NAME")

# 自定义模型信息（解决第三方模型校验问题，补全所有字段）
CUSTOM_MODEL_INFO = ModelInfo(
    name=MODEL_NAME,
    family="qwen",
    context_window=128000,
    function_calling=True,
    json_output=True,
    structured_output=True,  # 补上这个，消除警告
    vision=False
)

# 创建模型客户端
model_client = OpenAIChatCompletionClient(
    model=MODEL_NAME,
    api_key=API_KEY,
    base_url=BASE_URL,
    model_info=CUSTOM_MODEL_INFO
)