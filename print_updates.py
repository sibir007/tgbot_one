#!/usr/bin/env python3
# A simple script to print all updates received.
# Import modules to access environment, sleep, write to stderr
import os
import sys
import time
import tg_util
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Import the client
from telethon import TelegramClient

# os.e

# This is a helper method to access environment variables or
# prompt the user to type them in the terminal if missing.
def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


# Define some variables so the code reads easier
session = os.environ.get('APP_SESSION', 'printer')
api_id = get_env('APP_API_ID', 'Enter your API ID: ', int)
api_hash = get_env('APP_API_HASH', 'Enter your API hash: ')
bot_token = get_env('BOOT_TOKEN', 'Enter your BOOT TOKEN: ')
proxy = ('http', 'proxy', 3128, False, 'SibiryakovDO', 'vzlsoFia1302')
# proxy = None if not tg_util.domain_is_vzljot() else get_env('VZL_PROXY', 'Enter your VZLJOT PROXY: ') 


# This is our update handler. It is called when a new update arrives.
async def handler(update):
    print(update)


# Use the client in a `with` block. It calls `start/disconnect` automatically.
with TelegramClient(session, api_id, api_hash, proxy=proxy) as client:
    # Register the update handler so that it gets called
    client.add_event_handler(handler)

    # Run the client until Ctrl+C is pressed, or the client disconnects
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
