import telebot
from telebot import types

from payment import create_payment_link, chech_payment_status


bot = telebot.TeleBot('5854895024:AAEFFw548ac5MRXnOpbuYsoU9a-OOatBdOk')


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.from_user.id, 'Привет! Этот бот поможет тебе подключить быстрый VPN, '
                                           'чтобы ты мог бесконечно продолжать смотреть котиков в Instagram 🐈‍⬛')
    bot.send_message(message.from_user.id, 'Чтобы начать, напиши свое имя')
    bot.register_next_step_handler(message, request_surname)


def request_surname(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, choose_tariff)


def choose_tariff(message):
    global surname
    surname = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('10 ГБ')
    btn2 = types.KeyboardButton('20 ГБ')
    btn3 = types.KeyboardButton('30 ГБ')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "✅ Выбери подходящий тариф", reply_markup=markup)
    bot.register_next_step_handler(message, generate_access)


def generate_access(message):
    # todo здесь мы получаем данные или файл

    # Получаем ссылку для оплаты
    link_for_pay = create_payment_link(message.from_user.id)

    # Создаем объект кнопки с ссылкой
    btn_url = types.InlineKeyboardButton(text='💳 Оплатить', url=link_for_pay)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(btn_url)

    # Создаем объект второй кнопки с проверкой оплаты
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_chech_payment = types.InlineKeyboardButton(text='✅ Проверить оплату')
    markup.add(btn_chech_payment)

    # Отправляем сообщение с клавиатурой и кнопкой с ссылкой
    bot.send_message(message.from_user.id, text='Нажмите на кнопку, чтобы оплатить:', reply_markup=keyboard)
    bot.send_message(chat_id=message.from_user.id, text='Проверить оплату', reply_markup=markup)
    bot.register_next_step_handler(message, check_payment)


@bot.message_handler(content_types=['text'])
def check_payment(message):
    if chech_payment_status(message.from_user.id):
        text_message = 'Оплата успешно прошла. Сейчас вышлем вам файл конфигурации VPN и инструкции'
    else:
        text_message = 'Ваш платеж не найден'

    bot.send_message(message.from_user.id, text=text_message)


bot.polling(none_stop=True, interval=0)
