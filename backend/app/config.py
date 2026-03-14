from functools import lru_cache
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

    parsed = urlsplit(database_url)
    query = dict(parse_qsl(parsed.query))

    if 'render.com' in parsed.hostname and 'sslmode' not in query:
        query['sslmode'] = 'require'

    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


class Settings(BaseSettings):
    app_name: str = 'Digital Library API'
    api_prefix: str = '/api'
    secret_key: str = 'digital-library-secret-key'
    database_url: str
    cors_origins: list[str] = [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:4173',
        'http://127.0.0.1:4173',
    ]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    @property
    def sqlalchemy_database_url(self) -> str:
        return normalize_database_url(self.database_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
