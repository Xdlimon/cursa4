from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# ������ ��� �������� ���������� � ���������� ������������
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(Date)
    location = Column(String)

    # ����� � ��������������
    bookings = relationship("Booking", back_populates="event")


# ������ ��� �������� ���������� � �������������
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))

    # ����� � ��������
    event = relationship("Event", back_populates="bookings")
