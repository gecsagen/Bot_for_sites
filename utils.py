import fake_useragent
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from colorama import Fore, init
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import random

init()


def bot(url, flag_window=False, speed=0.075, how_page=3, flag_proxy=False):
    """Пролистает N статей на сайте 'url', а также все языковые копии этих страниц"""

    print(Fore.BLUE + f'Запускается процесс автоматизации на сайте: {url} ')
    url_copy = url

    # создаем объект настроек браузера
    option = webdriver.FirefoxOptions()

    #  проверяем нужно ли использовать прокси или нет
    if flag_proxy:
        #  считываем и получаем прокси из файла
        with open('proxy.txt') as proxy_file:
            list_proxy = proxy_file.readlines()
        proxy = random.choice(list_proxy).strip()
        proxy_split = proxy.split(':')
        port = int(proxy_split[1])
        ipaddress = f'{proxy_split[0]}'
        #  записываем прокси в настройки браузера
        option.set_preference('network.proxy.type', 1)  # прописваем тип прокси
        option.set_preference('network.proxy.socks', ipaddress.strip())  # прописваем прокси
        option.set_preference('network.proxy.socks_port', port)  # прописываем порт
        print(f'Прокси: {Fore.LIGHTWHITE_EX + proxy}')
    else:
        print(f'Запущен без прокси!')

    # записываем остальные настройки в браузер
    option.set_preference('dom.webdriver.enabled', False)  # убираем антидетект
    option.set_preference('dom.webnotifications.enabled', False)  # отключаем уведомлений
    option.set_preference('media.volume_scale', '0.0')  # отключаем звук
    user = fake_useragent.UserAgent().random  # создаем случайный useragent
    option.set_preference('general.useragent.override', user)  # записываем случайный useragent
    option.set_preference('media.peerconnection.enabled', False)  # отключаем webrtc
    option.headless = flag_window  # отключение окон браузера

    #  сохраняем настройки браузера
    browser = webdriver.Firefox(options=option)
    try:
        #  открываем главную страницу сайта
        browser.implicitly_wait(30)
        browser.get(url)

        #  сохраняем html код страницы
        time.sleep(3)
        scr = browser.page_source

        #  парсим все ссылки на статьи
        soup = BeautifulSoup(scr, 'lxml')
        urls_temp = soup.find_all('span', itemprop="headline")
        urls_results = []  # готовые ссылки на статьи
        for url in urls_temp:
            temp = url.find('a')
            urls_results.append(temp.get('href'))

        #  получаем доступные языки для перевода
        lang_results = []
        lang_list = soup.find_all('a', class_='nturl')
        for lang in lang_list:
            temp = lang.find('img')
            lang_results.append(temp.get("alt"))

        #  получаем сслыки на N необходимых статей
        new_urls = urls_results[:how_page]

        #  генериуем ссылки на все возможные языковые копии
        all_lang_urls = []
        for url_x in new_urls:
            all_lang_urls.append(url_x)
            url_split = url_x.split('/')
            for lang_x in lang_results:
                result = f"{'/'.join(url_split[:3])}/{lang_x}/{'/'.join(url_split[3:])}"
                all_lang_urls.append(result)

        #  печать промежуточных результатов
        print(Fore.BLUE + f'На сайте {url_copy} программа обойдет вот эти {how_page} статьи:')
        print(Fore.LIGHTBLUE_EX + f'{new_urls}')

        # делаем перходы на каждую страницу языковой копии
        for url in all_lang_urls:
            browser.implicitly_wait(10)
            browser.get(url)
            print(Fore.BLUE + f'Переходим на страницу -> {url}')

            #  листраем страницу вниз
            number_scrolls = 100
            while number_scrolls != 0:
                body = browser.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.DOWN)
                number_scrolls -= 1
                time.sleep(speed)
            print(Fore.GREEN + f'Страница {url} успешно пролистана')

        browser.quit()
        return None
    except Exception as ex:
        print(Fore.RED + f'Возникла ошибка: {ex}')
        browser.quit()
        return None
    finally:
        browser.quit()


if __name__ == '__main__':
    bot('https://detonic.shop/category/news', False, 0.075)
