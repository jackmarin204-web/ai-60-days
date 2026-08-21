# 作用：导入 Python 标准库的单元测试工具。
import unittest

# 作用：导入 FastAPI 的测试客户端。
from fastapi.testclient import TestClient

# 作用：导入你的 FastAPI 应用。
from api import app


# 作用：创建一个不会真正占用 8000 端口的测试客户端。
# 它会在 Python 进程内部模拟 HTTP 请求。
client = TestClient(app)


# 作用：测试优先级技能查询接口。
class SkillApiTest(unittest.TestCase):
    # 作用：验证合法查询会返回成功状态码和列表。
    def test_priority_skills_success(self):
        # 作用：模拟 GET /skills/priority?minimum_priority=4。
        response = client.get(
            "/skills/priority",
            params={"minimum_priority": 4},
        )

        # 作用：确认 API 返回 HTTP 200。
        self.assertEqual(response.status_code, 200)

        # 作用：确认响应主体是 JSON 数组。
        self.assertIsInstance(response.json(), list)

        # 作用：确认至少返回一项技能。
        self.assertGreater(len(response.json()), 0)

    # 作用：验证非法查询参数会被 FastAPI 拒绝。
    def test_priority_skills_invalid_parameter(self):
        # 作用：发送超出 1 到 5 范围的优先级。
        response = client.get(
            "/skills/priority",
            params={"minimum_priority": 10},
        )

        # 作用：422 表示请求格式不符合接口模型。
        self.assertEqual(response.status_code, 422)

    # 作用：验证技能缺口接口能够返回结构化数据。
    def test_skill_gaps_success(self):
        # 作用：模拟查询 AI Application Engineer 岗位的技能缺口。
        response = client.get(
            "/skills/gaps",
            params={"role_name": "AI Application Engineer"},
        )

        # 作用：确认接口调用成功。
        self.assertEqual(response.status_code, 200)

        # 作用：确认接口返回的是列表。
        self.assertIsInstance(response.json(), list)

        # 作用：确认每条结果包含技能名称和缺口字段。
        first_skill = response.json()[0]
        self.assertIn("skill_name", first_skill)
        self.assertIn("skill_gap", first_skill)

    # 作用：验证不存在的技能会返回 404。
    def test_update_unknown_skill(self):
        # 作用：模拟修改数据库中不存在的 Java 技能。
        response = client.patch(
            "/progress/Java",
            json={"current_level": 50},
        )

        # 作用：404 表示请求对象不存在。
        self.assertEqual(response.status_code, 404)

    # 作用：验证超出范围的掌握度会在 API 层被拒绝。
    def test_update_invalid_level(self):
        # 作用：发送超过 100 的非法掌握度。
        response = client.patch(
            "/progress/Python",
            json={"current_level": 101},
        )

        # 作用：422 表示请求体不符合 Pydantic 模型。
        self.assertEqual(response.status_code, 422)


# 作用：直接运行本文件时执行全部 API 测试。
if __name__ == "__main__":
    unittest.main(verbosity=2)