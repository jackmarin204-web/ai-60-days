# 作用：导入 dataclass，用来定义结构化的数据对象。
from dataclasses import dataclass

# 作用：导入类型标注，帮助我们明确列表和字典中的数据类型。
from typing import Dict, List, Set, Tuple

# 作用：导入 TF-IDF 文本向量化工具。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：导入余弦相似度计算函数。
from sklearn.metrics.pairwise import cosine_similarity


# 作用：表示一个文档片段。
@dataclass
class DocumentChunk:
    # 作用：保存文档编号。
    doc_id: str

    # 作用：保存片段编号。
    chunk_id: int

    # 作用：保存片段文本。
    text: str


# 作用：表示一个用户问题及其正确答案片段。
@dataclass
class RetrievalQuery:
    # 作用：保存用户提出的问题。
    question: str

    # 作用：保存该问题对应的正确片段编号。
    relevant_chunk_ids: Set[str]


# 作用：根据文档片段和用户问题，返回相似度最高的结果。
def retrieve(
    chunks: List[DocumentChunk],
    question: str,
    top_k: int = 3,
) -> List[Tuple[DocumentChunk, float]]:
    # 作用：提取所有片段中的文本。
    chunk_texts: List[str] = [chunk.text for chunk in chunks]

    # 作用：创建 TF-IDF 向量化器。
    vectorizer: TfidfVectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
    )

    # 作用：根据所有文档片段建立词汇表并计算片段向量。
    chunk_matrix = vectorizer.fit_transform(chunk_texts)

    # 作用：使用相同的词汇表把用户问题转换为向量。
    question_vector = vectorizer.transform([question])

    # 作用：计算用户问题与每个片段之间的余弦相似度。
    similarity_scores = cosine_similarity(
        question_vector,
        chunk_matrix,
    )[0]

    # 作用：把片段和对应的相似度分数配对。
    scored_chunks: List[Tuple[DocumentChunk, float]] = list(
        zip(chunks, similarity_scores)
    )

    # 作用：按照相似度从高到低排序。
    scored_chunks.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    # 作用：只返回前 top_k 个结果。
    return scored_chunks[:top_k]


# 作用：计算一个问题的 Hit@K。
def calculate_hit_at_k(
    retrieved_chunks: List[Tuple[DocumentChunk, float]],
    relevant_chunk_ids: Set[str],
) -> int:
    # 作用：提取前 K 个结果的片段编号。
    retrieved_ids: Set[str] = {
        f"{chunk.doc_id}:{chunk.chunk_id}"
        for chunk, _ in retrieved_chunks
    }

    # 作用：如果返回结果与正确答案有交集，说明命中。
    if retrieved_ids.intersection(relevant_chunk_ids):
        return 1

    # 作用：没有找到正确片段时返回 0。
    return 0


# 作用：计算一个问题的 MRR。
def calculate_reciprocal_rank(
    retrieved_chunks: List[Tuple[DocumentChunk, float]],
    relevant_chunk_ids: Set[str],
) -> float:
    # 作用：逐个检查检索结果的排名位置。
    for rank, (chunk, _) in enumerate(retrieved_chunks, start=1):
        # 作用：生成当前片段的唯一编号。
        chunk_key: str = f"{chunk.doc_id}:{chunk.chunk_id}"

        # 作用：如果当前片段是正确答案，返回排名倒数。
        if chunk_key in relevant_chunk_ids:
            return 1 / rank

    # 作用：没有检索到正确答案时，倒数排名为 0。
    return 0.0


# 作用：创建用于练习的文档片段。
chunks: List[DocumentChunk] = [
    DocumentChunk(
        doc_id="ai_001",
        chunk_id=0,
        text="FastAPI 是一个用于创建 Python Web API 的现代框架。",
    ),
    DocumentChunk(
        doc_id="ai_001",
        chunk_id=1,
        text="FastAPI 支持类型检查，并且可以自动生成 Swagger 接口文档。",
    ),
    DocumentChunk(
        doc_id="ai_002",
        chunk_id=0,
        text="SQLite 是一种不需要独立服务器的轻量级关系型数据库。",
    ),
    DocumentChunk(
        doc_id="ai_003",
        chunk_id=0,
        text="RAG 会先检索相关文档，再把文档交给大语言模型生成答案。",
    ),
    DocumentChunk(
        doc_id="ai_004",
        chunk_id=0,
        text="交叉验证可以评估机器学习模型在不同数据划分上的稳定性。",
    ),
]


# 作用：创建测试问题，并明确每个问题对应的正确片段。
queries: List[RetrievalQuery] = [
    RetrievalQuery(
        question="如何使用 FastAPI 创建接口？",
        relevant_chunk_ids={"ai_001:0"},
    ),
    RetrievalQuery(
        question="FastAPI 能自动生成什么文档？",
        relevant_chunk_ids={"ai_001:1"},
    ),
    RetrievalQuery(
        question="RAG 如何生成答案？",
        relevant_chunk_ids={"ai_003:0"},
    ),
]


# 作用：保存所有问题的 Hit@3 分数。
hit_scores: List[int] = []

# 作用：保存所有问题的 MRR 分数。
mrr_scores: List[float] = []

# 作用：逐个评测每个测试问题。
for query in queries:
    # 作用：检索当前问题最相关的 3 个片段。
    retrieved_results = retrieve(
        chunks=chunks,
        question=query.question,
        top_k=3,
    )

    # 作用：计算当前问题是否命中正确片段。
    hit_score: int = calculate_hit_at_k(
        retrieved_chunks=retrieved_results,
        relevant_chunk_ids=query.relevant_chunk_ids,
    )

    # 作用：计算当前问题的正确答案排名倒数。
    reciprocal_rank: float = calculate_reciprocal_rank(
        retrieved_chunks=retrieved_results,
        relevant_chunk_ids=query.relevant_chunk_ids,
    )

    # 作用：保存当前问题的评测结果。
    hit_scores.append(hit_score)
    mrr_scores.append(reciprocal_rank)

    # 作用：打印当前问题。
    print(f"\n问题：{query.question}")

    # 作用：打印当前问题的检索结果。
    for rank, (chunk, score) in enumerate(retrieved_results, start=1):
        print(
            f"第 {rank} 名 | "
            f"相似度={score:.4f} | "
            f"{chunk.text}"
        )

    # 作用：打印当前问题的 Hit 和 MRR。
    print(f"Hit@3：{hit_score}")
    print(f"MRR：{reciprocal_rank:.4f}")


# 作用：计算所有问题的平均 Hit@3。
average_hit: float = sum(hit_scores) / len(hit_scores)

# 作用：计算所有问题的平均 MRR。
average_mrr: float = sum(mrr_scores) / len(mrr_scores)

# 作用：打印整体评测结果。
print("\n========== 检索评测结果 ==========")
print(f"平均 Hit@3：{average_hit:.2%}")
print(f"平均 MRR：{average_mrr:.4f}")
print("===================================")