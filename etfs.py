import math
from utils.service import dump_json, diff_month, get_sector, dump_image, get_list_paginate
from utils.func_api import get_total_stocks, get_stocks, get_brand_info, get_info, get_parameters_stock, get_list_sector
from datetime import datetime



def get_list_efts_paginate(etfs_symbol_list: list) -> list:
    return get_list_paginate(_list=etfs_symbol_list, url='https://www.tbank.ru/api/trading/etfs/list')

def parsing_api(efts_symbol_list: list, list_sector: list, efts_list: list=[]) -> list:
    print('start parsing api')
    for efts in efts_symbol_list:
        for eft in efts:
            brand = eft.get('brand', '')
            try:
                brand_info = get_brand_info(brand=brand).get('payload', '').get('brands', [])[0]
            except IndexError:
                brand_info = get_brand_info(brand=brand).get('payload', '').get('brands', {})
            ticker = eft.get('ticker', '')
            exchangeShowName = eft.get('exchangeShowName', '')
            overview = get_info(url=f'https://www.tbank.ru/api/invest-gw/fireg-advisory/api/web/v2/etf/positions/{ticker}/overview', params_get={'idKind': 'ticker'})
            parameters_stock = get_parameters_stock(ticker=ticker, type_='etfs').get('payload', {})
            # параметры бумаги
            parameters_ticker = ticker
            bcsClassCode = parameters_stock.get('symbol', {}).get('bcsClassCode', None)
            lot_size = parameters_stock.get('symbol', {}).get('lotSize', None)
            qualInvestorFlag = parameters_stock.get('symbol', {}).get('tradeQualInvestor', None)
            isin = parameters_stock.get('symbol', {}).get('isin', None)
            currency = parameters_stock.get('symbol', {}).get('currency', None)
            price = parameters_stock.get('price', None)
            indexDescription = overview.get('detail', {}).get('indexDescription', None)
            structure = overview.get('detail', {}).get('structure', [])
            advantages = overview.get('detail', {}).get('advantages', [])
            timeline = overview.get('detail', {}).get('netAsset', {}).get('timeline', [])
            lastCountMonth = 0
            sumEtf = 0
            percentMonth = 0
            if timeline != []:
                start_date, end_date = datetime.strptime(timeline[0]['d'], '%Y-%m-%d'), datetime.strptime(timeline[-1]['d'], '%Y-%m-%d')
                lastCountMonth = diff_month(end_date, start_date)
                sumEtf = timeline[-1]['v']
                percentMonth = 100 - (timeline[0]['v'] * 100) / timeline[-1]['v']
                # print(start_date, end_date, timeline[-1]['v'])
            # print(overview)
            if brand_info != []:
                description = brand_info.get('brandInfo', '')
                main_link = brand_info.get('externalLinks', {}).get('main', None)
                logoBaseColor = brand_info.get('logoBaseColor', '')
                sector = brand_info.get('sector', '')
            else:
                description = overview.get('description', '')
                logoBaseColor = eft.get('textColor', '')
                sector = eft.get('sector','')
                main_link = None

            sector_show_name = get_sector(list_sector=list_sector, code=sector)
            logo = 'https://invest-brands.cdn-tinkoff.ru/'+ eft.get('logoName', '').replace('.png', 'x160.png')
            show_name = eft.get('showName', '')
            country = 'Россия'
            eft_info = {'brand': brand, 'ticker': ticker, 'logo': logo, 'showName': show_name, 'description': description}
            eft_info['country'] = country
            eft_info['link'] = main_link
            eft_info['exchangeShowName']=exchangeShowName
            eft_info['price'] = price
            eft_info['logoBaseColor'] = logoBaseColor
            eft_info['sectorId'] = sector
            eft_info['sectorName'] =  sector_show_name
            eft_info['indexDescription'] = indexDescription 
            eft_info['structure'] = structure
            eft_info['advantages'] = advantages
            eft_info['lastCountMonth'] = lastCountMonth
            eft_info['sumEtf'] = sumEtf
            eft_info['percentMonth'] = percentMonth
            # print(brand, brand_info, description, logoBaseColor, sector)

            eft_info['parametrsEtfs'] = {}
            eft_info['parametrsEtfs']['parametersTicker'] = parameters_ticker
            eft_info['parametrsEtfs']['bcsClassCode'] = bcsClassCode 
            eft_info['parametrsEtfs']['lotSize'] = lot_size
            eft_info['parametrsEtfs']['qualInvestorFlag'] = qualInvestorFlag
            eft_info['parametrsEtfs']['isin'] = isin
            eft_info['parametrsEtfs']['currency'] = currency


            dump_image(url=logo, ticker=ticker)
            efts_list.append(eft_info)
    print('end parsing api')
    return efts_list


def start_parsing_etfs():
    list_sector = get_list_sector().get('payload',{}).get('sectors', [])
    group_by_list = {}
    
    # for sector in list_sector:
    #     group_by_list['sectors'].append({sector['eng']: []})
    efts_symbol_list = get_list_efts_paginate([])
    efts_list = parsing_api(efts_symbol_list=efts_symbol_list, efts_list=[], list_sector=list_sector)


    group_by_list = efts_list
    dump_json(group_by_list, file='json/etfs.json')

if __name__ == '__main__':
    start_parsing_etfs()
