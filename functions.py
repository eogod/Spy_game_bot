import random
from storage import Storage
from data import Team
from bot import Persons, Teams, ready_counter, game_counter
import time


def get_teams():
    count = len(Persons)
    ostatok = count % 6
    count = [i for i in range(count)]
    random.shuffle(count)
    per = [Persons[i] for i in count]
    for i in range(len(count) // 6):
        TT = Team(i + 1, per[i:i + 6])
        Teams.append(TT)
    if ostatok != 0:
        for i in range(1, ostatok + 1):
            Teams[i].append(Persons[-i])
    for i in Teams:
        i.change_c_s()


def start_game():
    game_counter = 1
    time.sleep(20)


def del_user_from_lobby(tg_id):
    for player in Persons:
        if player.tg_id == tg_id:
            Persons.remove(player)
            break


def test_ready_counter(id):
    if ready_counter[id] == len(Teams[id].players):
        return True


def end_game():
    game_counter = 0
    for i in range(len(ready_counter)):
        if test_ready_counter(i):
            pass