import sys
import time
from colorama import Fore, init
from utils import bot
from multiprocessing import Pool, freeze_support

init()

#  блок считывания данных из файла настроек
try:
    with open('settings.txt') as settings_file:
        timer = int(settings_file.readline())  # таймер
        show_windows = settings_file.readline().strip()  # показвать окна браузера или нет
        speed = float(settings_file.readline().strip())  # скорость пролистывания
        how_page = int(settings_file.readline().strip())  # количество страниц
        flag_proxy = settings_file.readline().strip()  # использовать ли прокси
        url_list = [url.strip() for url in settings_file]  # список сайтов
    if show_windows == 'False':
        show_windows = False
    else:
        show_windows = True
    if flag_proxy == 'False':
        flag_proxy = False
    else:
        flag_proxy = True
except FileNotFoundError:
    print(
        Fore.RED + f'Пожалуйста создайте файл настроек {Fore.BLUE + "settings.txt"} '
                   f'{Fore.RED + "программа будет завершена"}')
    sys.exit(1)

#  заполняем аргументы для запуска функций в несколько процессов
args = [(str(url), show_windows, speed, how_page, flag_proxy) for url in url_list]

#  блок запуска программы
if __name__ == '__main__':
    freeze_support()
    while True:
        #  печать актуальных настроек
        print(Fore.CYAN + '<<<Запущена проверка поиска новых статей>>>')
        print(Fore.LIGHTWHITE_EX + '---------------')
        print(Fore.LIGHTWHITE_EX + 'Текущие настройки:')
        print(Fore.LIGHTWHITE_EX + f'Таймер -> {timer} минут')
        print(Fore.LIGHTWHITE_EX + f'Не показывать окна? -> {show_windows}')
        print(Fore.LIGHTWHITE_EX + f'Скорость пролиствания -> {speed}')
        print(Fore.LIGHTWHITE_EX + f'Количество страниц для обхода -> {how_page}')
        print(Fore.LIGHTWHITE_EX + f'Использовать ли прокси? -> {flag_proxy}')
        print(Fore.LIGHTWHITE_EX + f'URL адреса -> {url_list}')
        print(Fore.LIGHTWHITE_EX + '---------------')
        #  запускаем
        with Pool(processes=len(url_list)) as p:
            p.starmap(bot, args)
        time.sleep(timer * 60)
