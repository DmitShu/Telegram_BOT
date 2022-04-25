import telebot
from bot_extensions import APIException, Bot_Extensions

# token хранится в области, вынесенной за версионный контроль.
# Для тестирования, исользуйте свой
# bot = telebot.TeleBot('')

bot = telebot.TeleBot(Bot_Extensions.get_token())

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}!\n\n"
                                      f"Чтобы узнать стоимость, введите команду в следующем формате:\n"
                                      f"<имя валюты цену которой нужно узнать> <имя валюты в которой надо узнать цену> <количество валюты> (USD RUB 1000)\n"
                                      f"Допускается не указывать количество (USD RUB)\n\n"
                                      f"список доступных валют можно узнать по команде /values")

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    bot.send_message(message.chat.id, Bot_Extensions.get_values())

# Обрабатываются все сообщения
@bot.message_handler(content_types=['text'])
def do_convert(message: telebot.types.Message):
    try:
        reply = Bot_Extensions.process_data(message.text)

    except APIException as ex:
        bot.send_message(message.chat.id, f'Ошибка:\n{ex}\n')

    except Exception as ex:
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{ex}\n'
                                          f'Попробуйте команду /help\n'
                                          f'Если ничего не помогло, обратитесь к разработчику.')

    else:
        bot.send_message(message.chat.id, reply)

bot.polling(none_stop=True)

# test area:
# quote, base, amount = 'USD', 'EUR', 1
# req = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={cur[quote]}&tsyms={cur[base]}')
# repl = json.loads(req.content)[cur[base]]
# print(repl)