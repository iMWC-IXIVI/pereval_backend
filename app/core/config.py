import os
import random
import string

from pathlib import Path, WindowsPath

from pydantic_settings import BaseSettings

from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    DB_URL: str
    BASE_DIR: WindowsPath = Path(__file__).parent.parent
    MEDIA_DIR: str = os.path.join(BASE_DIR, 'media')

    def generate_unique_value(self):
        result = [random.choice(string.digits) for _ in range(5)]
        random_alpha = [random.choice(string.ascii_letters) for _ in range(5)]

        result.extend(random_alpha)
        random.shuffle(result)

        return ''.join(result)

    class Config:
        env_file = '.env'


settings = Settings()
