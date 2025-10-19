from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_host: str = Field(default="localhost", alias="DATABASE_HOST")
    database_port: int = Field(default=5432, alias="DATABASE_PORT")
    database_username: str = Field(default="postgres", alias="DATABASE_USERNAME")
    database_password: str = Field(default="postgres", alias="DATABASE_PASSWORD")
    database_name: str = Field(default="planning_poker", alias="DATABASE_NAME")
    database_schema: str = Field(default="agile_scrum", alias="DATABASE_SCHEMA")

    database_pool_size: int = Field(default=10, alias="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=20, alias="DATABASE_MAX_OVERFLOW")
    database_echo: bool = Field(default=False, alias="DATABASE_ECHO")

    app_name: str = Field(default="Planning Poker", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")

    secret_key: str = Field(..., alias="SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.database_username}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"

settings = Settings()
