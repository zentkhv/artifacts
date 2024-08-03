import json
from pygments import highlight, lexers, formatters
import pytz
from datetime import datetime, timedelta
import requests

from credentials import token
from logger import logger

timezone = pytz.timezone('Asia/Vladivostok')

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

# chars = {  # fight gathering
#     'Zent': 'gathering',
#     'MKS': 'gathering',
#     'Markiz': 'gathering',
#     'Belka': 'gathering',
#     'Witcher': 'gathering'
# }

chars = {  # fight gathering
    # 'Zent': 'Cooper Rocks',
    'MKS': 'Cooper Rocks',
    'Markiz': 'Cooper Rocks',
    'Belka': 'Cooper Rocks',
    'Witcher': 'Chicken'
}

targets = {
    'Bank': [4, 1, 'bank/deposit'],
    'Ash Tree': [-1, 0, 'gathering'],
    'Cooper Rocks': [2, 0, 'gathering'],
    'Chicken': [0, 1, 'fight'],
    'Green Slime': [0, -1, 'fight'],
    'Red Slime': [1, -1, 'fight'],
    'Blue Slime': [2, -1, 'fight'],
    'Yellow Slime': [1, -2, 'fight']
}


def print_json(data):
    # json_obj = json.loads(data)
    formatted_json_str = json.dumps(data, indent=2, sort_keys=True)
    highlighted_json = highlight(formatted_json_str, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(highlighted_json)


def get_url(char: str, action: str):
    # if char == "characters":
    #     return f"https://api.artifactsmmo.com/my/{char}"
    return f"https://api.artifactsmmo.com/my/{char}/action/{action}"


def get_chars_info():
    url = "https://api.artifactsmmo.com/my/characters"
    response = requests.get(url=url, headers=headers).json()
    return response['data']


def get_char_info(char_name: str):
    data = get_chars_info()
    for character in data:
        if character['name'] == char_name:
            return character


def get_cooldown(char_name: str):
    chars_data = get_chars_info()
    for char in chars_data:
        if char['name'] == char_name:
            cooldown = calculate_cooldown(char['cooldown_expiration'])
            if cooldown > 0:
                # print(f"{char_name} on cooldown: {cooldown} seconds")
                logger.log(f"{char_name} on cooldown: {cooldown} seconds", 'warning')
            return cooldown


def calculate_cooldown(exparation_datetime):  # Метод определения отката
    exparation_datetime = datetime.fromisoformat(exparation_datetime.replace("Z", "+00:00"))  # Форматируем таймзону
    current_time_vladivostok = datetime.now(timezone)  # Берем текущее время
    input_time_vladivostok = exparation_datetime.astimezone(timezone)  # Переводим время в нужную таймзону
    time_difference = input_time_vladivostok - current_time_vladivostok  # Вычисляем разницу
    time_difference_seconds = time_difference.total_seconds()  # Вычисляем разницу в секундах
    time_difference_seconds = int(time_difference_seconds)  # Приводим float в int
    if time_difference_seconds < 0:
        return 0
    else:
        return time_difference_seconds
