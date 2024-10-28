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
client.get_entity
client.get_input_entity
client.get_dialogs
client.get_participants
@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi')

@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def handler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await client.download_profile_photo(sender)
        await event.respond('Saved your photo {}'.format(sender.username))

client.iter_dialogs
client.start()
client.run_until_disconnected()
