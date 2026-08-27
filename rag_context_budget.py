# 作用：导入 dataclass，用于定义结构化数据对象。
from dataclasses import dataclass

# 作用：导入列表类型标注。
from typing import List


# 作用：表示一个带相似度的检索片段。
@dataclass
class RetrievedChunk:
    # 作用：保存文档来源。
    source: str

    # 作用：保存片段编号。
    chunk_id: int

    # 作用：保存片段文本。
    text: str

    # 作用：保存该片段与问题的相似度。
    score: float


# 作用：估算一段文本需要占用多少 Token。
def estimate_tokens(text: str) -> int:
    # 作用：用字符数量近似 Token 数量。
    return len(text)


# 作用：按照数量和 Token 预算选择检索片段。
def select_chunks_with_budget(
    chunks: List[RetrievedChunk],
    max_chunks: int = 3,
    max_tokens: int = 100,
) -> List[RetrievedChunk]:
    # 作用：保存最终被选中的片段。
    selected_chunks: List[RetrievedChunk] = []

    # 作用：记录当前已经使用的估算 Token 数。
    used_tokens: int = 0

    # 作用：按照相似度从高到低遍历片段。
    for chunk in chunks:
        # 作用：估算当前片段需要的 Token 数。
        current_tokens: int = estimate_tokens(chunk.text)

        # 作用：如果已经达到最大片段数量，则停止选择。
        if len(selected_chunks) >= max_chunks:
            break

        # 作用：如果加入当前片段会超过预算，则跳过当前片段。
        if used_tokens + current_tokens > max_tokens:
            continue

        # 作用：把当前片段加入最终上下文。
        selected_chunks.append(chunk)

        # 作用：更新已使用的 Token 数量。
        used_tokens += current_tokens

    # 作用：打印预算使用情况，方便调试。
    print(
        f"选择了 {len(selected_chunks)} 个片段，"
        f"估算使用 {used_tokens}/{max_tokens} Tokens"
    )

    # 作用：返回预算范围内的片段。
    return selected_chunks


# 作用：把选中的片段组合成模型上下文。
def build_context(
    chunks: List[RetrievedChunk],
) -> str:
    # 作用：保存每个片段的格式化文本。
    context_parts: List[str] = []

    # 作用：遍历所有被选中的片段。
    for chunk in chunks:
        # 作用：增加来源标记，让模型知道资料来自哪里。
        formatted_text: str = (
            f"[来源：{chunk.source}，片段：{chunk.chunk_id}]\n"
            f"{chunk.text}"
        )

        # 作用：保存当前格式化片段。
        context_parts.append(formatted_text)

    # 作用：用分隔线连接所有上下文片段。
    return "\n\n---\n\n".join(context_parts)


# 作用：准备按照相似度排序的模拟检索结果。
retrieved_chunks: List[RetrievedChunk] = [
    RetrievedChunk(
        source="sqlite_manual",
        chunk_id=1,
        text="SQLite 的数据通常保存在 .db 文件中。",
        score=0.91,
    ),
    RetrievedChunk(
        source="sqlite_manual",
        chunk_id=0,
        text="SQLite 是一种不需要独立服务器的轻量级关系型数据库。",
        score=0.82,
    ),
    RetrievedChunk(
        source="python_manual",
        chunk_id=2,
        text="Python 可以使用 sqlite3 模块连接 SQLite 数据库。",
        score=0.71,
    ),
    RetrievedChunk(
        source="fastapi_manual",
        chunk_id=0,
        text="FastAPI 可以创建 Python Web API 服务。",
        score=0.25,
    ),
]

# 作用：根据最大片段数和 Token 预算筛选上下文。
selected_chunks: List[RetrievedChunk] = select_chunks_with_budget(
    chunks=retrieved_chunks,
    max_chunks=3,
    max_tokens=100,
)

# 作用：把筛选后的片段组装成上下文。
context: str = build_context(
    chunks=selected_chunks,
)

# 作用：打印最终上下文。
print("\n========== 最终上下文 ==========")
print(context)

# 作用：打印最终上下文的估算长度。
print(
    f"\n上下文估算字符数："
    f"{estimate_tokens(context)}"
)