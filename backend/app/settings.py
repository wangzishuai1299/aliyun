from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config= SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")
    DATABASE_URL:str="mysql+pymysql://root:root@127.0.0.1:3306/admin_db?charset=utf8mb4"
    TITLE:str="备忘录"

settings = Settings()