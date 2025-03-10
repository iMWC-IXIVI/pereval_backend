from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Database:
        DB_URL: str

    database: Database

    class Config:
        env_file = '.env'


settings = Settings()
