# 作用：导入 TF-IDF 文本向量化工具。
from sklearn.feature_extraction.text import TfidfVectorizer

# 作用：导入截断奇异值分解，用于把高维矩阵压缩成低维矩阵。
from sklearn.decomposition import TruncatedSVD

# 作用：导入余弦相似度计算函数。
from sklearn.metrics.pairwise import cosine_similarity

# 作用：导入 NumPy，用于处理数值数组。
import numpy as np


# 作用：准备一组轻量级中文技术文档。
documents: list[str] = [
    "FastAPI 可以快速创建 Python Web API 接口。",
    "Python Web 框架可以帮助开发者创建后端 API 服务。",
    "SQLite 是一种轻量级关系型数据库。",
    "RAG 会检索相关文档，再让模型生成答案。",
    "向量数据库可以保存文档的 Embedding 向量。",
]

# 作用：创建 TF-IDF 向量化器。
vectorizer: TfidfVectorizer = TfidfVectorizer(
    # 作用：使用字符级别特征，适合处理中文文本。
    analyzer="char",

    # 作用：提取长度为 2 到 4 的连续字符片段。
    ngram_range=(2, 4),
)

# 作用：根据所有文档建立词汇表，并生成稀疏 TF-IDF 矩阵。
tfidf_matrix = vectorizer.fit_transform(documents)

# 作用：打印文档数量和 TF-IDF 特征数量。
print(f"文档数量：{tfidf_matrix.shape[0]}")
print(f"TF-IDF 特征数量：{tfidf_matrix.shape[1]}")

# 作用：创建 SVD 压缩器，把高维特征压缩成 3 个隐藏维度。
svd: TruncatedSVD = TruncatedSVD(
    n_components=3,
    random_state=42,
)

# 作用：根据 TF-IDF 矩阵学习主要模式，并生成稠密向量。
embedding_matrix: np.ndarray = svd.fit_transform(tfidf_matrix)

# 作用：打印压缩后的矩阵形状。
print(f"Embedding 矩阵形状：{embedding_matrix.shape}")

# 作用：逐篇显示每篇文档对应的稠密向量。
for index, document in enumerate(documents):
    # 作用：读取当前文档的向量。
    embedding_vector: np.ndarray = embedding_matrix[index]

    # 作用：打印文档编号、文本和向量。
    print(f"\n文档 {index}：{document}")
    print(f"向量：{embedding_vector}")

# 作用：定义一个用户问题。
question: str = "如何开发 Python API？"

# 作用：使用已经建立的词汇表，把问题转换成 TF-IDF 向量。
question_tfidf = vectorizer.transform([question])

# 作用：使用已经训练好的 SVD，把问题压缩成稠密向量。
question_embedding: np.ndarray = svd.transform(question_tfidf)

# 作用：计算问题向量与所有文档向量之间的余弦相似度。
similarity_scores: np.ndarray = cosine_similarity(
    question_embedding,
    embedding_matrix,
)[0]

# 作用：按照相似度从高到低获得文档编号。
ranked_indexes: np.ndarray = np.argsort(
    similarity_scores
)[::-1]

# 作用：打印问题和排序结果。
print(f"\n问题：{question}")
print("\n相似度排序结果：")

# 作用：遍历排序后的文档编号。
for rank, document_index in enumerate(ranked_indexes, start=1):
    # 作用：读取当前文档的相似度。
    score: float = similarity_scores[document_index]

    # 作用：打印排名、相似度和文档内容。
    print(
        f"第 {rank} 名 | "
        f"相似度={score:.4f} | "
        f"{documents[document_index]}"
    )