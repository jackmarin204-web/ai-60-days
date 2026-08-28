# 作用：导入 dataclass，用来定义结构化数据。
from dataclasses import dataclass

# 作用：导入列表和字典类型标注。
from typing import Any, Dict, List


# 作用：表示一个答案引用的知识库片段。
@dataclass
class SourceCitation:
    # 作用：保存来源文档名称。
    source: str

    # 作用：保存片段编号。
    chunk_id: int

    # 作用：保存片段原文。
    text: str

    # 作用：保存该片段的相关度。
    score: float


# 作用：表示一个标准化的 RAG 响应。
@dataclass
class RagResponse:
    # 作用：保存用户原始问题。
    question: str

    # 作用：保存系统生成的答案。
    answer: str

    # 作用：保存答案使用的引用来源。
    sources: List[SourceCitation]

    # 作用：保存整体置信度。
    confidence: float

    # 作用：表示答案是否有知识库依据。
    grounded: bool

    # 作用：把 Python 对象转换成 API 常用的字典格式。
    def to_dict(self) -> Dict[str, Any]:
        # 作用：把每一个来源对象转换成普通字典。
        source_items: List[Dict[str, Any]] = [
            {
                "source": source.source,
                "chunk_id": source.chunk_id,
                "text": source.text,
                "score": round(source.score, 4),
            }
            for source in self.sources
        ]

        # 作用：返回稳定的响应结构。
        return {
            "question": self.question,
            "answer": self.answer,
            "sources": source_items,
            "confidence": round(self.confidence, 4),
            "grounded": self.grounded,
        }


# 作用：根据检索结果构造一个可追溯的答案。
def build_rag_response(
    question: str,
    sources: List[SourceCitation],
    minimum_confidence: float = 0.20,
) -> RagResponse:
    # 作用：没有任何来源时，不能假装有依据。
    if not sources:
        # 作用：创建无证据时的安全回答。
        return RagResponse(
            question=question,
            answer="知识库中没有找到相关资料。",
            sources=[],
            confidence=0.0,
            grounded=False,
        )

    # 作用：取排名第一的来源作为主要证据。
    best_source: SourceCitation = sources[0]

    # 作用：读取最高相关度作为整体置信度。
    confidence: float = best_source.score

    # 作用：判断最高分是否达到最低可信阈值。
    grounded: bool = confidence >= minimum_confidence

    # 作用：达到阈值时使用证据原文作为示例答案。
    if grounded:
        # 作用：在没有连接大模型时，先返回抽取式答案。
        answer: str = best_source.text

    # 作用：相关度过低时拒绝给出确定答案。
    else:
        # 作用：创建低置信度回答。
        answer = "当前资料相关度不足，无法可靠回答。"

    # 作用：返回完整的结构化响应。
    return RagResponse(
        question=question,
        answer=answer,
        sources=sources,
        confidence=confidence,
        grounded=grounded,
    )


# 作用：准备模拟检索来源。
sources: List[SourceCitation] = [
    SourceCitation(
        source="sqlite_manual",
        chunk_id=1,
        text="SQLite 的数据通常保存在 .db 文件中。",
        score=0.91,
    ),
    SourceCitation(
        source="sqlite_manual",
        chunk_id=0,
        text="SQLite 是一种轻量级关系型数据库。",
        score=0.76,
    ),
]

# 作用：定义用户问题。
question: str = "SQLite 的数据保存在哪里？"

# 作用：根据问题和来源构造标准 RAG 响应。
response: RagResponse = build_rag_response(
    question=question,
    sources=sources,
)

# 作用：打印字典形式的 API 响应。
print(response.to_dict())