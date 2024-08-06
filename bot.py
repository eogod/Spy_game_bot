import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import *
from config import load_config
from data_exs import a
import re
from data import Player

persons = []
bot = telebot.TeleBot(load_config())

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    button_successful_registration = InlineKeyboardMarkup(row_width=2)
    button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                                       InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                                       InlineKeyboardButton(text='Присоединиться', callback_data='join'),
                                       InlineKeyboardButton(text='START', callback_data='start_game')
                                       )
    pl = from_bd(message)
    try:
        bot.send_message(message.from_user.id,text=f"🖖 Здравствуй, {pl.name}\n\n⚜️ Количество баллов: {pl.points}", reply_markup=button_successful_registration)
    except KeyError:
        bot.send_message(message.from_user.id,text="Тебя нет в базе обратись к админу")



@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "some text")


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    button_back = InlineKeyboardMarkup(row_width=2)
    button_back.add(InlineKeyboardButton(text="Назад", callback_data='start'))
    if call.data == 'join':
        button_join = InlineKeyboardMarkup(row_width=2)
        button_join.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                        InlineKeyboardButton(text="Назад", callback_data='start'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Подожди пока мы тебе найдем команду", reply_markup=button_join)
    elif call.data == 'start':
        for i in persons:
            if i.tg_id == call.from_user.id:
                button_successful_registration = InlineKeyboardMarkup(row_width=2)
                button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                                                   InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                                                   InlineKeyboardButton(text='Присоедиться', callback_data='join'), )
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"🖖 Здравствуй, {i.name}⚜️ Количество баллов: {i.points}",
                                 reply_markup=button_successful_registration)
    elif call.data == 'rating':
        # берем из базы даных рейтинг показываем рейтинг + кнопка back
        rating = "1) Я"

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text=rating, reply_markup=button_back)
    #elif call.data == 'start_game':
        #функция для начала игры
    elif call.data == 'rules':
        # пишем список правил + кнопка back
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='rules',reply_markup=button_back)

    elif call.data == 'team':
        # взять из базы данных список команды и кнопка back
        button_team = InlineKeyboardMarkup(row_width=2)
        button_team.add(InlineKeyboardButton(text="Ответить на вопрос", callback_data='answer'),
                             InlineKeyboardButton(text='Выбрать шпиона', callback_data='choice'),
                             InlineKeyboardButton(text="Назад", callback_data='back'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 text='team',reply_markup=button_team)
    elif call.data == "answer":
        # взять из базы вопросы и сделать 4 кнопки отправить их
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='answer',reply_markup=button_back)
    elif call.data == "choice":
        # взять из базы имена команды и выбрать двоих
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='choice',reply_markup=button_back)




def from_bd(message):
    tg_id = message.from_user.id
    pl = Player()
    for i, req in enumerate(session.query(User).filter(User.telegram_id == tg_id).all()):
        pl.name = req.name
        pl.point = int(req.points)
        pl.tg_id = tg_id
        persons.append(pl)
    return pl