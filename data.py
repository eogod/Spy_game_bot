from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
from config import load_database
import psycopg2


engine = create_engine(load_database())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
tele_id = 1093476166 ### потом поменяешь короче на зпрошенный айди
Base = declarative_base()
class User(Base):
    __tablename__ = "users_from_bot"
    telegram_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    points = Column(Integer, nullable=False, default=0)


class Player:
    def __init__(self):
        self.name = ''
        self.tg_id = 0
        self.points = 0
        self.role = ''
        self.command_id = 0
    def addPoint(self,num: int):
        self.point += num




Base.metadata.create_all(engine)
session = SessionLocal()
results = session.query(User).filter(
    User.telegram_id == tele_id,
).all()

# tg_id = session.query(User.telegram_id).first()
# print(tg_id)
for result in results:
    print(f"""
          Telegram_ID: {result.telegram_id}
          Name: {result.name}
          points: {result.points}
    """)

session.close()