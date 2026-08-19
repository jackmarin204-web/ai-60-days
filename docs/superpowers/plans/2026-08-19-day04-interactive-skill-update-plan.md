# Day 04 Interactive Skill Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow a learner to update one skill's progress through terminal input and immediately receive an updated report.

**Architecture:** Keep all logic in `skill_tracker.py`. Move the existing execution statements into `main()` so importing the file does not start an interactive session. Add one input function that validates a skill name and a 0–100 numeric progress value, updates the existing dictionary only after validation, and returns a success flag.

**Tech Stack:** Python 3 standard library; existing lists, dictionaries, functions, `input()`, `try`/`except`.

---

### Task 1: Isolate program startup

**Files:**
- Modify: `skill_tracker.py` (the current execution statements after `print_report`)
- Test: terminal execution of `python3 skill_tracker.py`

- [ ] **Step 1: Write the expected behavior down before changing code**

Expected behavior: importing `skill_tracker` must not print a report or ask for input; running `python3 skill_tracker.py` must start the program.

- [ ] **Step 2: Verify the current behavior is not import-safe**

Run:

```bash
python3 -c "import skill_tracker"
```

Expected: the current report prints during import, proving the execution statements need to be isolated.

- [ ] **Step 3: Replace the bottom execution statements with a `main` function and entry-point guard**

```python
# 作用：组织一次完整的交互、分析和报告流程。
def main():
    # 作用：在计算前保证初始技能数据完整且合法。
    validate_skill_data(skill_progress, learning_path)

    # 作用：后续任务会在此处调用交互更新函数。
    print("技能追踪器已启动。")


# 作用：只有直接运行本文件时才启动程序；被其他文件导入时不自动执行。
if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Verify both execution modes**

Run:

```bash
python3 -c "import skill_tracker"
python3 skill_tracker.py
```

Expected: the first command has no output; the second displays `技能追踪器已启动。`.

- [ ] **Step 5: Commit the isolated entry point**

```bash
git add skill_tracker.py
git commit -m "refactor: isolate skill tracker entry point"
```

### Task 2: Add safe single-skill input

**Files:**
- Modify: `skill_tracker.py` (add a function before `main`, then call it from `main`)
- Test: terminal runs with valid, unknown, nonnumeric, and out-of-range input

- [ ] **Step 1: Define the input/output contract**

`prompt_skill_update(progress_data, ordered_skills)` shows every skill and its current progress, asks for a skill name and a new progress value, changes the dictionary only for valid input, and returns `True` on success or `False` otherwise.

- [ ] **Step 2: Add the minimal validation function**

```python
# 作用：接收一次技能更新输入；成功更新时返回 True，失败时返回 False。
def prompt_skill_update(progress_data, ordered_skills):
    # 作用：先显示可更新的技能及其当前进度，帮助用户输入正确名称。
    print("\n当前技能进度：")
    for skill in ordered_skills:
        print(f"- {skill}：{progress_data[skill]}%")

    # 作用：读取用户希望更新的技能名称，并去掉输入两端的空格。
    skill_name = input("\n请输入要更新的技能名称：").strip()

    # 作用：未知技能不能更新，直接提示并结束本次输入。
    if skill_name not in ordered_skills:
        print(f"更新失败：未找到技能“{skill_name}”。")
        return False

    # 作用：读取进度文本，并尝试将其转换为整数。
    raw_progress = input("请输入新的掌握度（0-100）：").strip()
    try:
        new_progress = int(raw_progress)
    except ValueError:
        print("更新失败：掌握度必须是 0 到 100 之间的整数。")
        return False

    # 作用：拒绝不在合理范围内的数值，保护原始数据。
    if not 0 <= new_progress <= 100:
        print("更新失败：掌握度必须是 0 到 100 之间的整数。")
        return False

    # 作用：全部校验通过后才修改原字典，并向调用者报告成功。
    progress_data[skill_name] = new_progress
    print(f"更新成功：{skill_name} 已更新为 {new_progress}%。")
    return True
```

- [ ] **Step 3: Call the function from `main` and restore the existing analysis flow**

```python
# 作用：运行一次交互更新；输入无效时保留原数据并继续展示报告。
prompt_skill_update(skill_progress, learning_path)

# 作用：基于最新且已校验的数据生成报告所需结果。
average_progress = calculate_average(skill_progress, learning_path)
next_focus = find_next_focus(skill_progress, learning_path, PASSING_SCORE)
skill_gaps = find_skill_gaps(skill_progress, learning_path, PASSING_SCORE)
current_stage = get_current_stage(average_progress)
next_focus_gap = PASSING_SCORE - skill_progress[next_focus]

# 作用：展示本次输入后的完整分析报告。
print_report(
    average_progress,
    current_stage,
    next_focus,
    next_focus_gap,
    skill_gaps,
)
```

- [ ] **Step 4: Run four boundary tests**

Run `python3 skill_tracker.py` four times with these inputs:

| 技能名 | 进度 | Expected |
|---|---|---|
| `Python` | `45` | Displays success; report uses Python 45%. |
| `不存在` | `40` | Displays unknown-skill failure; no data changes. |
| `Python` | `abc` | Displays numeric-input failure; no data changes. |
| `Python` | `101` | Displays range failure; no data changes. |

- [ ] **Step 5: Commit the interactive update**

```bash
git add skill_tracker.py
git commit -m "feat: add interactive skill progress updates"
git push
```
