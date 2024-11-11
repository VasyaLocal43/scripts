import argparse
import re
import requests
from urllib.parse import urljoin

def arg_pars():
    parser = argparse.ArgumentParser(description="Extract all links from the specified webpage.")
    parser.add_argument("-u", "--url", default='https://kali.org', dest='urlPars', help="URL to extract links from")
    options = parser.parse_args()
    return options

def find_links(url):
    try:
        # Проверяем, содержит ли URL схему (http или https)
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Выполняем запрос к указанному URL
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()  # Проверка на HTTP-ошибки

        # Ищем все ссылки на странице
        links = re.findall(r'href=["\'](.*?)["\']', resp.text)
        # Преобразуем относительные ссылки в абсолютные
        absolute_links = [urljoin(url, link) for link in links]
        return absolute_links
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return []

# Получаем URL из аргументов командной строки
url = arg_pars().urlPars
href_find = find_links(url)

# Печатаем найденные ссылки
if href_find:
    for link in href_find:
        print(link)
else:
    print("No links found or an error occurred.")
