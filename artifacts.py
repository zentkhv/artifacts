# Библиотеки
import time
import threading
import requests
import json
from pygments import highlight, lexers, formatters
from datetime import datetime, timedelta
import pytz

# Локальные скрипты
import credentials


# Глобальные объекты
vladivostok_tz = pytz.timezone('Asia/Vladivostok')
token = credentials.token

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

chars = {  # fight gathering
    # 'Zent': 'gathering',
    'MKS': 'gathering',
    'Markiz': 'gathering',
    'Belka': 'gathering',
    'Witcher': 'gathering'
}

places = {
    'Bank': [4, 1, 'bank/deposit'],
    'Ash Tree': [-1, 0, 'gathering'],
    'Cooper Rocks': [2, 0, 'gathering']
}


# Методы
def get_url(char: str, action: str):
    # if char == "characters":
    #     return f"https://api.artifactsmmo.com/my/{char}"
    return f"https://api.artifactsmmo.com/my/{char}/action/{action}"


def get_cooldown(char_name: str):
    chars_data = chars_info()
    for char in chars_data:
        if char['name'] == char_name:
            cd = calculate_cooldown(char['cooldown_expiration'])
            if cd > 0:
                print(f"{char_name} on cooldown: {cd} seconds")
            return cd


def calculate_cooldown(exparation_datetime):  # Метод определения отката
    exparation_datetime = datetime.fromisoformat(exparation_datetime.replace("Z", "+00:00"))  # Форматируем таймзону
    current_time_vladivostok = datetime.now(vladivostok_tz)  # Берем текущее время
    input_time_vladivostok = exparation_datetime.astimezone(vladivostok_tz)  # Переводим время в нужную таймзону
    time_difference = input_time_vladivostok - current_time_vladivostok  # Вычисляем разницу
    time_difference_seconds = time_difference.total_seconds()  # Вычисляем разницу в секундах
    time_difference_seconds = int(time_difference_seconds)  # Приводим float в int
    if time_difference_seconds < 0:
        return 0
    else:
        return time_difference_seconds


def print_json(data):
    # json_obj = json.loads(data)
    formatted_json_str = json.dumps(data, indent=2, sort_keys=True)
    highlighted_json = highlight(formatted_json_str, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(highlighted_json)


def ping():
    url = "https://api.artifactsmmo.com"
    print_json(requests.get(url=url, headers={"Accept": "application/json"}).json())


def chars_info():
    url = "https://api.artifactsmmo.com/my/characters"
    response = requests.get(url=url, headers=headers).json()
    return response['data']


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
        print(f"{char} successfully made {action}")
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


def deposit_items(char_info):
    bank_info = places['Bank']
    if char_info['x'] != bank_info[0] or char_info['y'] != bank_info[1]:
        move(char_info['name'], bank_info[0], bank_info[1])
        print(f"{char_info['name']} moved to bank")
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
            print(f"{char_info['name']} deposited {item['quantity']} {item['code']}")
            # print_json(response.json())


def work_loop(char, action):
    while True:
        execute_action(char, action)


if __name__ == "__main__":
    # ping()
    # print()

    # move("Zent", 1, 1)

    # WORK LOOP
    for character in chars.keys():
        thread = threading.Thread(target=work_loop, args=(character, chars[character]))
        thread.start()

    # DEPOSIT ITEMS
    # for character in chars_info():
    #     thread = threading.Thread(target=deposit_items, args=(character,))
    #     thread.start()

    # threads = []
    # for character in chars.keys():
    #     thread = threading.Thread(target=work_loop, args=(character, chars[character]))
    #     threads.append(thread)
    #     thread.start()

    # for thread in threads:  # Ожидание завершения всех потоков
    #     thread.join()
