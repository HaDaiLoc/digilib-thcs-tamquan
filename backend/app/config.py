import ast
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ENV_FILE = Path(__file__).resolve().parents[1] / '.env'


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

    parsed = urlsplit(database_url)
    query = dict(parse_qsl(parsed.query))

    if parsed.hostname and 'render.com' in parsed.hostname and 'sslmode' not in query:
        query['sslmode'] = 'require'

    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


def load_env_file() -> dict[str, str]:
    if not ENV_FILE.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def parse_cors_origins(raw_value: str | None) -> list[str]:
    default_origins = [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:4173',
        'http://127.0.0.1:4173',
    ]

    if not raw_value:
        return default_origins

    try:
        parsed = ast.literal_eval(raw_value)
    except (ValueError, SyntaxError):
        parsed = None

    if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
        return parsed

    return [origin.strip() for origin in raw_value.split(',') if origin.strip()] or default_origins


def get_env_value(env_values: dict[str, str], *keys: str, default: str = '') -> str:
    for key in keys:
        value = os.getenv(key) or env_values.get(key)
        if value:
            return value
    return default


@dataclass(frozen=True)
class Settings:
    app_name: str = 'Digital Library API'
    api_prefix: str = '/api'
    secret_key: str = 'digital-library-secret-key'
    database_url: str = ''

    # Kept as nvidia_* for backward compatibility with existing app code.
    nvidia_api_base_url: str = 'https://router.huggingface.co/v1'
    nvidia_api_key: str = ''
    nvidia_model: str = 'google/gemma-4-31b-it:novita'

    ai_request_timeout_seconds: int = 45
    ai_max_response_tokens: int = 1024
    ai_candidate_limit: int = 15
    ai_max_question_length: int = 500
    cors_origin_regex: str = r'^https?://(localhost|127\.0\.0\.1)(:\d+)?$'
    cors_origins: list[str] = field(default_factory=lambda: [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:4173',
        'http://127.0.0.1:4173',
    ])

    @property
    def sqlalchemy_database_url(self) -> str:
        return normalize_database_url(self.database_url)


@lru_cache
def get_settings() -> Settings:
    env_values = load_env_file()
    database_url = get_env_value(env_values, 'DATABASE_URL')

    if not database_url:
        raise RuntimeError('DATABASE_URL is missing. Set it in environment variables or backend/.env.')

    return Settings(
        app_name=get_env_value(env_values, 'APP_NAME', default='Digital Library API'),
        api_prefix=get_env_value(env_values, 'API_PREFIX', default='/api'),
        secret_key=get_env_value(env_values, 'SECRET_KEY', default='digital-library-secret-key'),
        database_url=database_url,
        nvidia_api_base_url=get_env_value(
            env_values,
            'NVIDIA_API_BASE_URL',
            'HF_API_BASE_URL',
            'AI_API_BASE_URL',
            default='https://router.huggingface.co/v1',
        ),
        nvidia_api_key=get_env_value(
            env_values,
            'NVIDIA_API_KEY',
            'HF_TOKEN',
            'HF_API_KEY',
            'AI_API_KEY',
            default='',
        ),
        nvidia_model=get_env_value(
            env_values,
            'NVIDIA_MODEL',
            'HF_MODEL',
            'AI_MODEL',
            default='google/gemma-4-31b-it:novita',
        ),
        ai_request_timeout_seconds=int(get_env_value(env_values, 'AI_REQUEST_TIMEOUT_SECONDS', default='30')),
        ai_max_response_tokens=int(get_env_value(env_values, 'AI_MAX_RESPONSE_TOKENS', default='700')),
        ai_candidate_limit=int(get_env_value(env_values, 'AI_CANDIDATE_LIMIT', default='10')),
        ai_max_question_length=int(get_env_value(env_values, 'AI_MAX_QUESTION_LENGTH', default='500')),
        cors_origin_regex=get_env_value(env_values, 'CORS_ORIGIN_REGEX', default=r'^https?://(localhost|127\.0\.0\.1)(:\d+)?$'),
        cors_origins=parse_cors_origins(get_env_value(env_values, 'CORS_ORIGINS')),
    )
