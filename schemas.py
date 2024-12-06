from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Базовая информация о мероприятии
class EventBase(BaseModel):
    title: str
    date: date
    location: str

# Схема для создания нового события
class EventCreate(EventBase):
    pass

# Ответ с информацией о бронировании
class BookingBase(BaseModel):
    user_name: str
    event_id: int

class BookingCreate(BookingBase):
    pass

# Упрощенное представление мероприятия для ссылки в Booking
class EventInBooking(BaseModel):
    id: int
    title: str
    date: date

    class Config:
        orm_mode = True

# Полная информация о бронировании
class Booking(BookingBase):
    id: int
    event: Optional[EventInBooking]  # Ссылка на упрощённую схему Event

    class Config:
        orm_mode = True

# Полная информация о мероприятии
class Event(EventBase):
    id: int
    bookings: List[Booking] = []  # Полные данные о бронированиях

    class Config:
        orm_mode = True
