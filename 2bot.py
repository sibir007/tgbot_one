from http import client
import os
import asyncio
from telethon import TelegramClient, events, Button
from telethon import functions, types
from telethon.events.common import EventCommon
import re
from telethon.tl.custom.message import Message
from decouple import Config, RepositoryEnv

import logging
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(format="[%(levelname) %(asctime)s] %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

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


bot_commands = [
                types.BotCommand(
                    command='start',
                    description='start bot conversation'
                ),
                types.BotCommand(
                    command='help',
                    description='returns a help message, like a short text about what your bot can do and a list of commands'
                ),
                types.BotCommand(
                    command='settings',
                    description="shows the bot's settings for this user and suggests commands to edit them."
                ),
                types.BotCommand(
                    command='ping',
                    description="ping-pong"
                ),
            ]

# bc = types.BotCommand(
#     command='quiz',
#     description="simple quiz"
# )
# bc.command

def get_set_bot_commands_request(bot_commands: list[types.BotCommand]) -> functions.bots.SetBotCommandsRequest:

    return functions.bots.SetBotCommandsRequest(
            scope=types.BotCommandScopeDefault(),
            lang_code='en',
            commands=bot_commands
    )

async def set_all_bot_commands(bot):
    
    request = get_set_bot_commands_request(bot_commands) 
    result = await bot(request)
    return result
    
async def deleted_message(bot: TelegramClient, chat_id, message: str, sek_delay: float):
    msg: Message = await bot.send_message(chat_id, message=message)
    await asyncio.sleep(sek_delay)
    await msg.delete()


# def init_not_deleted_message_command(bot):
#     not_deleted_mes = 'This is not deleted msg'

#     bot_commands.append(
#                 types.BotCommand(
#                     command='not_deleted_message',
#                     description="test create non deleted msg"
#                 ))
#     msgs = []
#     bot.on(events.NewMessage(pattern='/not_deleted_message'))
#     async def handler(event):
        
    

def init_mes_edit_command(bot):
    resp_mes = """
    Edit me command response:
    ```
    git clone https://github.com/SharzyL/tg_searcher.git telethon_examples2/
    ```\n
    **This is bold**\n
    __This is italic__
    """
    
    msgs = []
    
    @bot.on(events.NewMessage(pattern='/edit_me'))
    async def register_edit_me_messages(event):
        msgs.append(event.id)
        raise events.StopPropagation()
    
    @bot.on(events.MessageEdited(func=lambda m: m.id in msgs))
    async def handle(event):
        resp = await event.respond(resp_mes)
        await asyncio.sleep(5)
        msgs.remove(event.id)
        await event.delete()
        await resp.delete()
        raise events.StopPropagation()

    bot_commands.append(
                types.BotCommand(
                    command='edit_me',
                    description="test events.MessageEdited"
                ))
    
# test keybords
def init_keybords_command(bot):
    resp_msg = """
    **keybord buttons**:\n
    **text** - send text;\n
    **loc** - request location;\n
    **ph** - request phone;\n
    **poll** - request poll;\n
    **poll_q** - request poll;\n
    **clear_all** - clear all mes
    """
    bot_commands.append(
        types.BotCommand(
            command='get_keybord',
            description='test keybords buttons'
        ))
    bot_commands.append(
        types.BotCommand(
            command='clear_keybord',
            description='clear keybord'
        ))
    
    
    @bot.on(events.NewMessage(pattern='/get_keybord'))
    async def handler(event: EventCommon):
        # print(event)
        await event.respond(resp_msg, buttons=[
            [Button.text('text')],
            [
                Button.request_location('loc'),
                Button.request_phone('ph'),                
            ],
            [
                Button.request_poll('poll'),
                Button.request_poll('poll_q', force_quiz=False),
            ],
            # [Button.text('/clear_all')]
        ])
        raise events.StopPropagation()
        
    @bot.on(events.NewMessage(pattern='/clear_keybord'))
    async def handler(event: EventCommon):
        await event.respond("clear keybord", buttons=Button.clear())
        raise events.StopPropagation()

    # @bot.on(events.NewMessage(pattern='/clear_all'))
    # async def handler(event: EventCommon):
    #     async for message in event.client.iter_messages(event.chat_id, ):
    #         await message.delete()
    #     raise events.StopPropagation()



# test inline button
def init_quiz_command(bot):
    # {
    #     chat_id = [mes1.id, mes2.id, mes3.id, ...],
    #     ...,
    #     ...,
    # }
    quiz_context = {}
    @bot.on(events.NewMessage(pattern='/quiz'))
    async def simple_quiz(event: EventCommon):
        
        # если в quiz_context существует event.chat_id key
        # значит предыдущий /quiz не закончен, в этом случае
        # сначала нужно закончить его
        if event.chat_id in quiz_context:
            await deleted_message(
                bot, 
                event.chat_id, 
                'закончите предыдущий quiz',
                3)
            await event.delete()
            raise events.StopPropagation()
              
        msg: Message = await event.reply(
            'Yes or no?', 
            buttons=[
                [Button.inline('Yes!', b'quiz_yes')], 
                [Button.inline('Nope', b'quiz_no')]
            ]
        )
        
        msg_list: list = [event.id, msg.id]
        # quiz_context.get(event.chat_id, [])
        # msg_list.extend()
        quiz_context[event.chat_id] = msg_list
        # await remove_bot_commands(bot)
        # await set_bot_commands_from_quiz(bot)
        raise events.StopPropagation()

    @bot.on(events.CallbackQuery(data=re.compile(b'quiz_')))
    async def quiz_check(event: EventCommon):
        if event.data == b'quiz_yes':
            msg = await event.answer('Correct answer!', alert=True)
            await bot.delete_messages(event.chat_id, quiz_context[event.chat_id])
            del quiz_context[event.chat_id]
            # quiz_context[event.chat_id].append(msg.id)
        elif event.data == b'quiz_no':
            msg = await event.answer('Wrong answer!', alert=True)
            # quiz_context[event.chat_id].append(msg.id)
        else:
            msg = await event.answer('Ничего не подходит!', alert=True)
            # quiz_context[event.chat_id].append(msg.id)
        raise events.StopPropagation()
    
    bot_commands.append(
                types.BotCommand(
                    command='quiz',
                    description="test Button.inline"
                ))
            
    


async def main():
    
    if os.environ.get('USERDOMAIN', '') == 'VZLJOT':
        proxy_setings = [
            dotenv_config('VZL_PROXY_PROTOCOL'),
            dotenv_config('VZL_PROXY_HOST'),
            int(dotenv_config('VZL_PROXY_PORT')),
            dotenv_config('VZL_PROXY_LOGIN'),
            dotenv_config('VZL_PROXY_PASSWORD'),
        ]
        bot = TelegramClient('bot', api_hash=api_hash, api_id=api_id, proxy=proxy_setings)
    else:
        bot = TelegramClient('bot', api_hash=api_hash, api_id=api_id)
        
        


    await bot.start(bot_token=bot_token)

    init_quiz_command(bot)
    
    init_mes_edit_command(bot)
    
    init_keybords_command(bot)

    @bot.on(events.MessageEdited)
    async def message_edited_handler(event):
        print('Message', event.id, 'changed at', event.date)

    # @bot.on(events.UserUpdate)
    # async def user_update_handler(event):
    #     print(event.stringify())

    @bot.on(events.NewMessage(pattern='/start'))
    async def send_welcome(event: EventCommon):
        await event.reply('Lalala lalala lalalala lala')
        raise events.StopPropagation()


    # @bot.on(events.NewMessage)
    async def echo_all(event):
        await event.reply(f'bot echo... {event.text}')
        # event.s
        raise events.StopPropagation()
    
    # @bot.on(events.NewMessage(outgoing=True, pattern='!ping'))
    @bot.on(events.NewMessage(pattern='/ping'))
    async def pong(event: EventCommon):
        user = await event.get_chat()
        logger.info(f'user {user}')
        mes = await event.reply('!pong')
        await asyncio.sleep(5)
        await bot.delete_messages(event.chat_id, [event.id, mes.id])
        raise events.StopPropagation()

    await set_all_bot_commands(bot)

    try:

        await bot.run_until_disconnected()
    finally:
        await bot.disconnect()
        

if __name__ == '__main__':
    asyncio.run(main())



