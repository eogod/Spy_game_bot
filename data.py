from sqlalchemy import create_engine, Column, Integer, String, Enum, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from config import load_database
from random import randint
import copy

engine = create_engine(load_database())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users_from_bot"
    telegram_id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    points = Column(Integer, nullable=False, default=0)

    def update_points(telegram_id, plus_points):
        points = session.query(User.points).filter(User.telegram_id == telegram_id).first()[0]
        new_points = points + plus_points
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        user.points = new_points
        session.commit()

# 23 таска, первое время
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    normal_task = Column(Text, nullable=False)
    fake_task = Column(Text, nullable=False)

    # filter(Task.id == task_id).first()
    def get_tasks(self):
        tasks = session.query(Task).all()
        return tasks, len(tasks)


class Player:
    def __init__(self):
        self.name = ''
        self.tg_id = 0
        self.points = 0
        self.username = ''
        self.role = ''
        self.answers: list[str] = ''

    def set_answer(self, answer):
        self.answer = answer

    def set_role(self, role):
        self.role = role

    def addPoint(self, num: int):
        self.points += num


class Team:
    def init(self, team_id: int, players: list[Player]):
        self.id: int = team_id
        self.players: list[Player] = players
        self.task_for_civilian: String = ''
        self.task_for_spy: String = ''
        self.spy: list[int] = []

    def change_c_s(self):
        self.spy = [randint(0, len(self.players)) for i in range(2)]
        for i in range(len(self.players)):
            if i in self.spy:
                self.players[i].set_role('spy')
            else:
                self.players[i].set_role('civilian')

    # def voiting_results(self):
    #     '''LOGIKA                                                                                                                                                                                                                                                                                                               Шпион который выиграл раунд = 100
    #     Шпион который выиграл раунд = 100
    #     Никого из шпионов не раскрыли = 150 каждому
    #     Человек выбрал правильного шпиона(но команда нет) = 20
    #     Команда правильно кикнула шпиона = всей команде 50 (кроме шпионов)
    #     Команда правильно кикнула обеих шпионов = всей команде 100 (кроме шпионов)'''
    #     spies_id = [spy.tg_id for spy in self.spies]
    #
    #     win_spies = copy.copy(spies_id)
    #     correct_answers = 0
    #     for player in self.civilians + self.spies:
    #         if player.answer in spies_id:
    #             player.points += 20
    #             correct_answers += 1
    #             if player.answer in win_spies:
    #                 win_spies.remove(player.answer)
    #
    #     # Шпионам, кого не угадали начисляем 100
    #     for spy in self.spies:
    #         if spy.tg_id in win_spies:
    #             spy.addPoint(100)
    #
    #     # Если не угадали обоих, то ещё 50 накидываем
    #     if not correct_answers:
    #         for spy in self.spies:
    #             spy.addPoint(50)
    #
    #     if correct_answers >= 3 and len(win_spies) == 1:
    #         for civilian in self.civilians:
    #             civilian.addPoint(50)
    #
    #     elif correct_answers >= 3 and len(win_spies) == 0:
    #         for civilian in self.civilians:
    #             civilian.addPoint(100)


Base.metadata.create_all(engine)
session = SessionLocal()
results = session.query(User).all()