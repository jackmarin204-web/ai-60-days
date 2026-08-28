# 作用：导入列表、元组和集合类型标注。
from typing import List, Set, Tuple

# 作用：导入 TF-IDF 文本向量化工具。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：导入余弦相似度计算函数。
from sklearn.metrics.pairwise import cosine_similarity


# 作用：计算问题和文档之间的关键词匹配分数。
def keyword_overlap_score(
    question: str,
    document: str,
) -> float:
    # 作用：提取问题中的英文和数字词语。
    question_words: Set[str] = {
        word.lower()
        for word in question.replace("？", "").split()
        if word.strip()
    }

    # 作用：提取文档中的英文和数字词语。
    document_words: Set[str] = {
        word.lower()
        for word in document.replace("。", "").split()
        if word.strip()
    }

    # 作用：问题没有有效词语时返回 0。
    if not question_words:
        return 0.0

    # 作用：计算问题词语和文档词语的交集。
    matched_words: Set[str] = question_words.intersection(
        document_words
    )

    # 作用：返回关键词匹配比例。
    return len(matched_words) / len(question_words)


# 作用：计算文档是否包含问题中的重要短语。
def phrase_match_score(
    question: str,
    document: str,
) -> float:
    # 作用：去除中文问号，得到更容易匹配的问题文本。
    normalized_question: str = question.replace("？", "")

    # 作用：如果完整问题出现在文档中，返回最高分。
    if normalized_question in document:
        return 1.0

    # 作用：把问题按照常见疑问词进行简单切分。
    question_parts: List[str] = (
        normalized_question
        .replace("如何", "")
        .replace("什么", "")
        .replace("哪里", "")
        .replace("怎样", "")
        .split()
    )

    # 作用：保留出现在文档中的有效短语。
    matched_parts: List[str] = [
        part
        for part in question_parts
        if part and part in document
    ]

    # 作用：没有匹配短语时返回 0。
    if not question_parts:
        return 0.0

    # 作用：计算短语匹配比例。
    return len(matched_parts) / len(question_parts)


# 作用：对第一阶段召回结果重新计算排序分数。
def rerank(
    candidates: List[Tuple[int, str, float]],
    question: str,
) -> List[Tuple[int, str, float, float, float]]:
    # 作用：保存重排序后的结果。
    reranked_results: List[
        Tuple[int, str, float, float, float]
    ] = []

    # 作用：遍历第一阶段召回的候选文档。
    for document_index, document, initial_score in candidates:
        # 作用：计算关键词匹配分数。
        keyword_score: float = keyword_overlap_score(
            question=question,
            document=document,
        )

        # 作用：计算短语匹配分数。
        phrase_score: float = phrase_match_score(
            question=question,
            document=document,
        )

        # 作用：融合初始分数、关键词分数和短语分数。
        rerank_score: float = (
            initial_score * 0.5
            + keyword_score * 0.3
            + phrase_score * 0.2
        )

        # 作用：保存重排序所需的全部信息。
        reranked_results.append(
            (
                document_index,
                document,
                rerank_score,
                initial_score,
                keyword_score,
            )
        )

    # 作用：按照重排序分数从高到低排序。
    reranked_results.sort(
        key=lambda item: item[2],
        reverse=True,
    )

    # 作用：返回排序后的结果。
    return reranked_results


# 作用：准备轻量级技术文档。
documents: List[str] = [
    "FastAPI 可以快速创建 Python Web API 接口。",
    "Python Web 框架可以帮助开发者构建后端服务。",
    "SQLite 是一种轻量级关系型数据库。",
    "SQLite 的数据通常保存在 .db 文件中。",
    "RAG 会先检索文档，再让模型生成答案。",
]

# 作用：定义用户问题。
question: str = "SQLite 的数据保存在哪里？"

# 作用：创建 TF-IDF 向量化器。
vectorizer: TfidfVectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4),
)

# 作用：把文档转换成 TF-IDF 矩阵。
document_matrix = vectorizer.fit_transform(documents)

# 作用：把用户问题转换成向量。
question_vector = vectorizer.transform([question])

# 作用：计算初始 TF-IDF 相似度。
initial_scores = cosine_similarity(
    question_vector,
    document_matrix,
)[0]

# 作用：保存第一阶段召回的候选结果。
candidates: List[Tuple[int, str, float]] = []

# 作用：假设第一阶段先保留全部文档作为候选。
for index, document in enumerate(documents):
    # 作用：保存文档编号、文档内容和初始相似度。
    candidates.append(
        (
            index,
            document,
            float(initial_scores[index]),
        )
    )

# 作用：执行第二阶段重排序。
reranked_results = rerank(
    candidates=candidates,
    question=question,
)

# 作用：打印用户问题。
print(f"问题：{question}")

# 作用：打印重排序后的结果。
print("\n重排序结果：")

# 作用：遍历重排序后的文档。
for rank, result in enumerate(reranked_results, start=1):
    # 作用：拆出当前结果中的字段。
    (
        document_index,
        document,
        rerank_score,
        initial_score,
        keyword_score,
    ) = result

    # 作用：打印排名和各项分数。
    print(
        f"\n第 {rank} 名"
        f"\n重排序分数：{rerank_score:.4f}"
        f"\n初始分数：{initial_score:.4f}"
        f"\n关键词分数：{keyword_score:.4f}"
        f"\n文档：{document}"
    )