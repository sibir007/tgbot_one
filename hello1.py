from telethon import TelegramClient
from decouple import Config, RepositoryEnv

# задаём расположение .env файла
DOTENV_FILE = './.env'

# загружаем переменные окружения из .env файла
dotenv_config =  Config(RepositoryEnv(DOTENV_FILE))

api_id = dotenv_config('APP_API_ID')
api_hash = dotenv_config('APP_API_HASH')

with TelegramClient('anon', api_id=api_id, api_hash=api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
    