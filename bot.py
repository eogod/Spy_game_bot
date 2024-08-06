from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import *
from config import load_config
from data import Player

f = 1

Persons: list[Player] = []
Teams: list[Team] = []
game_counter = 0
ready_counter: list[int] = []
bot = AsyncTeleBot(load_config())

bot = AsyncTeleBot(load_config())


# Define a command handler
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    button_successful_registration = InlineKeyboardMarkup(row_width=2)
    button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                                       InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                                       InlineKeyboardButton(text='Присоедиться к лоби', callback_data='join'))
    pl = from_bd(message)
    try:
        await  bot.send_message(message.from_user.id,
                                text=f"🖖 Здравствуй, {pl.name}\n\n⚜️ Количество баллов: {pl.points}",
                                reply_markup=button_successful_registration)
    except KeyError:
        await bot.send_message(message.from_user.id, text="Тебя нет в базе обратись к админу")


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "some text")


@bot.callback_query_handler(func=lambda call: True)
async def answer(call):
    if call.data == 'join':
        if f:
            button_join = InlineKeyboardMarkup(row_width=2)
            button_join.add(InlineKeyboardButton(text="Обновить", callback_data='join'),
                            InlineKeyboardButton(text="Назад", callback_data='main'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"Подожди пока мы тебе найдем команду", reply_markup=button_join)
        else:
            button_join = InlineKeyboardMarkup(row_width=1)
            button_join.add(InlineKeyboardButton(text="Твоя карточка", callback_data='team'),
                            InlineKeyboardButton(text="Назад", callback_data='main'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"!", reply_markup=button_join)

    elif call.data == 'main':
        for i in Persons:
            if i.tg_id == call.from_user.id:
                button_successful_registration = InlineKeyboardMarkup(row_width=2)
                button_successful_registration.add(InlineKeyboardButton(text="Правила", callback_data='rules'),
                                                   InlineKeyboardButton(text='Рейтинг', callback_data='rating'),
                                                   InlineKeyboardButton(text='Присоедиться к лоби',
                                                                        callback_data='join'), )
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"🖖 Здравствуй, {i.name}⚜️ Количество баллов: {i.points}",
                                            reply_markup=button_successful_registration)
    elif call.data == 'rating':
        rating = "1) Я"
        button_rating = InlineKeyboardMarkup(row_width=2)
        button_rating.add(InlineKeyboardButton(text="Назад", callback_data='main'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=rating, reply_markup=button_rating)
    elif call.data == 'rules':
        button_rules = InlineKeyboardMarkup(row_width=2)
        button_rules.add(InlineKeyboardButton(text="Назад", callback_data='main'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='rules', reply_markup=button_rules)

    elif call.data == 'team':
        button_team = InlineKeyboardMarkup(row_width=2)
        button_team.add(InlineKeyboardButton(text='Список участников лоби', callback_data='team_lobi'),
                        InlineKeyboardButton(text="Выбрать шпионов", callback_data='answer1'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='team', reply_markup=button_team)
    elif call.data == 'team_list':
        button_team_list = InlineKeyboardMarkup(row_width=2)
        button_team_list.add(InlineKeyboardButton(text='Назад', callback_data='team'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='team', reply_markup=button_team_list)
    elif call.data == "answer2":
        # взять из базы вопросы и сделать 4 кнопки отправить их
        button_back = InlineKeyboardMarkup(row_width=2)
        button_back.add(InlineKeyboardButton(text="Назад", callback_data='start'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='answer', reply_markup=button_back)


def from_bd(message):
    tg_id = message.from_user.id
    pl = Player()
    for i, req in enumerate(session.query(User).filter(User.telegram_id == tg_id).all()):
        pl.name = req.name
        pl.point = int(req.points)
        pl.tg_id = tg_id
        Persons.append(pl)
    return pl
