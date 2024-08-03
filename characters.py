import time
import requests
from api import *

from logger import logger


def ping():
    url = "https://api.artifactsmmo.com"
    print_json(requests.get(url=url, headers={"Accept": "application/json"}).json())


def move(char: str, x: int, y: int):
    time.sleep(get_cooldown(char))
    url = get_url(char=char, action='move')
    response = requests.post(url, headers=headers, json={"x": x, "y": y})
    # print_json(response.json())


def execute_action(char, action):
    time.sleep(get_cooldown(char))
    url = get_url(char=char, action=action)
    # print(f"URL: {url}")
    response = requests.post(url, headers=headers)
    # print_json(response.json())

    if 'data' in response.json():
        # data = response.json()['data']
        # print(f"{char} successfully made {action}")
        logger.log(f"{char} successfully made {action}")
        coldown = get_cooldown(char)
        time.sleep(coldown)

        # if 'cooldown' in data:
        #     coldown = get_cooldown(char)
        #     print(f"{char} cooldown after {action}: {coldown} seconds")
        #     time.sleep(coldown)
        # else:
        #     print(f"URL: {url}")
        #     print_json(response.json())
        #     raise Exception("Cooldown not found")
    else:
        print_json(response.json())
        raise Exception("Bad request")


def give_command(char_name):
    chars_info = get_chars_info()
    for char_info in chars_info:
        if char_name == char_info['name']:
            char_target = chars[char_name]
            target_info = targets[char_target]

            if char_info['x'] != target_info[0] or char_info['y'] != target_info[1]:
                move(char_info['name'], target_info[0], target_info[1])
                logger.log(f"{char_info['name']} moved to {char_target}", 'debug')

            execute_action(char_name, target_info[2])


def deposit_items(char_info):
    place = 'Bank'
    bank_info = targets[place]
    if char_info['x'] != bank_info[0] or char_info['y'] != bank_info[1]:
        move(char_info['name'], bank_info[0], bank_info[1])
        logger.log(f"{char_info['name']} moved to {place}", 'debug')
    time.sleep(get_cooldown(char_info['name']))
    for item in char_info['inventory']:
        if item['code'] != "" and item['quantity'] > 0:
            time.sleep(get_cooldown(char_info['name']))
            url = get_url(char=char_info['name'], action=bank_info[2])
            params = {
                "code": f"{item['code']}",
                "quantity": item['quantity']
            }
            response = requests.post(url, headers=headers, json=params)
            logger.log(f"{char_info['name']} deposited {item['quantity']} {item['code']}")
            # print_json(response.json())
