# 作用：导入 dataclass，用于创建结构化数据对象。
from dataclasses import dataclass

# 作用：导入列表和集合类型标注。
from typing import List, Set


# 作用：表示一个带有来源信息的文档片段。
@dataclass
class Evidence:
    # 作用：保存文档来源名称。
    source: str

    # 作用：保存片段编号。
    chunk_id: int

    # 作用：保存片段的原始文本。
    text: str

    # 作用：保存该片段的检索相似度。
    score: float


# 作用：表示一条带引用的最终答案。
@dataclass
class AnswerWithCitations:
    # 作用：保存答案正文。
    answer: str

    # 作用：保存答案依赖的证据列表。
    evidence: List[Evidence]


# 作用：从证据中提取可以显示给用户的来源信息。
def format_citations(
    evidence: List[Evidence],
) -> str:
    # 作用：保存格式化后的来源文本。
    citation_parts: List[str] = []

    # 作用：记录已经出现过的来源，避免重复显示。
    seen_sources: Set[str] = set()

    # 作用：按照检索顺序处理所有证据。
    for item in evidence:
        # 作用：生成当前片段的唯一来源标识。
        citation_key: str = (
            f"{item.source}#{item.chunk_id}"
        )

        # 作用：跳过重复来源。
        if citation_key in seen_sources:
            continue

        # 作用：记录当前来源已经出现过。
        seen_sources.add(citation_key)

        # 作用：生成用户可以阅读的引用格式。
        citation_text: str = (
            f"[{item.source}，片段 {item.chunk_id}，"
            f"相关度 {item.score:.2f}]"
        )

        # 作用：保存当前引用。
        citation_parts.append(citation_text)

    # 作用：使用分号连接多个来源。
    return "；".join(citation_parts)


# 作用：检查答案是否至少有一条可靠证据。
def has_sufficient_evidence(
    evidence: List[Evidence],
    minimum_score: float = 0.20,
) -> bool:
    # 作用：逐个检查证据的相似度。
    for item in evidence:
        # 作用：只要有一条证据达到最低分数，就认为资料基本足够。
        if item.score >= minimum_score:
            return True

    # 作用：没有达到阈值时返回 False。
    return False


# 作用：根据问题和证据构造带引用的答案。
def build_answer(
    question: str,
    evidence: List[Evidence],
) -> AnswerWithCitations:
    # 作用：检查当前证据是否足以支持回答。
    sufficient: bool = has_sufficient_evidence(
        evidence=evidence,
        minimum_score=0.20,
    )

    # 作用：资料不足时拒绝编造答案。
    if not sufficient:
        # 作用：创建资料不足的安全回答。
        safe_answer: str = (
            "当前知识库中没有找到足够相关的资料，"
            "暂时无法可靠回答这个问题。"
        )

        # 作用：返回没有可靠结论的答案对象。
        return AnswerWithCitations(
            answer=safe_answer,
            evidence=evidence,
        )

    # 作用：在教学示例中，根据问题和第一条证据生成答案。
    main_evidence: Evidence = evidence[0]

    # 作用：把证据原文作为答案主体。
    answer_text: str = main_evidence.text

    # 作用：返回答案及其完整证据。
    return AnswerWithCitations(
        answer=answer_text,
        evidence=evidence,
    )


# 作用：准备一组模拟检索结果。
retrieved_evidence: List[Evidence] = [
    Evidence(
        source="sqlite_manual",
        chunk_id=1,
        text="SQLite 的数据通常保存在 .db 文件中。",
        score=0.91,
    ),
    Evidence(
        source="sqlite_manual",
        chunk_id=0,
        text="SQLite 是一种轻量级关系型数据库。",
        score=0.76,
    ),
]

# 作用：定义用户的问题。
user_question: str = "SQLite 的数据保存在哪里？"

# 作用：根据问题和检索证据构造答案。
result: AnswerWithCitations = build_answer(
    question=user_question,
    evidence=retrieved_evidence,
)

# 作用：格式化答案引用。
citations: str = format_citations(
    evidence=result.evidence,
)

# 作用：打印问题。
print(f"问题：{user_question}")

# 作用：打印答案正文。
print(f"\n答案：{result.answer}")

# 作用：打印引用来源。
print(f"\n来源：{citations}")