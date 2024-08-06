import random
from storage import Storage

def get_teams():
    count_spy = 2
    count_heroes = 4
    team_size = count_spy + count_heroes

    count_teams = len(Storage.data) // team_size
    not_enough = len(Storage.data) % team_size # ???????
    random.shuffle(Storage.data)
    
    # Storage.teams = [Storage.data[i:i+team_size] for i in range(0, count_teams, team_size)]
    for i in range(0, len(Storage.data), team_size):
        Storage.teams.append({"spy": Storage.data[i:i+count_spy], "hero": Storage.data[i+count_spy:i+count_heroes+count_spy]})
    return Storage.teams