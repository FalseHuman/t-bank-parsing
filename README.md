# Парсер биржевой информации (акции, фонды, фьючерсы, облигации) с сайта T-Банка (Тинькофф)

## Описание
Заказ с фриланса, было необходимо собирать информацию ([акции](https://www.tbank.ru/invest/stocks/), [фонды](https://www.tbank.ru/invest/etfs/), [фьючерсы](https://www.tbank.ru/invest/futures/), [облигации](https://www.tbank.ru/invest/bonds/)) для РФ-рынка и сохранить в json. Пример с [результатами](https://github.com/FalseHuman/t-bank-parsing/blob/master/json_example)


## Инструкция по установке

ЯП: Python 3.9+
Для работы парсера нужен Google Chrome, инструкция, как поставить на [VPS/VDS](https://skolo.online/documents/webscrapping/#pre-requisites)
```
cd t-bank-parsing
pip install virtualenv # Опционально
virtualenv venv # Опционально
pip install -r requirements.txt
```

# Получение cookies, headers, params
Чтобы получить эти параметры из консоли разработчика, 
получаете curl для любого запроса типа https://www.tbank.ru/api/, и испoльзуете любой curl-конвертер, и сохраняете их в utils/settings.py
```
cd utils
touch settings.py
```

# Запуск
```
python main.py 
```


Связаться со мной в [Telegram](https://t.me/FalseHuman)