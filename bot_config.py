#Словарь доступных валют
#Добавлены синонимы Пишем в капсе для простоты проверок потом.
currency = {
    'USD': ('USD', 'ДОЛЛАР', '$'),
    'EUR': ('EUR', 'ЕВРО', '€'),
    'RUB': ('RUB', 'РУБЛЬ', 'РУБ', 'Р'),
    'JPY': ('JPY', 'ЙЕНА'),
    'BTC': ('BTC', 'БИТКОИН', 'BITCOIN'),
    'ETH': ('ETH', 'ЭФИРИУМ', 'ETHERIUM'),
}

#URL GET запроса
#https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=EUR
url_get = ('https://min-api.cryptocompare.com/data/price?fsym=', '&tsyms=')