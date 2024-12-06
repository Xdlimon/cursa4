from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from models import Base, Event, Booking
from database import engine, get_session
from schemas import EventCreate, BookingCreate, Event as EventSchema, Booking as BookingSchema

# Инициализация приложения FastAPI
app = FastAPI()

# Настройка CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)


# Получение сессии базы данных
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


# ----------- МАРШРУТЫ ДЛЯ ТАБЛИЦЫ EVENTS -----------

# Создание нового события
@app.post("/events/", response_model=EventSchema)
async def create_event(event: EventCreate, db: Session = Depends(get_db)) -> EventSchema:
    new_event = Event(title=event.title, date=event.date, location=event.location)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# Получение всех событий
@app.get("/events/", response_model=List[EventSchema])
async def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


# Обновление события
@app.put("/events/{event_id}/", response_model=EventSchema)
async def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)) -> EventSchema:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_event.title = event.title
    db_event.date = event.date
    db_event.location = event.location
    db.commit()
    db.refresh(db_event)
    return db_event


# Удаление события
@app.delete("/events/{event_id}/")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"detail": f"Event with id {event_id} has been deleted."}


# ----------- МАРШРУТЫ ДЛЯ ТАБЛИЦЫ BOOKINGS -----------

# Создание нового бронирования
@app.post("/bookings/", response_model=BookingSchema)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)) -> BookingSchema:
    event = db.query(Event).filter(Event.id == booking.event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    new_booking = Booking(user_name=booking.user_name, event_id=booking.event_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# Получение всех бронирований для конкретного события
@app.get("/events/{event_id}/bookings/", response_model=List[BookingSchema])
async def get_bookings_for_event(event_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.event_id == event_id).all()


# Обновление бронирования
@app.put("/bookings/{booking_id}/", response_model=BookingSchema)
async def update_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)) -> BookingSchema:
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.user_name = booking.user_name
    db_booking.event_id = booking.event_id
    db.commit()
    db.refresh(db_booking)
    return db_booking


# Удаление бронирования
@app.delete("/bookings/{booking_id}/")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"detail": f"Booking with id {booking_id} has been deleted."}
