import random
from data import Player, Team
from bot import Persons


def get_teams():
    count = len(Persons)
    ostatok = count % 6
    count = [i for i in range(count)]
    random.shuffle(count)
    per = [Persons[i] for i in count]
    Teams = [per[i:i+6] for i in range(count//6)]
    if ostatok == 0:
        return Teams
    else:
        for i in range(1, ostatok+1):
            Team[i-1].append(Persons[-i])
        return Teams

def del_user_from_lobby(tg_id):
    for player in Persons:
        if player.tg_id == tg_id:
            Persons.remove(player)
            break
