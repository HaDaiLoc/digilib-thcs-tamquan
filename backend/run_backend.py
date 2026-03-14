import os

import uvicorn


def get_server_config() -> tuple[str, int, bool]:
    port_env = os.getenv('PORT')
    host = os.getenv('HOST') or ('0.0.0.0' if port_env else '127.0.0.1')
    port = int(port_env or os.getenv('APP_PORT') or '8001')

    if 'UVICORN_RELOAD' in os.environ:
        reload_enabled = os.getenv('UVICORN_RELOAD', '').strip().lower() in {'1', 'true', 'yes', 'on'}
    else:
        reload_enabled = not bool(port_env)

    return host, port, reload_enabled


if __name__ == '__main__':
    host, port, reload_enabled = get_server_config()
    uvicorn.run('app.main:app', host=host, port=port, reload=reload_enabled)