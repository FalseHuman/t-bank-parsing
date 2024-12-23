import requests
from utils.settings import params, cookies,headers


def get_info_req(start: int, end: int, url: str)->list:
    json_data = {
        'start': start,
        'end': end,
        'orderType': 'Desc',
        'sortType': 'ByPopularity',
        'countryOfRisk': 'RU',
        'country': 'All',
        'isPrivate': False,
        'filterOTC': False,
    }

    response = requests.post(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response.json()


def get_total_stocks(url: str):
    '''
    Получаем количество объектов (число)
    '''
    response = get_info_req(start=0,end=12, url=url)
    return response.get('payload', {}).get('total', 0)


def get_stocks(start: int, end: int, url: str, type_='stocks')->list:
    '''
    Получаем список объектов
    '''
    response = get_info_req(start=start,end=end, url=url)

    if type_ == 'stocks':
        symbols = [res.get('symbol', {}) for res in response.get('payload', {}).get('values', [])]
    else:
        symbols = response
    return symbols

def get_brand_info(brand: str) -> dict:
    '''
    Получаем информацию о компании
    '''
    json_data = {
        'brandId': brand,
    }

    response = requests.post(
        'https://www.tbank.ru/api/trading/symbols/brands',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response.json()


def get_list_countries() -> list:
    '''
    Получаем информацию о стране (код, название на русском)
    '''
    response = requests.post('https://www.tbank.ru/api/trading/symbols/countries', params=params, cookies=cookies, headers=headers)
    return response.json()


def get_list_sector(type_: str='stocks') -> list:
    '''
    Получаем информацию о секторе (код, название на русском)
    '''
    response = requests.post(f'https://www.tbank.ru/api/trading/{type_}/sectors', params=params, cookies=cookies, headers=headers)
    return response.json()


def get_parameters_stock(ticker: str, type_:str) -> dict:
    '''
    Получаем информацию о об объекте (по тикеру и типу - фонд, акция, фьючерс, облигация)
    '''
    json_data = {
        'ticker': ticker,
    }

    response = requests.post(
        f'https://www.tbank.ru/api/trading/{type_}/get',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response.json()


def get_info(url: str, params_get: dict=None) -> dict:
    '''
    Получаем информацию о об объекте по ссылке и параметрам
    '''
    if params_get is not None:
        params.update(**params_get)
    response = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    if params_get is not None:
        for key in params_get.keys():
            del params[key]
    return response.json()