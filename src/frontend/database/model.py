from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')


# Проверяем, что все переменные окружения установлены
if not all([POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_PORT, POSTGRESQL_DBNAME]):
    print("Warning: Some PostgreSQL environment variables are not set!")
    print(f"POSTGRESQL_USER: {POSTGRESQL_USER}")
    print(f"POSTGRESQL_HOST: {POSTGRESQL_HOST}")
    print(f"POSTGRESQL_PORT: {POSTGRESQL_PORT}")
    print(f"POSTGRESQL_DBNAME: {POSTGRESQL_DBNAME}")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}"
    f"@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DBNAME}?sslmode=require"
)

# Синхронный движок
engine = create_engine(DATABASE_URL, echo=True)

# Сессия
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class UserBirthInfo(Base):
    __tablename__ = "user_birth_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    birth_date: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_time: Mapped[str] = mapped_column(String(50), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(5), nullable=False)

    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("user_birth_info.user_id"), nullable=False)
    sender: Mapped[str] = mapped_column(String(20), nullable=False)  # "user" или "bot"
    text: Mapped[str] = mapped_column(Text, nullable=True)
    html: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    user = relationship("UserBirthInfo", back_populates="messages")

# Создаём таблицы
Base.metadata.create_all(engine)