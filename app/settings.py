from os import environ


APP_HOST = environ.get('SRV_APP_HOST', '0.0.0.0')
APP_PORT = int(environ.get('SRV_APP_PORT', 8000))
DB_DSN = environ.get('SRV_DB_DSN', 'postgresql://postgres:postgres@127.0.0.1:5432/postgres')
