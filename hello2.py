from telethon import TelegramClient
from decouple import Config, RepositoryEnv

# задаём расположение .env файла
DOTENV_FILE = './.env'

# загружаем переменные окружения из .env файла
dotenv_config =  Config(RepositoryEnv(DOTENV_FILE))

api_id = dotenv_config('APP_API_ID')
api_hash = dotenv_config('APP_API_HASH')
client = TelegramClient('anon', api_hash=api_hash, api_id=api_id)

async def main():
    me = await client.get_me()
    
    print(me.stringify())

    print(me.username)
    print(me.phone)
    
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
        
with client:
    client.loop.run_until_complete(main())