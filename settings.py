# 作用：导入 Pydantic Settings 配置基类。
from pydantic_settings import BaseSettings, SettingsConfigDict


# 作用：定义整个项目的配置结构。
class Settings(BaseSettings):
    # 作用：当前运行环境，默认使用开发环境。
    app_env: str = "development"

    # 作用：数据库文件路径，默认使用 career.db。
    database_path: str = "career.db"

    # 作用：大模型 API Key；没有配置时允许为空。
    model_api_key: str | None = None

    # 作用：告诉 Pydantic 从 .env 文件读取配置。
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# 作用：创建整个项目共用的配置对象。
settings = Settings()