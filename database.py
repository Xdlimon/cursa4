from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Параметры подключения к базе данных
DATABASE_URL = 'sqlite:///./sports_booking.db'

# Создаем движок для работы с базой данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем фабрику сессий для работы с базой данных
get_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Базовый класс для определения моделей
Base = declarative_base()
