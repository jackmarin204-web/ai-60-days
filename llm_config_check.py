# 作用：导入 os，用于读取环境变量。
import os

# 作用：导入 Path，用于检查文件路径。
from pathlib import Path

# 作用：导入 load_dotenv，让程序读取项目根目录下的 .env 文件。
from dotenv import load_dotenv

# 作用：加载 .env 文件中的配置。
load_dotenv()


# 作用：读取指定名称的环境变量。
def read_required_env(name: str) -> str:
    # 作用：读取环境变量的原始值。
    value: str | None = os.getenv(name)

    # 作用：如果变量不存在或为空，则抛出异常。
    if not value:
        raise RuntimeError(
            f"缺少必要的环境变量：{name}"
        )

    # 作用：返回经过检查的环境变量值。
    return value


# 作用：检查项目目录中的 .env 文件是否存在。
env_file: Path = Path(".env")

# 作用：如果文件不存在，给出明确提示。
if not env_file.exists():
    print(
        "未找到 .env 文件。"
        "请先创建它，并配置 LLM_API_KEY。"
    )

# 作用：读取 API Key，但绝不打印完整密钥。
api_key: str | None = os.getenv("LLM_API_KEY")

# 作用：读取模型名称。
model_name: str | None = os.getenv("LLM_MODEL")

# 作用：判断 API Key 是否已经配置。
if api_key:
    # 作用：只显示密钥是否存在，不显示密钥内容。
    print("LLM_API_KEY：已配置")
else:
    # 作用：提示用户配置 API Key。
    print("LLM_API_KEY：未配置")

# 作用：判断模型名称是否已经配置。
if model_name:
    # 作用：显示模型名称。
    print(f"LLM_MODEL：{model_name}")
else:
    # 作用：提示用户配置模型名称。
    print("LLM_MODEL：未配置")