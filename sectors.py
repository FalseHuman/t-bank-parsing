from utils.service import dump_json
from utils.func_api import get_list_sector

def start_sector_parsing(type_: str = 'stocks') -> list:
    list_sector = get_list_sector(type_=type_).get('payload',{}).get('sectors', [])
    normalize_sector_list = []
    for sector in list_sector:
        normalize_sector_list.append({'sectorId': sector['eng'], 'sectorName': sector['rus']})
    dump_json(normalize_sector_list, file='json/sectors.json')

if __name__ == '__main__':
    start_sector_parsing()