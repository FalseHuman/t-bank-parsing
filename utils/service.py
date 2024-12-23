import os
import time
import json
import math
import requests
from utils.func_api import get_stocks, get_total_stocks
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def get_list_paginate(_list: list, url: str, type_='stocks') -> list:
    calculate_page_parsing_stocks = math.ceil(get_total_stocks(url=url) / 12)
    list_page = []
    for i in range(0, calculate_page_parsing_stocks*12+1, 12):
        list_page.append(i)

    while len(list_page)!=1:
        start = list_page.pop(0)
        end = list_page[0]
        _list.append(get_stocks(start, end, url=url, type_=type_))

    return _list


def download_image(url: str, ticker: str):
    img_data = requests.get(url).content
    with open(f'images/{ticker}.jpg', 'wb') as handler:
        handler.write(img_data)


def dump_image(url: str, ticker: str):
    try:
        download_image(url, ticker)
    except FileNotFoundError:
        os.mkdir('images')
        download_image(url, ticker)


def get_sector(list_sector: list, code:str) -> str:
    for eng_sector in list_sector:
        if eng_sector.get('eng') == code:
            return eng_sector.get('rus', '')
    return None


def group_by_sector(stocks_list: list, group_by_list: dict) -> list:
    for stock in stocks_list:
        for sector in group_by_list['sectors']:
            if stock['sector']['eng'] in sector.keys():
                if stock['sector']['eng'] not in  sector[list(sector.keys())[0]]:
                    sector[list(sector.keys())[0]].append(stock)

    return group_by_list


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def save_file(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def dump_json(data, file:str):
    try:
        save_file(data, file)
    except FileNotFoundError:
        os.mkdir('json')
        save_file(data, file)


def wait_load_page(second: int):
    time.sleep(second)


def create_driver():
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--v=99")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    return driver