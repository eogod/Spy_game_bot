from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import *
import asyncio
from config import load_config
from data_exs import a
import re
from data import Player

Persons: list[Player] = []
Teams: list[Team] = []
game_counter = 0
ready_counter: list[int] = []
bot = AsyncTeleBot(load_config())

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    button_successful_registration = InlineKeyboardMarkup(row_width=2)
    button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                                       InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                                       InlineKeyboardButton(text='Присоединиться', callback_data='join'),
                                       InlineKeyboardButton(text='START', callback_data='start_game')
                                       )
    pl = from_bd(message)
    try:
        await bot.send_message(message.from_user.id, text=f"🖖 Здравствуй, {pl.name}\n\n⚜️ Количество баллов: {pl.points}", reply_markup=button_successful_registration)
    except KeyError:
        await bot.send_message(message.from_user.id, text="Тебя нет в базе, обратись к админу")


@bot.message_handler(commands=['info'])
async def send_info(message):
    await bot.reply_to(message, "some text")


@bot.callback_query_handler(func=lambda call: True)
async def answer(call):
    button_back = InlineKeyboardMarkup(row_width=2)
    button_back.add(InlineKeyboardButton(text="Назад", callback_data='start'))

    if call.data == 'join':
        button_join = InlineKeyboardMarkup(row_width=2)
        button_join.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                        InlineKeyboardButton(text="Назад", callback_data='start'))

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"Подожди пока мы тебе найдем команду", reply_markup=button_join)

    elif call.data == 'start':
        for i in Persons:
            if i.tg_id == call.from_user.id:
                button_successful_registration = InlineKeyboardMarkup(row_width=2)
                button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                                                   InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                                                   InlineKeyboardButton(text='Присоединиться', callback_data='join'))
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"🖖 Здравствуй, {i.name}\n⚜️ Количество баллов: {i.points}",
                                            reply_markup=button_successful_registration)

    elif call.data == 'rating':
        # берем из базы данных рейтинг показываем рейтинг + кнопка back
        rating = "1) Я"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=rating, reply_markup=button_back)

    elif call.data == 'rules':
        # пишем список правил + кнопка back
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='rules', reply_markup=button_back)

    elif call.data == 'team':
        # взять из базы данных список команды и кнопка back
        button_team = InlineKeyboardMarkup(row_width=2)
        button_team.add(InlineKeyboardButton(text="Ответить на вопрос", callback_data='answer'),
                        InlineKeyboardButton(text='Выбрать шпиона', callback_data='choice'),
                        InlineKeyboardButton(text="Назад", callback_data='back'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='team', reply_markup=button_team)

    elif call.data == "answer":
        # взять из базы вопросы и сделать 4 кнопки отправить их
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='answer', reply_markup=button_back)

    elif call.data == "choice":
        # взять из базы имена команды и выбрать двоих
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='choice', reply_markup=button_back)


def from_bd(message):
    tg_id = message.from_user.id
    pl = Player()
    for i, req in enumerate(session.query(User).filter(User.telegram_id == tg_id).all()):
        pl.name = req.name
        pl.point = int(req.points)
        pl.tg_id = tg_id
        Persons.append(pl)
    return pl


