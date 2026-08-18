# 作用：建立一份 AI 求职技能追踪器。
# 本程序练习列表、字典、循环、条件判断与基础统计。

# 作用：用字典保存“技能名称：当前掌握度”的对应关系。
# 掌握度范围暂定为 0 到 100。
skill_progress = {
    "Python": 30,
    "Git": 15,
    "SQL": 0,
    "后端开发": 0,
    "机器学习": 0,
    "大模型应用": 0,
    "数据结构与算法":0
}

# 作用：用列表规定学习顺序。
# 列表中的顺序就是我们后续建议的学习优先级。
learning_path = [
    "Python",
    "Git",
    "SQL",
    "后端开发",
    "机器学习",
    "大模型应用",
    "数据结构与算法"
]

# 作用：把今天的学习成果更新到字典。
# 这里的写法表示：找到 Python 对应的值，并把它更新为 35。
skill_progress["Python"] = 35
skill_progress["Git"] = 30

# 作用：创建变量，用于累计所有技能的掌握度。
total_progress = 0

# 作用：遍历学习路径中的每一项技能。
# skill 每次会依次取到 Python、Git、SQL 等名称。
for skill in learning_path:
    # 作用：根据技能名称，从字典中取出对应掌握度。
    current_progress = skill_progress[skill]

    # 作用：把每项技能的掌握度累加起来，为计算平均值做准备。
    total_progress = total_progress + current_progress

    # 作用：输出每项技能的当前状态。
    print(f"{skill}：{current_progress}%")

# 作用：计算平均掌握度。
# len(learning_path) 表示列表中共有多少项技能。
average_progress = total_progress / len(learning_path)

# 作用：根据所有技能的平均掌握度，判断你目前整体所处的学习阶段。
# 这不是逐项判断技能，而是对整个学习计划只判断一次。
if average_progress < 30:
    current_stage = "基础建设"
else:
    current_stage = "能力提升"

# 作用：找出第一项尚未达到 60% 的技能，作为下一步重点。
next_focus = None

for skill in learning_path:
    # 作用：如果当前技能还未达到 60%，就把它设为学习重点并停止查找。
    if skill_progress[skill] < 60:
        next_focus = skill
        break

        
# 作用：输出总览，:.1f 表示小数保留 1 位。
print("\n========== AI 求职技能报告 ==========")
print(f"平均掌握度：{average_progress:.1f}%")
print(f"当前阶段：{current_stage}")
print(f"下一项学习重点：{next_focus}")
print("====================================")