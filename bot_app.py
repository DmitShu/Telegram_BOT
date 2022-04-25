import telebot
from bot_extensions import APIException, BotExtensions

# token хранится в области, вынесенной за версионный контроль.
# Для тестирования, исользуйте свой
# bot = telebot.TeleBot('')

bot = telebot.TeleBot(BotExtensions.get_token())

# Обрабатываются сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}!\n\n"
                                      f"Чтобы узнать стоимость, введите команду в следующем формате:\n"
                                      f"<имя валюты цену которой нужно узнать> <имя валюты в которой надо узнать цену> <количество валюты> ( апример USD RUB 1000)\n"
                                      f"Допускается не указывать количество (пример USD RUB)\n\n"
                                      f"список доступных валют можно узнать по команде /values")


# Обрабатывается сообщение, содержащее команду '/values'
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    bot.send_message(message.chat.id, BotExtensions.get_values())


# Обрабатываются все текстовые сообщения
@bot.message_handler(content_types=['text'])
def try_convert(message: telebot.types.Message):
    try:
        reply = BotExtensions.process_data(message.text)

    except APIException as ex:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{ex}\n')

    except Exception as ex:
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{ex}\n'
                                          f'Для помощи используйте команду /help\n'
                                          f'Если ничего не помогло, обратитесь к разработчику.')

    else:
        bot.send_message(message.chat.id, reply)


bot.polling()