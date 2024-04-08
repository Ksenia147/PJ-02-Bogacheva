import telebot
from extensions import APIException, CryptoConverter
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = ("Добро пожаловать в бота для перевода валют!\n\nЧтобы начать работу введите команду в следующем формате:\n"
            "<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> "
            "<количество первой валюты>\n\nВводите название валюты в именительном падеже и единственном числе\n"
            "Чтобы узнать возможные валюты, введите команду /values")
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types= "text")
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("Количество параметров не совпадает с необходимым")

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду {e}")
    else:
        text = f"Цена {amount} {base} в {quote} - {total_base * int(amount)}"
        bot.reply_to(message, text)

bot.polling(none_stop=True)
