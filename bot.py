import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import *
from config import load_config
from data_exs import a
import re
from data import Player

bot = telebot.TeleBot(load_config())
Persons = []

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    button_join = InlineKeyboardMarkup(row_width=1)
    button_join.add(InlineKeyboardButton(text='Присоединиться', callback_data='join'))
    bot.send_message(message.from_user.id, "Готов испытать себя?", reply_markup=button_join)





@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "some text")


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    button_back = InlineKeyboardMarkup(row_width=2)
    button_back.add(InlineKeyboardButton(text="Назад", callback_data='back'))
    tg_id = call.from_user.id
    pl = Player()
    for i, req in enumerate(session.query(User).filter(User.telegram_id == tg_id).all()):
        pl.name = req.name
        pl.point = int(req.points)
        pl.tg_id = tg_id
        Persons.append(pl)
    if call.data == 'join':
        button_successful_registration = InlineKeyboardMarkup(row_width=2)
        button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                     InlineKeyboardButton(text='Рейтинг', callback_data='rating'), InlineKeyboardButton(text='Моя команда', callback_data='team'))
        button_unsuccessful_registration = InlineKeyboardMarkup(row_width=1)
        button_unsuccessful_registration.add(InlineKeyboardButton(text="Назад", callback_data='unback'))

        try:
            user_name = a[call.message.chat.id]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text=f"Привет {user_name}", reply_markup=button_successful_registration)
        except KeyError:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text="Тебя нет в базе, лох", reply_markup=button_unsuccessful_registration)


    elif call.data == 'rating':
        # берем из базы даных рейтинг показываем рейтинг + кнопка back
        rating = "1) Я"

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text=rating, reply_markup=button_back)
    elif call.data == 'rules':
        # пишем список правил + кнопка back
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='rules',reply_markup=button_back)

    elif call.data == 'back':
        # функция с "начальным меню"
        button_afterback = InlineKeyboardMarkup(row_width=2)
        button_afterback.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                        InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                        InlineKeyboardButton(text='Моя команда', callback_data='team'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Начальное меню', reply_markup=button_afterback)

    elif call.data == 'team':
        # взять из базы данных список команды и кнопка back
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='team',reply_markup=button_back)
    elif call.data == "answer":
        # взять из базы вопросы и сделать 4 кнопки отправить их
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='answer',reply_markup=button_back)
    elif call.data == "choice":
        # взять из базы имена команды и выбрать двоих
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='choice',reply_markup=button_back)
    elif call.data == "unback":

        # кнопка назад при неудачной регестрации
        button_join = InlineKeyboardMarkup(row_width=1)
        button_join.add(InlineKeyboardButton(text='Присоединиться', callback_data='join'))
        bot.send_message(call.message.from_user.id, "Готов испыать себя?", reply_markup=button_join)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Готов испытать себя?', reply_markup=button_join)

