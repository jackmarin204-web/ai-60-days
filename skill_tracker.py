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

# 作用：集中定义技能的基础合格线。
# 后续如果规则变化，只需要修改这一处数值。
PASSING_SCORE = 60


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


# 作用：找出第一项未达到指定合格线的技能。
def find_next_focus(progress_data, ordered_skills, target_progress):
    # 作用：按照学习顺序逐项检查。
    for skill in ordered_skills:
        # 作用：使用传入的合格线判断，而不再把 60 写死。
        if progress_data[skill] < target_progress:
            return skill

    # 作用：全部达标时返回 None。
    return None


# 作用：找出所有未达到指定合格线的技能。
def find_skill_gaps(progress_data, ordered_skills, target_progress):
    # 作用：创建空列表，用于保存待提升技能。
    skill_gaps = []

    # 作用：按学习顺序筛选未达标技能。
    for skill in ordered_skills:
        # 作用：使用传入的合格线进行判断。
        if progress_data[skill] < target_progress:
            skill_gaps.append(skill)

    # 作用：返回待提升技能列表。
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

# 作用：显示当前技能，并接收一次用户输入来更新一项技能进度。
# 成功更新返回 True；输入无效时返回 False，且不修改原始数据。
def prompt_skill_update(progress_data, ordered_skills):
    # 作用：先展示可更新的技能和当前进度，避免用户记错名称。
    print("\n当前技能进度：")
    for skill in ordered_skills:
        print(f"- {skill}：{progress_data[skill]}%")

    # 作用：读取技能名称；strip() 会去除输入前后的空格。
    skill_name = input("\n请输入要更新的技能名称：").strip()

    # 作用：若技能不存在，停止本次更新，保护原始数据。
    if skill_name not in ordered_skills:
        print(f"更新失败：未找到技能“{skill_name}”。")
        return False

    # 作用：读取掌握度文本；input() 得到的永远是字符串。
    raw_progress = input("请输入新的掌握度（0-100）：").strip()

    # 作用：尝试把文本转成整数；转换失败时捕获 ValueError，避免程序崩溃。
    try:
        new_progress = int(raw_progress)
    except ValueError:
        print("更新失败：掌握度必须是 0 到 100 之间的整数。")
        return False

    # 作用：拒绝超出合理范围的数字，避免污染技能数据。
    if not 0 <= new_progress <= 100:
        print("更新失败：掌握度必须是 0 到 100 之间的整数。")
        return False

    # 作用：所有校验通过后，才真正修改字典中的技能进度。
    progress_data[skill_name] = new_progress

    # 作用：告知用户本次更新结果。
    print(f"更新成功：{skill_name} 已更新为 {new_progress}%。")
    return True



# 作用：组织一次完整的技能分析流程。
# 当前版本先验证数据并生成报告；下一步会在这里加入用户输入。
def main():
    # 作用：在计算前保证技能名称和掌握度都合法。
    validate_skill_data(skill_progress, learning_path)

   # 作用：运行更新函数，并接收它返回的成功或失败状态。
    update_succeeded = prompt_skill_update(skill_progress, learning_path)

# 作用：当输入无效时明确告知用户，后续报告将使用未修改的数据。
    if not update_succeeded:
        print("提示：本次输入无效，报告将使用原有技能数据。")

    # 作用：根据当前技能Python
    # 数据计算平均掌握度。
    average_progress = calculate_average(skill_progress, learning_path)

    # 作用：找出下一项未达到合格线的重点技能。
    next_focus = find_next_focus(
        skill_progress,
        learning_path,
        PASSING_SCORE,
    )

    # 作用：找出所有未达到合格线的技能。
    skill_gaps = find_skill_gaps(
        skill_progress,
        learning_path,
        PASSING_SCORE,
    )

    # 作用：根据平均掌握度判断当前学习阶段。
    current_stage = get_current_stage(average_progress)

    # 作用：计算当前重点距离合格线的差距。
    next_focus_gap = PASSING_SCORE - skill_progress[next_focus]

    # 作用：输出本次完整的技能分析报告。
    print_report(
        average_progress,
        current_stage,
        next_focus,
        next_focus_gap,
        skill_gaps,
    )


# 作用：只有直接运行本文件时才执行 main。
# 如果其他程序导入 skill_tracker，则不会自动输出报告。
if __name__ == "__main__":
    main()