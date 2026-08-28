# 作用：导入抽象基类和抽象方法。
from abc import ABC, abstractmethod

# 作用：导入数据类。
from dataclasses import dataclass

# 作用：导入列表类型标注。
from typing import List


# 作用：表示一条检索证据。
@dataclass
class Evidence:
    # 作用：保存文档来源。
    source: str

    # 作用：保存片段编号。
    chunk_id: int

    # 作用：保存片段内容。
    text: str

    # 作用：保存相关度分数。
    score: float


# 作用：定义所有生成器必须遵守的统一接口。
class Generator(ABC):
    # 作用：声明生成答案的方法，但不提供具体实现。
    @abstractmethod
    def generate(
        self,
        question: str,
        evidence: List[Evidence],
    ) -> str:
        # 作用：抽象方法没有具体答案。
        pass


# 作用：创建一个不依赖外部模型的本地生成器。
class ExtractiveGenerator(Generator):
    # 作用：根据最高相关度证据直接抽取答案。
    def generate(
        self,
        question: str,
        evidence: List[Evidence],
    ) -> str:
        # 作用：没有证据时返回拒答。
        if not evidence:
            return "当前知识库没有找到相关资料。"

        # 作用：读取排名第一的证据。
        best_evidence: Evidence = evidence[0]

        # 作用：相关度过低时拒绝做出确定回答。
        if best_evidence.score < 0.20:
            return "当前资料相关度不足，无法可靠回答。"

        # 作用：返回证据原文作为本地示例答案。
        return best_evidence.text


# 作用：模拟一个将来可以连接真实大语言模型的生成器。
class MockLlmGenerator(Generator):
    # 作用：根据证据生成一个模拟答案。
    def generate(
        self,
        question: str,
        evidence: List[Evidence],
    ) -> str:
        # 作用：没有证据时不允许编造内容。
        if not evidence:
            return "资料不足，无法回答。"

        # 作用：提取所有证据文本。
        evidence_texts: List[str] = [
            item.text
            for item in evidence
        ]

        # 作用：使用固定模板模拟模型生成过程。
        return (
            f"根据知识库资料，关于“{question}”，"
            f"可以参考："
            f"{'；'.join(evidence_texts)}"
        )


# 作用：定义一个统一的 RAG 服务。
class RagService:
    # 作用：初始化 RAG 服务并注入一个生成器。
    def __init__(
        self,
        generator: Generator,
    ) -> None:
        # 作用：保存生成器对象。
        self.generator: Generator = generator

    # 作用：根据问题和检索证据生成答案。
    def answer(
        self,
        question: str,
        evidence: List[Evidence],
    ) -> str:
        # 作用：调用当前生成器完成答案生成。
        return self.generator.generate(
            question=question,
            evidence=evidence,
        )


# 作用：准备模拟检索证据。
evidence: List[Evidence] = [
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

# 作用：定义用户问题。
question: str = "SQLite 的数据保存在哪里？"

# 作用：创建使用本地抽取式生成器的服务。
extractive_service: RagService = RagService(
    generator=ExtractiveGenerator(),
)

# 作用：使用本地生成器生成答案。
extractive_answer: str = extractive_service.answer(
    question=question,
    evidence=evidence,
)

# 作用：创建使用模拟大模型生成器的服务。
mock_llm_service: RagService = RagService(
    generator=MockLlmGenerator(),
)

# 作用：使用模拟生成器生成答案。
mock_llm_answer: str = mock_llm_service.answer(
    question=question,
    evidence=evidence,
)

# 作用：打印抽取式生成结果。
print("========== 抽取式生成器 ==========")
print(extractive_answer)

# 作用：打印模拟大模型生成结果。
print("\n========== 模拟 LLM 生成器 ==========")
print(mock_llm_answer)