from utils.service import dump_json, get_sector, dump_image, get_list_paginate
from utils.func_api import get_parameters_stock, get_list_sector, get_brand_info


def get_list_bonds_paginate(bonds_symbol_list: list) -> list:
    return get_list_paginate(_list=bonds_symbol_list, url='https://www.tbank.ru/api/trading/bonds/list', type_='bonds')


def parsing_api(bonds_symbol_list: list, list_sector: list, bonds_list: list=[]) -> list:
    print('start parsing api')
    bonds_symbol_list = [res.get('payload', {}).get('values', []) for res in bonds_symbol_list]
    for bonds in bonds_symbol_list:
        for bond in bonds:
            # callDate = bond.get('callDate', None)
            # lotPrice = bond.get('lotPrice', None)
            # matDate = bond.get('matDate', None)
            # nkd = bond.get('nkd', None)
            # price = bond.get('price', None)
            # prices = bond.get('prices', None)
            # pricesNoNkd = bond.get('pricesNoNkd', None)
            # totalYield = bond.get('totalYield', None)
            # yieldToCall = bond.get('yieldToCall', None)
            # yieldToClient = bond.get('yieldToClient', None)
            # riskCategory = bond.get('riskCategory', None)
            symbol = bond.get('symbol', {})
            ticker = symbol.get('ticker', None)
            tradeQualInvestor = symbol.get('tradeQualInvestor', None)
            currency = symbol.get('currency', None)
            countryOfRiskBriefName = symbol.get('countryOfRiskBriefName', None)
            exchangeShowName = symbol.get('exchangeShowName', None)
            showName = symbol.get('showName', None)

            brand = symbol.get('brand', None)
            try:
                brand_info = get_brand_info(brand=brand).get('payload', '').get('brands', [])[0]
            except IndexError:
                brand_info = get_brand_info(brand=brand).get('payload', '').get('brands', {})

            if brand_info != []:
                description = brand_info.get('brandInfo', '')
                main_link = brand_info.get('externalLinks', {}).get('main', None)
            else:
                description = None
                main_link = None

            logo = 'https://invest-brands.cdn-tinkoff.ru/'+ symbol.get('logoName', '').replace('.png', 'x160.png')
            sector = symbol.get('sector', None)
            sector_show_name = get_sector(list_sector=list_sector, code=sector)

            parameters_stock = get_parameters_stock(ticker=ticker, type_='bonds').get('payload', {})
            exclude_keys = ['auctionSchedules', 'availableOrders', 'contentMarker', 'lotPrice',\
                            'symbol']
            for key in exclude_keys:
                try:
                    del parameters_stock[key]
                except KeyError:
                    pass

            bond_info = {'ticker': ticker, 'logo': logo}
            bond_info['brand'] = brand
            bond_info['showName'] = showName
            bond_info['description'] = description
            bond_info['main_link'] = main_link
            bond_info['parametrs_bond'] = parameters_stock
            bond_info['tradeQualInvestor'] = tradeQualInvestor
            bond_info['currency'] = currency
            bond_info['exchangeShowName'] = exchangeShowName
            
            bond_info['countryOfRiskBriefName'] = countryOfRiskBriefName

            bond_info['sectorId'] = sector
            bond_info['sectorName'] =  sector_show_name
            # bond_info['callDate'] = callDate
            # bond_info['lotPrice'] = lotPrice
            # bond_info['matDate'] = matDate
            # bond_info['nkd'] = nkd
            # bond_info['price'] = price
            # bond_info['prices'] = prices
            # bond_info['pricesNoNkd'] = pricesNoNkd
            # bond_info['totalYield'] = totalYield
            # bond_info['yieldToCall'] = yieldToCall
            # bond_info['yieldToClient'] = yieldToClient
            # bond_info['riskCategory'] = riskCategory
            dump_image(url=logo, ticker=ticker)
            bonds_list.append(bond_info)
    print('end parsing api')
    return bonds_list



def start_parsing_bonds():
    list_sector = get_list_sector().get('payload',{}).get('sectors', [])
    group_by_list = {}
    
    # for sector in list_sector:
    #     group_by_list['sectors'].append({sector['eng']: []})
    
    bonds_symbol_list = get_list_bonds_paginate([])
    bonds_list = parsing_api(bonds_symbol_list=bonds_symbol_list, bonds_list=[], list_sector=list_sector)


    group_by_list = bonds_list
    dump_json(group_by_list, file='json/bonds.json')

if __name__ == '__main__':
    start_parsing_bonds()