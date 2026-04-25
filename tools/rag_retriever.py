from rag.vector_store import get_rag_retriever

class RAGRetrieverTool:
    def __init__(self):
        self.retriever = get_rag_retriever()

    def search_knowledge(self, query: str) -> str:
        """
        根据问题检索Pygame游戏开发知识库
        :param query: 检索关键词
        :return: 参考文档文本
        """
        try:
            if self.retriever is None:
                return ""
            # 新版 LangChain 用 invoke 方法，而不是 get_relevant_documents
            docs = self.retriever.invoke(query)
            content = "\n\n".join([doc.page_content for doc in docs])
            return content
        except Exception as e:
            print(f"⚠️ RAG检索异常：{e}")
            return ""

# 全局单例
rag_tool = RAGRetrieverTool()