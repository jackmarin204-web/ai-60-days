# 作用：导入 Python 自带的单元测试工具，不需要额外安装。
import unittest

# 作用：导入需要被验证的业务函数。
from skill_tracker import (
    calculate_average,
    find_next_focus,
    find_skill_gaps,
    get_current_stage,
    validate_skill_data,
)


# 作用：集中测试技能追踪器的核心业务规则。
class SkillTrackerTest(unittest.TestCase):
    # 作用：验证学习阶段的边界规则：30 以下基础建设，30 及以上能力提升。
    def test_current_stage_boundary(self):
        self.assertEqual(get_current_stage(29.9), "基础建设")
        self.assertEqual(get_current_stage(30), "能力提升")

    # 作用：验证平均掌握度计算是否正确。
    def test_calculate_average(self):
        progress_data = {"Python": 40, "Git": 60}
        ordered_skills = ["Python", "Git"]

        self.assertEqual(
            calculate_average(progress_data, ordered_skills),
            50,
        )

    # 作用：验证程序会按学习路径顺序找到第一个未达标技能。
    def test_find_next_focus(self):
        progress_data = {"Python": 60, "Git": 30, "SQL": 0}
        ordered_skills = ["Python", "Git", "SQL"]

        self.assertEqual(
            find_next_focus(progress_data, ordered_skills, 60),
            "Git",
        )

    # 作用：验证程序会找出全部未达标技能，且不包含正好达到合格线的技能。
    def test_find_skill_gaps(self):
        progress_data = {"Python": 60, "Git": 59, "SQL": 0}
        ordered_skills = ["Python", "Git", "SQL"]

        self.assertEqual(
            find_skill_gaps(progress_data, ordered_skills, 60),
            ["Git", "SQL"],
        )

    # 作用：验证掌握度超出 0 到 100 范围时，数据校验会明确拒绝。
    def test_validate_skill_data_rejects_invalid_progress(self):
        progress_data = {"Python": 101}
        ordered_skills = ["Python"]

        with self.assertRaises(ValueError):
            validate_skill_data(progress_data, ordered_skills)


# 作用：直接运行本文件时，启动 unittest 测试执行器并显示详细结果。
if __name__ == "__main__":
    unittest.main(verbosity=2)