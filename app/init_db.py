from decimal import Decimal

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import ParkingSlot, Tariff


def create_tables():
    Base.metadata.create_all(bind=engine)


def seed_parking_slots(db):
    existing_slots = db.scalars(
        select(ParkingSlot)
    ).all()

    if existing_slots:
        return

    slot_numbers = [
        "A01",
        "A02",
        "A03",
        "A04",
        "A05",
        "B01",
        "B02",
        "B03",
        "B04",
        "B05",
    ]

    for slot_number in slot_numbers:
        slot = ParkingSlot(
            slot_number=slot_number,
            slot_type="STANDARD",
            status="AVAILABLE",
        )

        db.add(slot)


def seed_tariff(db):
    existing_tariff = db.scalar(
        select(Tariff).where(
            Tariff.active.is_(True)
        )
    )

    if existing_tariff:
        return

    tariff = Tariff(
        tariff_name="Standard Parking",
        first_hour_rate=Decimal("100.00"),
        additional_hour_rate=Decimal("50.00"),
        active=True,
    )

    db.add(tariff)


def initialize_database():
    create_tables()

    db = SessionLocal()

    try:
        seed_parking_slots(db)
        seed_tariff(db)

        db.commit()

        print("Database initialized successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()
