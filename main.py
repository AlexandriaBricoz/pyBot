from collections import defaultdict

import telebot
from telebot import types

import tocken

bot = telebot.TeleBot(tocken.tocken)

buffets = ['Буфет 1', 'Буфет 2', 'Авега']
menu = {
    buffets[0]: [['макароны', 100], ['пюре', 120], ['кофе', 80]],
    buffets[1]: [['макароны', 90], ['булочка', 100], ['чай', 60]],
    buffets[2]: [['макароны', 100], ['кофе', 80], ['суп', 120]]
}
user_data = []
users_orders = defaultdict(list)


class Users_id:
    pass


Users_id.ids = {}


def regist(message):
    if any(e[0] == message.chat.id for e in user_data):
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
    else:
        bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(message, get_name)


def input_login(message):
    bot.register_next_step_handler(message, input_login_2)


def handler_case(message):
    if message.text.strip() == 'Регистрация':
        regist(message)
    if message.text.strip() == 'Вход':
        bot.send_message(message.chat.id, 'Введите логин')
        input_login(message)
    if message.text.strip() == 'Сделать заказ':
        make_an_order(message)
    if message.text.strip() == 'Назад':
        markup = gen_markup_start()
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)


def gen_markup_start():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Регистрация")
    item2 = types.KeyboardButton("Вход")
    item3 = types.KeyboardButton("Помощь")
    item4 = types.KeyboardButton("Сделать заказ")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    return markup


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = gen_markup_start()
    bot.send_message(m.chat.id, """Привет! Я - ваш помощник в мире удобных заказов еды из буфетов 🍔🍕.

С моей помощью вы можете легко и быстро оформить заказ из различных буфетов и кафе ОГУ, и вкусная еда будет у вас в считанные минуты.

Чтобы начать пользоваться нашим сервисом, просто следуйте инструкциям:

1. Зарегистрируйтесь или войдите в свой аккаунт, если у вас уже есть учетная запись.
2. Выберите ближайший ресторан или кафе, изучите меню и создайте заказ.
3. Оплатите заказ удобным для вас способом.
4. Ожидайте быструю доставку прямо к вашей двери.

Если у вас возникнут вопросы или потребуется помощь, нажмите "Помощь", и я всегда готов помочь.🍽️""",
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    handler_case(message)


def login_does_not_exist(message):
    if message.text == 'Регистрация':
        regist(message)
    else:
        input_login_2(message)


def get_name(message):
    user_id = message.chat.id
    user_data.append([user_id, message.text])
    bot.send_message(user_id, f"Спасибо, {str(user_data[len(user_data) - 1][1])}! Теперь введите свой адрес:")
    bot.register_next_step_handler(message, get_address)


def get_address(message):
    user_id = message.chat.id
    user_data[len(user_data) - 1].append(message.text)
    bot.send_message(user_id, "Регистрация завершена. Теперь вы можете войти в аккаунт.")
    print(user_data)


def input_login_2(message):
    if [e for e in user_data if message.text == e[1]]:
        user_login = [e for e in user_data if message.text in e]
        Users_id.ids[message.chat.id] = user_login[0][0]
        bot.send_message(message.chat.id, 'Выполнен вход. Теперь вы можете сделать заказ.')
    else:
        bot.send_message(message.chat.id, 'Такой логин не существует. Попробуйте ещё раз или зарегистрируйтесь.')
        bot.register_next_step_handler(message, login_does_not_exist)


# @bot.message_handler(commands=['order'])
# def order(message):
#     user_id = message.chat.id
#     if user_id not in user_data or 'name' not in user_data[user_id] or 'address' not in user_data[user_id]:
#         bot.send_message(user_id, "Пожалуйста, зарегистрируйтесь сначала.")
#         bot.send_message(user_id, "Введите /start для начала регистрации.")
#     else:
#         bot.send_message(user_id, "Оформление заказа. Введите ваш заказ:")


def list_str(list: list) -> str:
    result = ''
    for i, string in enumerate(list):
        result = f'{result} {i + 1}) {string[0]} - {string[1]}\n'
    return result


def gen_markup_menu(message, buffet):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for dish in menu[buffet]:
        markup.add(types.KeyboardButton(dish[0]))
    bot.send_message(message.chat.id, 'Что пожелаете?)', reply_markup=markup)


def make_an_order(message):
    if message.chat.id in Users_id.ids:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for buffet in buffets:
            markup.add(types.KeyboardButton(buffet))
        markup.add(types.KeyboardButton('Назад'))
        bot.send_message(message.chat.id, "Выберите буфет или кафе.", reply_markup=markup)
        bot.register_next_step_handler(message, out_menu)
    else:
        bot.send_message(message.chat.id, 'Войдите в аккаунт')


def out_menu(message):
    buffet = message.text.strip()
    if buffet == 'Назад':
        markup = gen_markup_start()
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    elif buffet in menu.keys():
        bot.send_message(message.chat.id, f'Меню в выбранном месте:\n{list_str(menu[message.text.strip()])}')
        gen_markup_menu(message, message.text.strip())
        bot.register_next_step_handler(message, menu_case, buffet)
    else:
        bot.send_message(message.chat.id, 'Попробуйте ещё раз')
        bot.register_next_step_handler(message, out_menu)


def gen_markup_dish(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить")
    item2 = types.KeyboardButton("Оплатить заказ")
    item3 = types.KeyboardButton("Повторить заказ")
    item4 = types.KeyboardButton("Очистить корзину")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    return markup


def gen_markup_dish_case(message, buffet):
    if message.text.strip() == 'Добавить':
        gen_markup_menu(message, buffet)
        bot.register_next_step_handler(message, menu_case, buffet)
    elif message.text.strip() == 'Оплатить заказ':
        payment(message, buffet)
    elif message.text.strip() == 'Повторить заказ':
        bot.send_message(message.chat.id, repeat_order(message))
        bot.register_next_step_handler(message, gen_markup_dish_case, buffet)
    elif message.text.strip() == 'Очистить корзину':
        users_orders.pop(Users_id.ids[message.chat.id])
        markup = gen_markup_start()
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    elif message.text.strip() == 'Назад':
        markup = gen_markup_start()
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    else:
        bot.register_next_step_handler(message, gen_markup_dish_case, buffet)


def menu_case(message, buffet):
    for dish in menu[buffet]:
        if dish[0] == message.text.strip():
            users_orders[Users_id.ids[message.chat.id]].append(dish)
    markup = gen_markup_dish(message)
    print(users_orders[Users_id.ids[message.chat.id]])
    bot.send_message(message.chat.id, "Хороший выбор", reply_markup=markup)
    bot.register_next_step_handler(message, gen_markup_dish_case, buffet)


def price_order(message):
    check_sum = 0
    for price in users_orders[Users_id.ids[message.chat.id]]:
        check_sum += price[1]
    return check_sum


def payment(message, buffet):
    bot.send_message(message.chat.id, f'Стоимость заказа составляет {price_order(message)}Р')
    markup = payment_markup(message)
    bot.send_message(message.chat.id, 'Выберите способ оплаты', reply_markup=markup)
    bot.register_next_step_handler(message, payment_case, buffet)


def repeat_order(message) -> str:
    result = ''
    for paragraph in users_orders[Users_id.ids[message.chat.id]]:
        result = f'{result}{paragraph[0]} - {paragraph[1]}\n'
    return result


def payment_case(message, buffet):
    if message.text.strip() == 'Юкасса':
        bot.send_message(message.chat.id, 'Вы выбрали Юкассу')
        bot.register_next_step_handler(message, menu_case)
    elif message.text.strip() == 'СПБ':
        bot.send_message(message.chat.id, 'Вы выбрали СПБ')
    elif message.text.strip() == 'Повторить заказ':
        bot.send_message(message.chat.id, repeat_order(message))
        payment(message, buffet)
    elif message.text.strip() == 'Добавить':
        gen_markup_menu(message, buffet)
        bot.register_next_step_handler(message, menu_case, buffet)
    elif message.text.strip() == 'Очистить корзину':
        users_orders.pop(Users_id.ids[message.chat.id])
        markup = gen_markup_start()
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    else:
        payment(message, buffet)


def payment_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Юкасса")
    item2 = types.KeyboardButton("СПБ")
    item3 = types.KeyboardButton("Повторить заказ")
    item4 = types.KeyboardButton("Добавить")
    item5 = types.KeyboardButton("Очистить корзину")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    return markup


if __name__ == '__main__':
    print('start')
    bot.polling(none_stop=True, interval=0)
    print('finish')
