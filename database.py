from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ��������� ����������� � ���� ������
DATABASE_URL = 'sqlite:///./sports_booking.db'

# ������� ������ ��� ������ � ����� ������
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# ������� ������� ������ ��� ������ � ����� ������
get_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ������� ����� ��� ����������� �������
Base = declarative_base()
