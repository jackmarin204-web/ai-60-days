# 作用：导入 dataclass，用来定义结构化数据对象。
from dataclasses import dataclass

# 作用：导入列表和元组类型标注。
from typing import List, Tuple


# 作用：表示一个已经被检索到的文档片段。
@dataclass
class DocumentChunk:
    # 作用：记录片段来自哪篇文档。
    doc_id: str

    # 作用：记录片段在文档中的顺序编号。
    chunk_id: int

    # 作用：保存片段正文。
    text: str


# 作用：表示一个带有相似度分数的检索结果。
@dataclass
class RetrievedChunk:
    # 作用：保存文档片段对象。
    chunk: DocumentChunk

    # 作用：保存该片段与用户问题的相似度。
    score: float


# 作用：把检索结果格式化成模型可以阅读的上下文。
def build_context(
    retrieved_chunks: List[RetrievedChunk],
) -> str:
    # 作用：保存格式化后的上下文片段。
    context_parts: List[str] = []

    # 作用：遍历所有检索结果。
    for result in retrieved_chunks:
        # 作用：读取当前检索结果中的文档片段。
        chunk: DocumentChunk = result.chunk

        # 作用：把来源、片段编号、相似度和正文组织起来。
        formatted_part: str = (
            f"[来源文档：{chunk.doc_id}]\n"
            f"[片段编号：{chunk.chunk_id}]\n"
            f"[相似度：{result.score:.4f}]\n"
            f"[内容：{chunk.text}]"
        )

        # 作用：把当前格式化结果加入上下文列表。
        context_parts.append(formatted_part)

    # 作用：使用分隔线连接多个上下文片段。
    return "\n\n---\n\n".join(context_parts)


# 作用：构造完整的 RAG 提示词。
def build_rag_prompt(
    question: str,
    context: str,
) -> str:
    # 作用：定义模型必须遵守的回答规则。
    instructions: str = (
        "你是一个严谨的技术问答助手。\n"
        "请只根据提供的上下文回答问题。\n"
        "如果上下文没有答案，请明确说“当前资料不足”。\n"
        "不要编造上下文中不存在的事实。"
    )

    # 作用：把规则、上下文和问题拼接成完整提示词。
    prompt: str = (
        f"【系统规则】\n"
        f"{instructions}\n\n"
        f"【参考上下文】\n"
        f"{context}\n\n"
        f"【用户问题】\n"
        f"{question}\n\n"
        f"【回答要求】\n"
        f"请给出简洁、准确并带来源说明的答案。"
    )

    # 作用：返回完整提示词。
    return prompt


# 作用：准备两个模拟检索结果。
retrieved_results: List[RetrievedChunk] = [
    RetrievedChunk(
        chunk=DocumentChunk(
            doc_id="sqlite",
            chunk_id=0,
            text="SQLite 是一种轻量级关系型数据库。",
        ),
        score=0.82,
    ),
    RetrievedChunk(
        chunk=DocumentChunk(
            doc_id="sqlite",
            chunk_id=1,
            text="SQLite 的数据通常保存在一个 .db 文件中。",
        ),
        score=0.91,
    ),
]


# 作用：定义用户提出的问题。
user_question: str = "SQLite 的数据保存在哪里？"

# 作用：将检索结果整理为结构化上下文。
context_text: str = build_context(
    retrieved_chunks=retrieved_results,
)

# 作用：将问题和上下文组装成最终提示词。
final_prompt: str = build_rag_prompt(
    question=user_question,
    context=context_text,
)

# 作用：打印整理后的上下文。
print("========== 上下文 ==========")
print(context_text)

# 作用：打印最终传给模型的提示词。
print("\n========== 最终 Prompt ==========")
print(final_prompt)