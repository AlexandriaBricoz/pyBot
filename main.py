import random

import telebot
from telebot import types

import tocken

bot = telebot.TeleBot(tocken.tocken)


def fakt_if(message):
    if old_message.message == 'fact':
        try:
            answer = str(fact(int(message)))
        except ValueError:
            answer = 'недопустимое значение'
    else:
        if message == 'Факт':
            answer = random.choice(facts)
        elif message == 'Поговорка':
            answer = random.choice(thinks)
        else:
            answer = 'Вы написали point: ' + message
    return answer


class Old_message():
    message = 0

    def new(self, text):
        self.message = text

    def __repr__(self):
        return self.message


def fact(n):
    x = 1
    for i in range(1, n + 1, 1):
        x = x * i
    return x


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь. fact найдёт факториал )')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Факт")
    item2 = types.KeyboardButton("Поговорка")
    item3 = types.KeyboardButton("fact")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(m.chat.id,
                     'Нажми: \nФакт - для получения интересного факта\n'
                     'Поговорка - для получения мудрой цитаты\n'
                     'fact - для поиска факториала ',
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    answer = fakt_if(message.text.strip())
    old_message.new(message.text.strip())
    print(old_message)  # просто тест
    bot.send_message(message.chat.id, answer)


old_message = Old_message()
facts = ['факт1', 'факт2', 'факт3']
thinks = ['поговорка1', 'поговорка2', 'поговорка3']

if __name__ == '__main__':
    print('start')
    bot.polling(none_stop=True, interval=0)
    print('finish')
