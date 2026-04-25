from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_all_knowledge_docs():
    # 读取 rag/knowledge_base 下所有 txt 文档
    base_dir = Path(__file__).parent / "knowledge_base"
    docs_list = []

    # 只加载txt格式知识库
    for file in base_dir.rglob("*.txt"):
        loader = TextLoader(str(file), encoding="utf-8")
        docs_list.extend(loader.load())

    # 文本分块，适配大模型上下文
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    split_docs = splitter.split_documents(docs_list)
    return split_docs