# 作用：导入 FastAPI 应用框架。
from fastapi import FastAPI, Query

# 作用：导入已经写好的数据库查询函数。
# 这些函数负责查询 career.db，API 文件不直接写 SQL。
from career_query import get_priority_skills, get_skill_gaps


# 作用：创建 FastAPI 应用对象。
app = FastAPI(
    title="AI Career Skill API",
    description="查询 AI 应用工程师岗位技能要求与个人能力缺口。",
    version="1.0.0",
)


# 作用：定义 GET /skills/priority 接口，查询高优先级技能。
@app.get("/skills/priority")
def read_priority_skills(
    # 作用：接收查询参数，并限制其范围为 1 到 5。
    minimum_priority: int = Query(default=4, ge=1, le=5),
):
    # 作用：调用数据库访问层，并将结果自动转换为 JSON。
    return get_priority_skills(minimum_priority)


# 作用：定义 GET /skills/gaps 接口，查询指定岗位的技能缺口。
@app.get("/skills/gaps")
def read_skill_gaps(
    # 作用：接收岗位名称；默认查询 AI Application Engineer。
    role_name: str = "AI Application Engineer",
):
    # 作用：调用数据库访问层，返回岗位目标与个人进度的差距。
    return get_skill_gaps(role_name)