# 作用：导入 dataclass，用来创建结构清晰的数据对象。
from dataclasses import dataclass


# 作用：定义一个文档片段的数据结构。
@dataclass
class DocumentChunk:
    # 作用：保存原始文档的编号。
    doc_id: str

    # 作用：保存当前片段在原始文档中的顺序编号。
    chunk_id: int

    # 作用：保存当前片段的具体文本内容。
    text: str


# 作用：把一篇长文档切分成多个有重叠的小片段。
def split_text(
    text: str,
    chunk_size: int = 30,
    overlap: int = 8,
) -> list[str]:
    # 作用：检查片段长度是否为正数。
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    # 作用：检查重叠长度不能大于或等于片段长度。
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须满足 0 <= overlap < chunk_size")

    # 作用：保存最终切分得到的所有文本片段。
    chunks: list[str] = []

    # 作用：计算下一次切分的起始位置。
    start: int = 0

    # 作用：计算原文的总字符数。
    text_length: int = len(text)

    # 作用：只要起始位置还没有到达文本末尾，就继续切分。
    while start < text_length:
        # 作用：计算当前片段的结束位置。
        end: int = min(start + chunk_size, text_length)

        # 作用：截取当前片段。
        current_chunk: str = text[start:end]

        # 作用：去除片段首尾多余空白。
        cleaned_chunk: str = current_chunk.strip()

        # 作用：避免把空字符串加入结果列表。
        if cleaned_chunk:
            # 作用：保存当前有效片段。
            chunks.append(cleaned_chunk)

        # 作用：如果已经到达文本末尾，则停止循环。
        if end >= text_length:
            break

        # 作用：下一段从当前结束位置向前回退 overlap 个字符。
        start = end - overlap

    # 作用：返回所有切分后的文本片段。
    return chunks


# 作用：把普通字符串片段包装成带有元数据的 DocumentChunk 对象。
def build_document_chunks(
    doc_id: str,
    text: str,
    chunk_size: int = 30,
    overlap: int = 8,
) -> list[DocumentChunk]:
    # 作用：先调用切分函数，得到普通文本列表。
    text_chunks: list[str] = split_text(
        text=text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    # 作用：保存带有文档编号和片段编号的结果。
    document_chunks: list[DocumentChunk] = []

    # 作用：遍历所有文本片段，同时获得片段编号。
    for chunk_id, chunk_text in enumerate(text_chunks):
        # 作用：创建一个结构化的文档片段对象。
        chunk: DocumentChunk = DocumentChunk(
            doc_id=doc_id,
            chunk_id=chunk_id,
            text=chunk_text,
        )

        # 作用：把当前片段加入结果列表。
        document_chunks.append(chunk)

    # 作用：返回结构化的文档片段列表。
    return document_chunks


# 作用：准备一篇用于练习的轻量级技术文档。
fastapi_document: str = (
    "FastAPI 是一个现代化的 Python Web 框架。"
    "它可以快速创建 API 服务。"
    "FastAPI 支持类型检查和自动生成接口文档。"
    "开发者可以使用 Swagger 页面测试接口。"
)

# 作用：把 FastAPI 文档切分成带元数据的片段。
fastapi_chunks: list[DocumentChunk] = build_document_chunks(
    doc_id="fastapi_001",
    text=fastapi_document,
    chunk_size=30,
    overlap=8,
)

# 作用：打印所有切分结果，观察每个片段的编号和文本。
for chunk in fastapi_chunks:
    # 作用：显示原始文档编号、片段编号和片段内容。
    print(
        f"文档={chunk.doc_id} | "
        f"片段={chunk.chunk_id} | "
        f"内容={chunk.text}"
    )

# 作用：打印片段总数，帮助我们了解切分结果规模。
print(f"\n总片段数：{len(fastapi_chunks)}")