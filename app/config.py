from os import getenv

from dotenv import load_dotenv


load_dotenv()

TOKEN = getenv("TOKEN")

TZ_INFO = "America/New_York"

DB_HOST = getenv("DB_HOST", default="localhost")
DB_PORT = getenv("DB_PORT", default=5432)
DB_NAME = getenv("DB_NAME", default="test")
DB_USER = getenv("DB_USER", default="test")
DB_PASSWORD = getenv("DB_PASSWORD", default="test")

CHAT_ID = int(getenv("CHAT_ID"))

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa
