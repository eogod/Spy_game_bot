import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import load_config
import logging


bot = telebot.TeleBot(load_config())

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.add(InlineKeyboardButton(text='invite', callback_data='invite'), InlineKeyboardButton(text='rating', callback_data='rating'))
    bot.reply_to(message, "Welcome to Spy game bot", reply_markup=buttons)

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "some text")


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'invite':
        bot.send_message(call.message.chat.id, 'invite')
    elif call.data == 'rating':
        bot.send_message(call.message.chat.id, 'rating')