# 作用：AI 求职技能追踪器。
# 本程序使用字典、列表、循环、条件判断和函数，生成学习差距分析报告。

# 作用：保存“技能名称：当前掌握度”的原始数据。
skill_progress = {
    "Python": 35,
    "Git": 30,
    "SQL": 0,
    "后端开发": 0,
    "机器学习": 0,
    "大模型应用": 0,
    "数据结构与算法": 0,
}

# 作用：定义技能学习的推荐顺序。
learning_path = [
    "Python",
    "Git",
    "SQL",
    "后端开发",
    "机器学习",
    "大模型应用",
    "数据结构与算法",
]


# 作用：检查数据是否完整、掌握度是否处于合理范围。
# 参数 progress_data 是传入的技能字典；ordered_skills 是传入的学习顺序列表。
def validate_skill_data(progress_data, ordered_skills):
    # 作用：逐项检查学习路径中的技能。
    for skill in ordered_skills:
        # 作用：如果学习路径存在技能、字典却没有该技能的数据，就主动报错。
        if skill not in progress_data:
            raise ValueError(f"缺少技能数据：{skill}")

        # 作用：读取当前技能的掌握度。
        progress = progress_data[skill]

        # 作用：掌握度必须是 0 到 100 之间的数字。
        if not 0 <= progress <= 100:
            raise ValueError(f"{skill} 的掌握度必须在 0 到 100 之间。")


# 作用：计算所有技能的平均掌握度。
def calculate_average(progress_data, ordered_skills):
    # 作用：初始化总掌握度，准备累计每项技能的数值。
    total_progress = 0

    # 作用：按学习顺序读取每项技能的掌握度并累加。
    for skill in ordered_skills:
        total_progress += progress_data[skill]

    # 作用：用总掌握度除以技能数量，得到平均值并返回。
    return total_progress / len(ordered_skills)


# 作用：找出第一项尚未达到 60% 基础合格线的技能。
def find_next_focus(progress_data, ordered_skills):
    # 作用：按既定学习顺序逐项检查。
    for skill in ordered_skills:
        # 作用：找到第一项未达标技能后立刻返回，避免无效遍历。
        if progress_data[skill] < 60:
            return skill

    # 作用：如果全部技能都合格，返回 None，表示没有当前重点。
    return None


# 作用：筛选所有尚未达到 60% 的技能，并形成能力缺口列表。
def find_skill_gaps(progress_data, ordered_skills):
    # 作用：创建空列表，准备收集待提升技能。
    skill_gaps = []

    # 作用：逐项检查技能掌握度。
    for skill in ordered_skills:
        # 作用：把未达标技能加入列表。
        if progress_data[skill] < 60:
            skill_gaps.append(skill)

    # 作用：把分析得到的列表交还给调用者。
    return skill_gaps


# 作用：根据整体平均掌握度，判断当前学习阶段。
def get_current_stage(average_progress):
    # 作用：平均掌握度低于 30%，说明还处于基础建设期。
    if average_progress < 30:
        return "基础建设"

    # 作用：平均掌握度达到 30% 或更高，进入能力提升期。
    return "能力提升"


# 作用：集中输出报告，避免把输出逻辑散落在程序各处。
def print_report(average_progress, current_stage, next_focus, next_focus_gap, skill_gaps):
    # 作用：将待提升技能列表连接为适合阅读的一行文字。
    gaps_text = "、".join(skill_gaps)

    # 作用：输出最终报告。
    print("\n========== AI 求职技能报告 ==========")
    print(f"平均掌握度：{average_progress:.1f}%")
    print(f"当前阶段：{current_stage}")
    print(f"下一项学习重点：{next_focus}")
    print(f"该技能距离基础合格线还差：{next_focus_gap}%")
    print(f"待提升技能数量：{len(skill_gaps)} 项")
    print(f"待提升技能：{gaps_text}")
    print("====================================")


# 作用：在开始计算前，先保证数据可靠。
validate_skill_data(skill_progress, learning_path)

# 作用：依次调用函数，获得报告所需的分析结果。
average_progress = calculate_average(skill_progress, learning_path)
next_focus = find_next_focus(skill_progress, learning_path)
skill_gaps = find_skill_gaps(skill_progress, learning_path)
current_stage = get_current_stage(average_progress)

# 作用：计算当前重点与 60% 合格线之间的差距。
next_focus_gap = 60 - skill_progress[next_focus]

# 作用：把全部计算结果交给报告函数输出。
print_report(
    average_progress,
    current_stage,
    next_focus,
    next_focus_gap,
    skill_gaps,
)