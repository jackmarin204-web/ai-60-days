# 作用：导入列表、元组和字典类型标注。
from typing import Dict, List, Tuple

# 作用：导入 TF-IDF 向量化工具。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：导入余弦相似度计算函数。
from sklearn.metrics.pairwise import cosine_similarity


# 作用：计算问题与文档之间的简单关键词重叠分数。
def keyword_score(
    question: str,
    document: str,
) -> float:
    # 作用：把问题按空格切分成词语集合。
    question_words: set[str] = set(question.lower().split())

    # 作用：把文档按空格切分成词语集合。
    document_words: set[str] = set(document.lower().split())

    # 作用：如果问题没有有效词语，直接返回 0。
    if not question_words:
        return 0.0

    # 作用：计算问题词语和文档词语的交集。
    common_words: set[str] = question_words.intersection(
        document_words
    )

    # 作用：用匹配词数量除以问题词数量，得到关键词分数。
    return len(common_words) / len(question_words)


# 作用：使用关键词分数和 TF-IDF 分数进行混合检索。
def hybrid_search(
    documents: List[str],
    question: str,
    keyword_weight: float = 0.4,
    semantic_weight: float = 0.6,
) -> List[Tuple[int, str, float, float, float]]:
    # 作用：检查两个权重之和是否为 1。
    if abs(keyword_weight + semantic_weight - 1.0) > 1e-6:
        raise ValueError("两个权重之和必须等于 1")

    # 作用：创建字符级 TF-IDF 向量化器。
    vectorizer: TfidfVectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
    )

    # 作用：把所有文档转换成 TF-IDF 矩阵。
    document_matrix = vectorizer.fit_transform(documents)

    # 作用：使用相同词汇表转换用户问题。
    question_vector = vectorizer.transform([question])

    # 作用：计算问题与每篇文档的 TF-IDF 相似度。
    semantic_scores = cosine_similarity(
        question_vector,
        document_matrix,
    )[0]

    # 作用：保存所有文档的混合检索结果。
    results: List[Tuple[int, str, float, float, float]] = []

    # 作用：逐篇处理文档。
    for index, document in enumerate(documents):
        # 作用：计算当前文档的关键词重叠分数。
        current_keyword_score: float = keyword_score(
            question=question,
            document=document,
        )

        # 作用：读取当前文档的 TF-IDF 相似度。
        current_semantic_score: float = float(
            semantic_scores[index]
        )

        # 作用：按照权重融合两种分数。
        current_hybrid_score: float = (
            keyword_weight * current_keyword_score
            + semantic_weight * current_semantic_score
        )

        # 作用：保存文档编号、内容和三种分数。
        results.append(
            (
                index,
                document,
                current_hybrid_score,
                current_keyword_score,
                current_semantic_score,
            )
        )

    # 作用：按照混合分数从高到低排序。
    results.sort(
        key=lambda item: item[2],
        reverse=True,
    )

    # 作用：返回排序后的全部结果。
    return results


# 作用：准备一组轻量级技术文档。
documents: List[str] = [
    "FastAPI 可以快速创建 Python Web API 接口。",
    "Python Web 框架可以帮助开发者开发后端服务。",
    "SQLite 是一种轻量级关系型数据库。",
    "RAG 会先检索相关文档，再让模型生成答案。",
    "Python 的 sqlite3 模块可以连接 SQLite 数据库。",
]

# 作用：定义用户问题。
question: str = "怎样开发 Python API 服务？"

# 作用：执行混合检索。
results = hybrid_search(
    documents=documents,
    question=question,
    keyword_weight=0.4,
    semantic_weight=0.6,
)

# 作用：打印用户问题。
print(f"问题：{question}")

# 作用：逐个显示排序后的结果。
for rank, result in enumerate(results, start=1):
    # 作用：拆出当前结果的各个字段。
    (
        document_index,
        document,
        hybrid_score,
        current_keyword_score,
        current_semantic_score,
    ) = result

    # 作用：打印排名和各种分数。
    print(
        f"\n第 {rank} 名"
        f"\n混合分数：{hybrid_score:.4f}"
        f"\n关键词分数：{current_keyword_score:.4f}"
        f"\nTF-IDF 分数：{current_semantic_score:.4f}"
        f"\n文档：{document}"
    )