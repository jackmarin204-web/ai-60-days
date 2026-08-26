# 作用：将文本转换为 TF-IDF 向量。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：计算两个向量之间的余弦相似度。
from sklearn.metrics.pairwise import cosine_similarity


# 作用：创建少量模拟知识库文档。
# 每个字符串代表一段可以被检索的知识。
documents = [
    "FastAPI 可以快速创建 Python Web API。",
    "SQLite 是一种轻量级关系型数据库。",
    "RAG 会先检索相关文档，再让模型生成答案。",
    "Docker 可以将应用和运行环境打包在一起。",
    "交叉验证可以评估机器学习模型的稳定性。",
]

# 作用：定义用户提出的问题。
query = "如何使用 RAG 检索知识库？"

# 作用：创建 TF-IDF 向量化器。
# 使用字符 n-gram，适合当前中文轻量示例。
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4),
)

# 作用：根据知识库文档建立词表，并将所有文档转换为向量。
document_vectors = vectorizer.fit_transform(documents)

# 作用：使用已经建立的词表转换用户问题。
# 这里必须使用 transform，不能再次 fit。
query_vector = vectorizer.transform([query])

# 作用：计算用户问题与每篇文档之间的余弦相似度。
# [0] 表示取出唯一查询对应的相似度数组。
similarity_scores = cosine_similarity(
    query_vector,
    document_vectors,
)[0]

# 作用：将文档编号和相似度分数配对。
document_scores = enumerate(similarity_scores)

# 作用：按相似度从高到低排序。
ranked_documents = sorted(
    document_scores,
    key=lambda item: item[1],
    reverse=True,
)

# 作用：输出用户问题。
print(f"用户问题：{query}")

# 作用：输出排序后的检索结果。
print("\n检索结果：")

# 作用：只显示最相关的前 3 篇文档。
for rank, (document_index, score) in enumerate(
    ranked_documents[:3],
    start=1,
):
    # 作用：读取当前排序结果对应的原始文档。
    document = documents[document_index]

    # 作用：输出排名、相似度和文档内容。
    print(
        f"{rank}. 相似度={score:.3f}：{document}"
    )