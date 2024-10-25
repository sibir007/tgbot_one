from decouple import Config, RepositoryEnv
import asyncio
import telegram


# задаём расположение .env файла
DOTENV_FILE = './.env'

# загружаем переменные окружения из .env файла
dotenv_config =  Config(RepositoryEnv(DOTENV_FILE))

async def main():
    bot = telegram.Bot(dotenv_config('TOKEN'))
    async with bot:
        print( await bot.get_me())


if __name__ == '__main__':
    # print(dotenv_config('TOKEN'))
    asyncio.run(main())
    
    'https://api.telegram.org/bot8106302607:AAF_FBkry4LeZHv7CG60gzonmuJUo3Yv8oU/getMe'