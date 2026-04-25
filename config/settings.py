import os
from pathlib import Path
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 游戏项目保存目录
GAME_PROJECTS_DIR = ROOT_DIR / "game_projects"

# RAG知识库目录
KNOWLEDGE_BASE_DIR = ROOT_DIR / "rag" / "knowledge_base"

# 向量数据库目录
VECTOR_DB_DIR = ROOT_DIR / ".cache" / "vector_db"

# 日志目录
LOGS_DIR = ROOT_DIR / "logs"

# 自动创建所有目录
for dir_path in [GAME_PROJECTS_DIR, KNOWLEDGE_BASE_DIR, VECTOR_DB_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# ========================
# 通义千问 终极兼容配置（解决所有字段报错）
# ========================
load_dotenv()

model_client = OpenAIChatCompletionClient(
    model=os.getenv("LLM_MODEL_NAME"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    model_info={
        "name": "qwen-turbo",
        "family": "qwen",
        "description": "通义千问兼容模型",
        "context_length": 8192,
        "max_tokens": 1024,
        "supports_functions": True,
        "supports_streaming": True,
        "supports_vision": False,
        "supports_tools": True,
        "vision": False,
        "function_calling": True,
        "json_output": True
    }
)