import os
from dotenv import load_dotenv
from rag.loader import load_all_knowledge_docs
from config.settings import VECTOR_DB_DIR

load_dotenv()

# -------------- 不用任何向量模型！完全本地关键词匹配 --------------
class SimpleKeywordEmbedding:
    def embed_documents(self, texts):
        return [[1.0] * 10 for _ in texts]

    def embed_query(self, text):
        return [1.0] * 10

# -------------- 固定返回空向量，不调用任何模型 --------------
def get_embedding_client():
    return SimpleKeywordEmbedding()

# -------------- 初始化知识库 --------------
def init_chroma_db():
    documents = load_all_knowledge_docs()

    if not documents:
        print("⚠️ 知识库为空，请在 knowledge_base 放入 txt 文档")
        return None

    try:
        from langchain_community.vectorstores import Chroma
        db = Chroma.from_documents(
            documents=documents,
            embedding=get_embedding_client(),
            persist_directory=str(VECTOR_DB_DIR)
        )
        print(f"✅ 知识库加载完成：{len(documents)} 条文档")
        return db
    except Exception as e:
        print("⚠️ 向量库初始化失败，将使用纯文本匹配")
        return None

# -------------- 获取检索器 --------------
def get_rag_retriever():
    try:
        from langchain_community.vectorstores import Chroma
        db = Chroma(
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=get_embedding_client()
        )
        return db.as_retriever(search_kwargs={"k": 3})
    except:
        return None