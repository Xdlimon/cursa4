import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_session
from models import Event, Booking

# Создаем тестовый клиент
client = TestClient(app)

# Переопределяем базу данных для тестов
@pytest.fixture(autouse=True)
def setup_test_database():
    # Создаем таблицы для тестов
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Фикстура для работы с базой данных."""
    db = get_session()
    try:
        yield db
    finally:
        db.close()

# Тест для создания мероприятий и бронирований
def test_create_events_and_bookings(db_session):
    # Создаем мероприятия
    events_data = [
        {"title": "Football Match", "date": "2024-12-10", "location": "Stadium A"},
        {"title": "Tennis Training", "date": "2024-12-11", "location": "Court B"},
    ]
    event_ids = []

    for event in events_data:
        response = client.post("/events/", json=event)
        assert response.status_code == 200
        event_data = response.json()
        assert event_data["title"] == event["title"]
        assert event_data["location"] == event["location"]
        event_ids.append(event_data["id"])

    # Создаем бронирования для мероприятий
    bookings_data = [
        {"user_name": "Alice", "event_id": event_ids[0]},
        {"user_name": "Bob", "event_id": event_ids[1]},
    ]

    for booking in bookings_data:
        response = client.post("/bookings/", json=booking)
        assert response.status_code == 200
        booking_data = response.json()
        assert booking_data["user_name"] == booking["user_name"]
        assert booking_data["event"]["id"] == booking["event_id"]

    # Проверяем бронирования для каждого мероприятия
    for event_id in event_ids:
        response = client.get(f"/events/{event_id}/bookings/")
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) > 0
