import random
from data import Team, Task
from bot import Persons, Teams, rounds, ready_counter
from time import sleep
from threading import Thread



def get_teams() -> None:
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
            Teams[i].players.append(Persons[-i])
    for i in Teams:
        i.change_c_s()


def functions_for_start() -> list[list[str]]:
    get_teams()
    tasks, count_tasks = Task.get_tasks()
    for team in Teams:
        team.task_for_civilian = tasks[(team.id + rounds) % count_tasks].normal_task
        team.task_for_civilian = tasks[(team.id + rounds) % count_tasks].fake_task
    team_messages = []
    for team in Teams:
        team_messages.append(get_team_message(team))
    return team_messages


def get_team_message(team: Team) -> list[str]:
    messages: list[str] = []
    for i in len(team.players):
        message = 'Ur role:\n' + team.players[i].role + '\nUr task:\n' + team.task_for_spy + '\nUr team:\n' + \
                  ''.join(['@' + player.username + ' ' for player in team.players]) + '\nUr teammate:\n@'
        if i in team.spy:
            message += team.players[(i + 1) % len(team.spy)].username
        messages.append(message)
    return messages


def spawn_treath_with_sleep() -> None:
    sleep(60)


def start_game() -> None:
    th = Thread(target=spawn_treath_with_sleep)
    th.start()


def del_user_from_lobby(tg_id: int) -> None:
    for player in Persons:
        if player.tg_id == tg_id:
            Persons.remove(player)
            break


def set_answer_pers(tg_id: int, answer: str) -> None:
    for team in Teams:
        for pers in team.players:
            if tg_id == pers.tg_id:
                pers.answers.append(answer)

            

def take_count_answer() -> list[bool]:
    ready_counter = []
    for team in Teams:
        count = 0
        for player in team.players:
            if player.answer != '':
                count += 1
        ready_counter.append(test_ready_counter(count))
    return ready_counter


def test_ready_counter(id: int, count: int) -> bool:
    if count[id] == len(Teams[id].players):
        return True
    else:
        return False


def end_game() -> None:
    ready_counter = take_count_answer()
    for i in range(len(ready_counter)):
        if ready_counter[i]:
            pass