import logging
from stocks import start_parsing_stocks
from bonds import start_parsing_bonds
from futures import start_parsing_futures
from etfs import start_parsing_etfs
from sectors import start_sector_parsing

logging.basicConfig(level=logging.INFO, filename="parsing.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

if __name__ == '__main__':
    list_func = [start_sector_parsing, start_parsing_stocks, start_parsing_bonds, start_parsing_futures, start_parsing_etfs]
    for func in list_func:
        try:
            logging.info(f"start parsing {func.__name__}")
            func()
            logging.info(f"end parsing {func.__name__}")
        except Exception as e:
            logging.error(f'{e}')