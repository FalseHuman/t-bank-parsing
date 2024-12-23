import math
from utils.service import dump_json, wait_load_page, create_driver, dump_image, get_sector, get_list_paginate
from utils.func_api import get_stocks, get_total_stocks, get_brand_info,\
                     get_list_sector, get_parameters_stock, get_info
from selenium.common.exceptions import NoSuchElementException



def get_list_stocks_paginate(stoks_symbol_list: list) -> list:
    return get_list_paginate(_list=stoks_symbol_list, url='https://www.tbank.ru/api/trading/stocks/list')


def parsing_api(stoks_symbol_list: list, list_sector: list, stocks_list: list=[]) -> list:
    print('parsing api start')
    for stocks in stoks_symbol_list:
        for stock in stocks:
            brand = stock.get('brand', '')
            brand_info = get_brand_info(brand=brand).get('payload', '').get('brands', [])[0]
            description = brand_info.get('brandInfo', '')
            logoBaseColor = brand_info.get('logoBaseColor', '')
            sector = brand_info.get('sector', '')
            sector_show_name = get_sector(list_sector=list_sector, code=sector)
            country = 'Россия'
            main_link = brand_info.get('externalLinks', {}).get('main', None)
            ticker = stock.get('ticker', '')
            exchangeShowName = stock.get('exchangeShowName', '')
            parameters_stock = get_parameters_stock(ticker=ticker, type_='stocks').get('payload', {})
            # параметры бумаги
            parameters_ticker = ticker
            bcsClassCode = parameters_stock.get('symbol', {}).get('bcsClassCode', None)
            lot_size = parameters_stock.get('symbol', {}).get('lotSize', None)
            qualInvestorFlag = parameters_stock.get('symbol', {}).get('qualInvestorFlag', None)
            isin = parameters_stock.get('symbol', {}).get('isin', None)
            currency = parameters_stock.get('symbol', {}).get('currency', None)

            # Торговые данные
            auction = parameters_stock.get('prices', {}).get('auction', None)
            close = parameters_stock.get('prices', {}).get('close', None)
            # earningsInfo = parameters_stock.get('historicalPrices', [''])[0]

            # Дивиденды
            dividends = get_info(url=f'https://www.tbank.ru/api/invest-gw/invest-calendar/event/{ticker}/dividends').get('payload', {})

            logo = 'https://invest-brands.cdn-tinkoff.ru/'+ stock.get('logoName', '').replace('.png', 'x160.png')
            show_name = stock.get('showName', '')
            stock_info = {'brand': brand, 'ticker': ticker, 'logo': logo, 'showName': show_name, 'description': description,}
            stock_info['country'] = country
            stock_info['link'] = main_link
            stock_info['logoBaseColor'] = logoBaseColor
            stock_info['sectorId'] = sector
            stock_info['sectorName'] =  sector_show_name
            stock_info['exchangeShowName'] = exchangeShowName


            stock_info['parametersStock'] = {}
            stock_info['parametersStock']['parametersTicker'] = parameters_ticker
            stock_info['parametersStock']['bcsClassCode'] = bcsClassCode 
            stock_info['parametersStock']['lotSize'] = lot_size
            stock_info['parametersStock']['qualInvestorFlag'] = qualInvestorFlag
            stock_info['parametersStock']['isin'] = isin
            stock_info['parametersStock']['currency'] = currency

            stock_info['tradingData'] = {}
            stock_info['tradingData']['auction'] = auction
            stock_info['tradingData']['close'] = close
            stock_info['dividends'] = dividends.get('dividends', [])
            # stock_info['trading_data']['earningsInfo'] = earningsInfo

            dump_image(url=logo, ticker=ticker)
            stocks_list.append(stock_info)
    print('parsing api end')
    return stocks_list

# start parsing selenium
def parsing_selenium(stocks_list: list) -> list:
    i = 0
    print('parsing selenium start')
    for i, stock in enumerate(stocks_list):
        i+=1
        message = f"{i}/{len(stocks_list)} - {stock['ticker']}"
        print(message)
        driver = create_driver()
        driver.get('https://www.tbank.ru/invest/stocks/'+ stock['ticker'])
        wait_load_page(5)
        div_percent = driver.find_element('xpath', ".//div[@data-qa-file='SecurityHeader']")
        try:
            span = div_percent.find_element('xpath', ".//span[@data-qa-file='Money']")
            stock['halfYearProfitability'] = span.text.replace('\n', '') + '%'
        except NoSuchElementException:
            stock['halfYearProfitability'] = None
        table_summary  = driver.find_element('xpath', ".//tbody[@data-qa-file='SecuritySummary']")
        table_cells = table_summary.find_elements('xpath', ".//td[@data-qa-file='TableCell']")
        traiding_data = [table_cell.text.replace('\n', '') for table_cell in table_cells]
        stock['tradingData']['dailyChange'] = traiding_data[traiding_data.index('Дневной диапазон') + 1]
        stock['tradingData']['percentDay'] = traiding_data[traiding_data.index('Изменение за день') + 1]
        stock['tradingData']['percenYear'] = traiding_data[traiding_data.index('Изменение за год') + 1]
        stock['tradingData']['yearChange'] = traiding_data[traiding_data.index('Годовой диапазон') + 1]
        driver.close()
    print('parsing selenium end')
    return stocks_list



def start_parsing_stocks():
    list_sector = get_list_sector().get('payload',{}).get('sectors', [])
    stoks_symbol_list, stocks_list = [], []
    group_by_list = {}
    
    # for sector in list_sector:
    #     group_by_list['sectors'].append({sector['eng']: []})

    stoks_symbol_list = get_list_stocks_paginate(stoks_symbol_list)
    stocks_list = parsing_api(stoks_symbol_list=stoks_symbol_list, stocks_list=stocks_list, list_sector=list_sector)
    stocks_list = parsing_selenium(stocks_list=stocks_list)
    
    group_by_list = stocks_list
    dump_json(group_by_list, file='json/stocks.json')


if __name__ == '__main__':
    start_parsing_stocks()