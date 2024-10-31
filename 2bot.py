import telethon
from telethon import TelegramClient, events

from decouple import Config, RepositoryEnv

# задаём расположение .env файла
DOTENV_FILE = './.env'

# загружаем переменные окружения из .env файла
dotenv_config =  Config(RepositoryEnv(DOTENV_FILE))

# BOOT_TOKEN, APP_SESSION, 
# APP_API_ID, APP_API_HASH,
# APP_TITLE, SHRT_NAME
# TEL





bot_token = dotenv_config('BOOT_TOKEN')
api_id = dotenv_config('APP_API_ID')
api_hash = dotenv_config('APP_API_HASH')

bot = TelegramClient('bot', api_hash=api_hash, api_id=api_id)
bot.start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    print(event.stringify())
    
    await event.reply('Lalala lalala lalalala lala')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo_all(event):
    await event.reply(f'bot echo... {event.text}')
    # event.s


bot.run_until_disconnected()