import threading
import random
from data import Player
from bot import bot
from telebot import types


games = {}

def join_game(message: types.Message):
    user_id = message.from_user.id
    game_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not game_id:
        bot.send_message(message.chat.id, "Пожалуйста, укажите идентификатор игры: /join <game_id>")
        return

    if game_id not in games:
        games[game_id] = []

    if user_id in [player.telegram_id for player in games[game_id]]:
        bot.send_message(message.chat.id, "Вы уже в этой игре!")
        return

    new_player = Player(telegram_id=user_id)
    games[game_id].append(new_player)

    bot.send_message(message.chat.id, f"Вы присоединились к игре {game_id}!")

    if len(games[game_id]) >= 3:
        threading.Thread(target=start_round, args=(game_id,)).start()
    else:
        bot.send_message(message.chat.id, "Ожидаем других игроков...")


# Начало раунда
def start_round(game_id):
    players = games[game_id]
    spy = random.choice(players)

    for player in players:
        player.role = 'spy' if player == spy else 'civilian'

    ask_questions(game_id)


def ask_questions(game_id):
    players = games[game_id]
    for player in players:
        bot.send_message(player.telegram_id, "Задайте вопрос другим игрокам!")


# Команда /end <game_id> для завершения игры
@bot.message_handler(commands=['end'])
def end_game(message: types.Message):
    game_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not game_id:
        bot.send_message(message.chat.id, "Пожалуйста, укажите идентификатор игры: /end <game_id>")
        return

    if game_id in games:
        del games[game_id]
        bot.send_message(message.chat.id, f"Игра {game_id} завершена. Спасибо за участие!")
    else:
        bot.send_message(message.chat.id, f"Игра {game_id} не найдена.")