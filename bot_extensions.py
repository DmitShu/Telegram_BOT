import requests
import json
from bot_config import currency

class APIException(Exception):
    pass

class Bot_Extensions:

    # вытаскиваем ключ бота из скрытого файла
    @staticmethod
    def get_token():

        with open('data\Token') as t:
            return (t.read())

    # вывод в сообщение текста доступных валют
    @staticmethod
    def get_values():
        reply = "Доступные валюты:"
        for k in currency.values():
            reply += '\n' + '\t' + '-'.join(k)
        return(reply)

    # проверки данных от пользователя и вывод текста
    @staticmethod
    def process_data(values: str):

        extxt = f'\nВведите команду в следующем формате:\n ' \
                f'<имя валюты цену которой нужно узнать> <имя валюты в которой надо узнать цену> <количество валюты> (USD RUB 1000)\n' \
                f'Допускается не указывать количество (USD RUB)\n\n' \
                f'список доступных валют можно узнать по команде /values'

        values = values.split()

        if len(values) < 2:
            raise APIException(f'"Параметров должно быть не менее двух"\n'
                                f'Например USD EUR')
        elif len(values) > 3:
            raise APIException(f'"Параметров слишком много"' + extxt)

        elif len(values) == 2:
            values += '1'

        quote, base, amount = values

        quote_ticker, base_ticker = '', ''

        for k, v in currency.items():

            if quote.upper() in v:
                quote_ticker = k

            if base.upper() in v:
                base_ticker = k

        if quote_ticker == '':
                raise APIException(f'"Не удалось обработать валюту {quote}"' + extxt)

        if base_ticker == '':
                raise APIException(f'"Не удалось обработать валюту {base}"' + extxt)

        if quote == base:
            raise APIException(f'"Введены одинаковые валюты {base} {base}"' + extxt)

        try:
            amount = abs(float(amount.replace(',', '.')))
        except:
            raise APIException(f'"Не удалось обработать количество {amount}"' + extxt)

        total = Bot_Extensions.get_price(quote_ticker, base_ticker, amount)

        reply = f'Цена {amount} {quote} в {base} = {round(total, 2)}'

        return reply

    # возвращает нужную сумму в валюте
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        try:
            req = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        except:
            raise APIException(f'"Сервер не отвечает"\n'
                               f'Попробуйте повторить запрос позже.\n'
                               f'Если не помогло, обратитесь к разработчику.\n')

        try:
            total = json.loads(req.content)[base] * amount
        except:
            raise APIException(f'"Неожиданный ответа сервера: {json.loads(req.content)}"\n'
                               f'Попробуйте повторить запрос позже.\n'
                               f'Если не помогло, обратитесь к разработчику.\n')

        return total