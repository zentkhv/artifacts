# Библиотеки
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Локальные скрипты
from api import *
from characters import *


# Глобальные объекты


# Методы
def work_loop(char):
    while True:
        give_command(char)


if __name__ == "__main__":
    # ping()
    print()

    # move("Zent", 1, 1)

    # WORK LOOP
    # with ThreadPoolExecutor(max_workers=20) as executor:
    #     for character in chars.keys():
    #         executor.submit(work_loop, character)

    threads = []
    for character in chars.keys():
        thread = threading.Thread(target=work_loop, args=(character,))
        threads.append(thread)
        thread.start()
        print(f"{character} started")

    # DEPOSIT ITEMS
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     for character in get_chars_info():
    #         executor.submit(deposit_items, character)

    # for thread in threads:  # Ожидание завершения всех потоков
    #     thread.join()
