import math
from utils.service import dump_json, dump_image
from utils.func_api import get_total_stocks, get_parameters_stock, get_info_req


def get_list_futures_paginate(stoks_symbol_list: list) -> list:
    calculate_page_parsing_stocks = math.ceil(get_total_stocks(url='https://www.tbank.ru/api/trading/futures/list') / 12)
    list_page = []
    for i in range(0, calculate_page_parsing_stocks*12+1, 12):
        list_page.append(i)

    while len(list_page)!=1:
        start = list_page.pop(0)
        end = list_page[0]
        stoks_symbol_list.append(get_info_req(start, end, url='https://www.tbank.ru/api/trading/futures/list'))

    return stoks_symbol_list

def parsing_api(futures_symbol_list: list, futures_list: list=[]) -> list:
    print('start parsing api')
    futures_symbol_list = [res.get('payload', {}).get('values', []) for res in futures_symbol_list]
    for futures in futures_symbol_list:
        for future in futures:
            viewInfo = future.get('viewInfo', {})
            earningsInfo = future.get('earningsInfo', {})
            instrumentInfo = future.get('instrumentInfo', {})
            priceInfo = future.get('priceInfo', {})
            brand = viewInfo.get('brand', None)
            color = viewInfo.get('color', None)

            ticker = instrumentInfo.get('ticker', None)
            orderInfo = get_parameters_stock(ticker=ticker, type_='futures').get('payload', {}).get('orderInfo', {})
            basicAsset =instrumentInfo.get('basicAsset', None)
            firstTradeDate = instrumentInfo.get('firstTradeDate', None)
            lastTradeDate = instrumentInfo.get('lastTradeDate', None)
            daysTillLastTrade = instrumentInfo.get('daysTillLastTrade', None)
            basicAssetSize = instrumentInfo.get('daysTillLastTrade', None)
            futuresType = instrumentInfo.get('futuresType', None)

            initialMargin = orderInfo.get('initialMargin', None)
            pointValue = orderInfo.get('pointValue', None)
            priceInCurrency = orderInfo.get('priceInCurrency', None)

            price = priceInfo.get('buy', None)
            basicAssetBrandDescription = instrumentInfo.get('basicAssetBrandDescription', None)
            classCode = instrumentInfo.get('classCode', None)
            logo = 'https://invest-brands.cdn-tinkoff.ru/'+ viewInfo.get('logoName', '').replace('.png', 'x160.png')
            
            futures_info = {'brand': brand, 'color': color, 'ticker': ticker, 'logo': logo}
            futures_info['price'] = price
            futures_info['firstTradeDate'] = firstTradeDate
            futures_info['lastTradeDate'] = lastTradeDate
            futures_info['daysTillLastTrade'] = daysTillLastTrade
            futures_info['basicAssetBrandDescription'] = basicAssetBrandDescription
            futures_info['classCode'] = classCode
            futures_info['earningsInfo'] = earningsInfo
            futures_info['basicAsset'] = basicAsset
            futures_info['basicAssetSize'] = basicAssetSize
            futures_info['futuresType'] =  futuresType

            futures_info['initialMargin'] = initialMargin
            futures_info['pointValue'] = pointValue
            futures_info['priceInCurrency'] =  priceInCurrency
            dump_image(url=logo, ticker=ticker)
            futures_list.append(futures_info)
    print('end parsing api')
    return futures_list


def start_parsing_futures():
    group_by_list = {}
    
    futures_symbol_list = get_list_futures_paginate([])
    futures_list = parsing_api(futures_symbol_list=futures_symbol_list, futures_list=[])


    group_by_list = futures_list
    # print(group_by_list)
    dump_json(group_by_list, file='json/futures.json')

if __name__ == '__main__':
    start_parsing_futures()