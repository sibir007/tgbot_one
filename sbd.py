import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

from telethon import TelegramClient, events
from decouple import Config, RepositoryEnv

# задаём расположение .env файла
DOTENV_FILE = './.env'

# загружаем переменные окружения из .env файла
dotenv_config =  Config(RepositoryEnv(DOTENV_FILE))

api_id = dotenv_config('APP_API_ID')
api_hash = dotenv_config('APP_API_HASH')

client = TelegramClient('anon', api_id=api_id, api_hash=api_hash)

async def main():
    entity = await client.get_entity("soniiikmill")
    print(entity.stringify())

with client:
    client.loop.run_until_complete(main())