import telebot
from config import load_config
import logging


bot = telebot.TeleBot(load_config())

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Spy game bot")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "some text")


