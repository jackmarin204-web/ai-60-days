# 作用：Day 01 学习进度计算器。
# 你将学习 input、数据类型转换、计算、条件判断和格式化输出。

# 作用：接收用户输入。
# 注意：input() 接收到的内容默认都是“文本”，即使你输入 3，也是字符串 "3"。
name = input("请输入你的名字：")
completed_days = int(input("你已经完成了多少天学习？"))
today_hours = float(input("你今天学习了多少小时？"))

# 作用：定义学习计划中的固定目标。
total_days = 60
daily_target_hours = 3

# 作用：计算学习进度与今天是否达标。
progress = completed_days / total_days * 100
hour_gap = today_hours - daily_target_hours

# 作用：用条件判断给出不同反馈。
if hour_gap >= 0:
    message = f"今天比计划多学习了 {hour_gap:.1f} 小时。"
else:
    message = f"今天距离计划还差 {-hour_gap:.1f} 小时。"

# 作用：使用三引号输出多行学习报告。
# :.1f 的意思是：将小数保留 1 位，例如 1.666 显示为 1.7。
print(f"""
========== 学习日报 ==========
学习者：{name}
总计划：{total_days} 天
已完成：{completed_days} 天
整体进度：{progress:.1f}%
今日学习：{today_hours:.1f} 小时
{message}
==============================
""")