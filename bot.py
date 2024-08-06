import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import load_config
from data_exs import a

bot = telebot.TeleBot(load_config())


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'join':
        bot.send_message(call.message.chat.id, 'join')
        # присоеденияется к игре + все кнопки показываем
    elif call.data == 'rating':
        # берем из базы даных рейтинг показываем рейтинг + кнопка back
        bot.send_message(call.message.chat.id, 'rating')
    elif call.data == 'ruls':
        bot.send_message(call.message.chat.id, 'ruls')
        # пишем список правил + кнопка back


# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    button_invite = InlineKeyboardMarkup(row_width=1)
    button_invite.add(InlineKeyboardButton(text='Присоединиться', callback_data='join'),
                      InlineKeyboardButton(text="Правила", callback_data='ruls'))
    bot.send_message(message.from_user.id, " Привет, Твой рейтинг: 0 место", reply_markup=button_invite)

    button_1 = InlineKeyboardMarkup(row_width=1)
    button_1.add(InlineKeyboardButton(text="Правила", callback_data='ruls'),
                 InlineKeyboardButton(text='rating', callback_data='rating'))
    try:
        user_name = a[message.from_user.id]
        bot.send_message(message.from_user.id, f"Привет {user_name}", reply_markup=button_1)
    except KeyError:
        print(message.from_user.id)
        bot.send_message(message.from_user.id, f"Тебя нет в базе лох", )


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "some text")
