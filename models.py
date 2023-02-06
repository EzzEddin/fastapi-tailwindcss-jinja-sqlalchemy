from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config


url = URL.create(
    drivername="postgresql",
    username=config("DB_USERNAME"),
    password=config("DB_PASSWORD"),
    host="localhost",
    database="mydb",
    port=5432
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)


Base.metadata.create_all(engine)
