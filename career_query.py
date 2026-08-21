# 作用：导入 Python 内置的 SQLite 数据库驱动。
import sqlite3

# 作用：提供自动关闭数据库连接的工具。
from contextlib import closing

# 作用：使用 Path 稳定地定位与当前代码同目录的数据库文件。
from pathlib import Path


# 作用：导入项目统一配置。
from settings import settings
# 作用：根据配置文件定位数据库。
DATABASE_PATH = Path(__file__).with_name(settings.database_path)


# 作用：执行任意查询，并将所有结果转换为字典列表。
# query 是 SQL 语句；parameters 是 SQL 占位符对应的参数。
def fetch_all(query: str, parameters: tuple = ()) -> list[dict]:
    # 作用：建立数据库连接，并确保函数结束时自动关闭连接。
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        # 作用：允许通过列名读取查询结果。
        connection.row_factory = sqlite3.Row

        # 作用：执行参数化 SQL，并取得全部结果行。
        rows = connection.execute(query, parameters).fetchall()

        # 作用：把 SQLite 行对象转换为普通 Python 字典。
        return [dict(row) for row in rows]

# 作用：查询优先级不低于指定值的岗位技能。
# minimum_priority 是调用者传入的最低优先级。
# -> list[dict] 是类型提示，表示函数返回“由多个字典组成的列表”。

def get_priority_skills(minimum_priority: int) -> list[dict]:
    # 作用：提前验证优先级范围，防止无效参数进入查询。
    if not 1 <= minimum_priority <= 5:
        raise ValueError("最低优先级必须在 1 到 5 之间。")

    # 作用：定义查询所需的 SQL。
    query = """
        SELECT
            skill_name,
            category,
            target_level,
            priority
        FROM job_requirements
        WHERE priority >= ?
        ORDER BY priority DESC, target_level DESC
    """

    # 作用：调用通用查询函数，并传入最低优先级参数。
    return fetch_all(query, (minimum_priority,))

# 作用：查询指定岗位的全部技能要求，并计算个人当前进度与岗位目标之间的差距。
# 作用：查询指定岗位的全部技能要求，并计算个人技能缺口。
# 作用：分页查询指定岗位的技能缺口。
def get_skill_gaps(
    role_name: str,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    # 作用：限制单页最大数量，避免客户端一次请求过多数据。
    if not 1 <= limit <= 100:
        raise ValueError("limit 必须在 1 到 100 之间。")

    # 作用：offset 不能是负数。
    if offset < 0:
        raise ValueError("offset 不能小于 0。")

    # 作用：建立数据库连接。
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # 作用：允许通过列名读取查询结果。
        connection.row_factory = sqlite3.Row

        # 作用：查询岗位技能，并限制本次返回的记录范围。
        cursor = connection.execute(
            """
            SELECT
                requirements.skill_name,
                requirements.target_level,
                COALESCE(progress.current_level, 0) AS current_level,
                requirements.target_level
                    - COALESCE(progress.current_level, 0) AS skill_gap,
                requirements.priority
            FROM job_requirements AS requirements
            LEFT JOIN learning_progress AS progress
                ON requirements.skill_name = progress.skill_name
            WHERE requirements.role = ?
            ORDER BY requirements.priority DESC, skill_gap DESC
            LIMIT ? OFFSET ?
            """,
            (role_name, limit, offset),
        )

        # 作用：读取当前页的数据并转换为字典列表。
        return [dict(row) for row in cursor.fetchall()]

    finally:
        # 作用：无论查询成功还是失败，都关闭数据库连接。
        connection.close()

# 作用：更新某项技能的个人掌握度，并返回更新后的记录。
def update_skill_progress(skill_name: str, current_level: int) -> dict:
    # 作用：在数据库层再次校验数值范围，不能只依赖 API 层。
    if not 0 <= current_level <= 100:
        raise ValueError("掌握度必须在 0 到 100 之间。")

    # 作用：建立数据库连接。
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # 作用：让查询结果支持通过列名读取。
        connection.row_factory = sqlite3.Row

        # 作用：确认这项技能确实存在于岗位要求表中。
        skill_row = connection.execute(
            """
            SELECT skill_name
            FROM job_requirements
            WHERE skill_name = ?
            """,
            (skill_name,),
        ).fetchone()

        # 作用：拒绝更新不存在的技能，避免写入无效数据。
        if skill_row is None:
            raise ValueError(f"不存在技能：{skill_name}")

        # 作用：新增技能进度；如果技能已存在，则更新原有进度。
        connection.execute(
            """
            INSERT INTO learning_progress (skill_name, current_level)
            VALUES (?, ?)
            ON CONFLICT(skill_name)
            DO UPDATE SET current_level = excluded.current_level
            """,
            (skill_name, current_level),
        )

        # 作用：将修改永久保存到 career.db。
        connection.commit()

        # 作用：读取刚刚保存的数据，作为函数返回结果。
        updated_row = connection.execute(
            """
            SELECT skill_name, current_level
            FROM learning_progress
            WHERE skill_name = ?
            """,
            (skill_name,),
        ).fetchone()

        # 作用：把数据库行转换为普通 Python 字典。
        return dict(updated_row)

    finally:
        # 作用：无论成功还是失败，都关闭数据库连接。
        connection.close()

# 作用：组织当前文件被直接运行时的演示流程。
def main():
    # 作用：查询优先级至少为 4 的核心技能。
    priority_skills = get_priority_skills(minimum_priority=4)

    # 作用：输出本次查询返回的记录数量。
    print(f"共找到 {len(priority_skills)} 项核心技能：")

    # 作用：遍历查询结果，并以容易阅读的格式输出。
    for skill in priority_skills:
        print(
            f"- {skill['skill_name']}："
            f"类别={skill['category']}，"
            f"目标={skill['target_level']}%，"
            f"优先级={skill['priority']}"
        )

    # 作用：查询 AI 应用工程师岗位的技能差距。
    skill_gaps = get_skill_gaps("AI Application Engineer")

# 作用：输出岗位目标、个人进度和需要补齐的差距。
    print("\n技能差距分析：")

# 作用：逐项显示技能缺口。
    for skill in skill_gaps:
        print(
            f"- {skill['skill_name']}："
            f"目标={skill['target_level']}%，"
            f"当前={skill['current_level']}%，"
            f"还差={skill['skill_gap']}%，"
            f"优先级={skill['priority']}"
            )


# 作用：只有直接运行 career_query.py 时才调用 main()。
# 将来 FastAPI 导入 get_priority_skills() 时，不会自动打印演示结果。
if __name__ == "__main__":
    main()