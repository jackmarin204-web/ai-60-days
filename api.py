# 作用：导入 FastAPI 应用框架。
from fastapi import FastAPI, HTTPException, Query

# 作用：导入已经写好的数据库查询函数。
# 这些函数负责查询 career.db，API 文件不直接写 SQL。
from career_query import (
    get_priority_skills,
    get_skill_gaps,
    update_skill_progress,
)

# 作用：导入 Pydantic，用于定义 API 数据模型和字段约束。
from pydantic import BaseModel, Field

# 作用：导入 Python 标准库日志工具。
import logging
# 作用：创建当前 API 服务的日志记录器。
logger = logging.getLogger("career_api")
# 作用：设置日志级别为 INFO，记录正常运行信息和错误信息。
logging.basicConfig(level=logging.INFO)


# 作用：定义客户端发送的技能进度请求体。
class ProgressUpdate(BaseModel):
    # 作用：掌握度必须是 0 到 100 之间的整数。
    current_level: int = Field(ge=0, le=100)


# 作用：定义 API 成功返回的技能进度结构。
class SkillProgressResponse(BaseModel):
    # 作用：返回被更新的技能名称。
    skill_name: str

    # 作用：返回更新后的当前掌握度。
    current_level: int = Field(ge=0, le=100)


# 作用：定义“岗位技能”接口返回的数据结构。
class PrioritySkill(BaseModel):
    # 作用：技能名称必须是字符串。
    skill_name: str

    # 作用：技能分类必须是字符串。
    category: str

    # 作用：目标掌握度必须是 0 到 100 之间的整数。
    target_level: int = Field(ge=0, le=100)

    # 作用：岗位优先级必须是 1 到 5 之间的整数。
    priority: int = Field(ge=1, le=5)


# 作用：定义“技能缺口”接口返回的数据结构。
class SkillGap(BaseModel):
    # 作用：技能名称必须是字符串。
    skill_name: str

    # 作用：岗位要求的目标掌握度。
    target_level: int = Field(ge=0, le=100)

    # 作用：个人当前掌握度。
    current_level: int = Field(ge=0, le=100)

    # 作用：岗位目标与个人当前水平之间的差值。
    skill_gap: int

    # 作用：岗位对该技能的重要程度。
    priority: int = Field(ge=1, le=5)

# 作用：创建 FastAPI 应用对象。
app = FastAPI(
    title="AI Career Skill API",
    description="查询 AI 应用工程师岗位技能要求与个人能力缺口。",
    version="1.0.0",
)


# 作用：定义查询优先级技能的 GET 接口。
@app.get("/skills/priority", response_model=list[PrioritySkill])
def read_priority_skills(
    # 作用：接收最低优先级，并限制在 1 到 5 之间。
    minimum_priority: int = Query(default=4, ge=1, le=5),
):
    # 作用：记录本次接口收到的查询参数。
    logger.info(
        "查询优先级技能，minimum_priority=%s",
        minimum_priority,
    )

    # 作用：调用数据库访问层并返回结果。
    result = get_priority_skills(minimum_priority)

    # 作用：记录本次返回了多少条数据。
    logger.info("查询完成，返回 %s 条技能记录", len(result))

    # 作用：将查询结果返回给客户端。
    return result



# 作用：查询岗位技能缺口，并声明返回一个 SkillGap 列表。
@app.get("/skills/gaps", response_model=list[SkillGap])
def read_skill_gaps(
    # 作用：接收岗位名称，并设置默认岗位。
    role_name: str = "AI Application Engineer",
):
    # 作用：查询数据库，并让 FastAPI 按 SkillGap 模型校验返回结果。
    return get_skill_gaps(role_name)

# 作用：定义修改技能进度的 PATCH 接口。
@app.patch(
    "/progress/{skill_name}",
    response_model=SkillProgressResponse,
)
def update_progress(
    # 作用：从 URL 路径中取得要修改的技能名称。
    skill_name: str,

    # 作用：从 JSON 请求体中取得新的掌握度。
    progress: ProgressUpdate,
):
    # 作用：调用数据库层执行实际更新。
    try:
        return update_skill_progress(
            skill_name,
            progress.current_level,
        )

    # 作用：将数据库层发现的不存在技能转换成 HTTP 404。
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

# 作用：提供服务健康检查接口。
@app.get("/health")
def health_check():
    # 作用：记录健康检查请求。
    logger.info("健康检查请求成功")

    # 作用：返回简单状态，供监控系统判断服务是否存活。
    return {
        "status": "ok",
        "service": "career-api",
    }