import os

import tg_util
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def print_environ():
    for item in os.environ.items():
        print(item)

def domain_is_vzljot():
    user_domain: str = os.environ.get('USERDOMAIN', '')
    if 'VZLJOT' == user_domain:
        return True
    return False

if __name__ == '__main__':
    # print_environ()
    print(domain_is_vzljot())