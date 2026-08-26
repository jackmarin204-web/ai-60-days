# 作用：导入 dataclass，用于定义结构化的数据对象。
from dataclasses import dataclass

# 作用：导入列表和元组类型标注。
from typing import List, Tuple

# 作用：导入 TF-IDF 文本向量化工具。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：导入余弦相似度计算函数。
from sklearn.metrics.pairwise import cosine_similarity


# 作用：表示原始文档切分后形成的一个片段。
@dataclass
class DocumentChunk:
    # 作用：保存原始文档的唯一编号。
    doc_id: str

    # 作用：保存当前片段的顺序编号。
    chunk_id: int

    # 作用：保存当前片段的具体文本。
    text: str


# 作用：把长文本切分成多个有重叠的小片段。
def split_text(
    text: str,
    chunk_size: int = 45,
    overlap: int = 10,
) -> List[str]:
    # 作用：检查片段长度是否合理。
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    # 作用：检查重叠长度是否合法。
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")

    # 作用：保存所有切分后的文本片段。
    chunks: List[str] = []

    # 作用：记录当前切分的起始字符位置。
    start: int = 0

    # 作用：获取原始文本的字符总长度。
    text_length: int = len(text)

    # 作用：只要起始位置还没有到达文本末尾，就继续切分。
    while start < text_length:
        # 作用：计算当前片段的结束位置。
        end: int = min(start + chunk_size, text_length)

        # 作用：截取当前范围内的文本。
        current_text: str = text[start:end]

        # 作用：去除片段开头和结尾的空白。
        cleaned_text: str = current_text.strip()

        # 作用：避免保存空文本片段。
        if cleaned_text:
            # 作用：把有效片段加入结果列表。
            chunks.append(cleaned_text)

        # 作用：如果已经到达文档末尾，则结束循环。
        if end >= text_length:
            break

        # 作用：下一段从当前位置向前重叠指定字符。
        start = end - overlap

    # 作用：返回切分后的文本片段。
    return chunks


# 作用：把一篇文档转换成带有编号的 DocumentChunk 列表。
def create_chunks(
    doc_id: str,
    text: str,
    chunk_size: int = 45,
    overlap: int = 10,
) -> List[DocumentChunk]:
    # 作用：调用切分函数，获得普通文本片段。
    text_chunks: List[str] = split_text(
        text=text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    # 作用：保存结构化的文档片段。
    document_chunks: List[DocumentChunk] = []

    # 作用：遍历所有文本片段，并获得它们的编号。
    for chunk_id, chunk_text in enumerate(text_chunks):
        # 作用：创建一个带元数据的片段对象。
        chunk: DocumentChunk = DocumentChunk(
            doc_id=doc_id,
            chunk_id=chunk_id,
            text=chunk_text,
        )

        # 作用：保存当前片段。
        document_chunks.append(chunk)

    # 作用：返回当前文档的所有片段。
    return document_chunks


# 作用：负责保存文档片段，并执行相似度检索。
class LocalRetriever:
    # 作用：初始化检索器。
    def __init__(self, chunks: List[DocumentChunk]) -> None:
        # 作用：保存所有文档片段。
        self.chunks: List[DocumentChunk] = chunks

        # 作用：创建字符级 TF-IDF 向量化器。
        self.vectorizer: TfidfVectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 4),
        )

        # 作用：提取所有文档片段的文本内容。
        chunk_texts: List[str] = [
            chunk.text
            for chunk in self.chunks
        ]

        # 作用：学习词汇表，并把所有片段转换成向量。
        self.chunk_matrix = self.vectorizer.fit_transform(chunk_texts)

    # 作用：检索与问题最相似的前 top_k 个片段。
    def search(
        self,
        question: str,
        top_k: int = 3,
    ) -> List[Tuple[DocumentChunk, float]]:
        # 作用：把用户问题转换成与文档相同空间的向量。
        question_vector = self.vectorizer.transform([question])

        # 作用：计算问题与每个片段之间的余弦相似度。
        scores = cosine_similarity(
            question_vector,
            self.chunk_matrix,
        )[0]

        # 作用：把片段和对应分数组合起来。
        scored_chunks: List[Tuple[DocumentChunk, float]] = list(
            zip(self.chunks, scores)
        )

        # 作用：按相似度从高到低排序。
        scored_chunks.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        # 作用：返回排名最靠前的若干结果。
        return scored_chunks[:top_k]


# 作用：准备三篇轻量级技术文档。
raw_documents: List[Tuple[str, str]] = [
    (
        "fastapi",
        "FastAPI 是一个现代化的 Python Web 框架。"
        "它可以快速创建 API 服务。"
        "FastAPI 支持类型检查和自动生成接口文档。"
        "开发者可以使用 Swagger 页面测试接口。",
    ),
    (
        "rag",
        "RAG 是一种检索增强生成技术。"
        "系统会先从知识库中检索相关文档。"
        "然后把相关文档和用户问题交给大语言模型。"
        "模型根据检索内容生成最终答案。",
    ),
    (
        "sqlite",
        "SQLite 是一种轻量级关系型数据库。"
        "它不需要单独运行数据库服务器。"
        "数据通常保存在一个 .db 文件中。"
        "Python 可以通过 sqlite3 模块访问 SQLite。",
    ),
]


# 作用：保存所有文档切分后得到的片段。
all_chunks: List[DocumentChunk] = []

# 作用：逐篇处理原始文档。
for document_id, document_text in raw_documents:
    # 作用：把当前文档切分成多个结构化片段。
    document_chunks: List[DocumentChunk] = create_chunks(
        doc_id=document_id,
        text=document_text,
    )

    # 作用：把当前文档的片段加入总片段列表。
    all_chunks.extend(document_chunks)


# 作用：创建本地检索器，并让它学习所有 chunk 的向量表示。
retriever: LocalRetriever = LocalRetriever(
    chunks=all_chunks,
)

# 作用：定义一个用户问题。
user_question: str = "SQLite 的数据保存在哪里？"

# 作用：检索与问题最相关的三个片段。
retrieval_results: List[Tuple[DocumentChunk, float]] = retriever.search(
    question=user_question,
    top_k=3,
)

# 作用：打印用户问题。
print(f"问题：{user_question}")

# 作用：打印检索结果。
print("\n检索到的上下文：")

# 作用：遍历所有检索结果。
for rank, (chunk, score) in enumerate(
    retrieval_results,
    start=1,
):
    # 作用：打印排名、相似度、来源文档和片段内容。
    print(
        f"\n第 {rank} 名"
        f"\n相似度：{score:.4f}"
        f"\n来源：{chunk.doc_id}"
        f"\n片段编号：{chunk.chunk_id}"
        f"\n内容：{chunk.text}"
    )