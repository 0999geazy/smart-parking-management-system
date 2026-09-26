from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[int] = mapped_column(primary_key=True)
    registration_number: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    vehicle_type: Mapped[str | None] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    parking_sessions = relationship("ParkingSession", back_populates="vehicle")


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    slot_id: Mapped[int] = mapped_column(primary_key=True)
    slot_number: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False
    )
    slot_type: Mapped[str] = mapped_column(
        String(30), default="STANDARD", nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="AVAILABLE", nullable=False
    )

    parking_sessions = relationship(
        "ParkingSession", back_populates="parking_slot"
    )


class Tariff(Base):
    __tablename__ = "tariffs"

    tariff_id: Mapped[int] = mapped_column(primary_key=True)
    tariff_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_hour_rate: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    additional_hour_rate: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )


class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    session_id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.vehicle_id"),
        nullable=False
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_slots.slot_id"),
        nullable=False
    )

    entry_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    exit_time: Mapped[datetime | None] = mapped_column(DateTime)

    duration_minutes: Mapped[int | None] = mapped_column(Integer)

    amount_due: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2)
    )

    status: Mapped[str] = mapped_column(
        String(20), default="ACTIVE", nullable=False
    )

    vehicle = relationship("Vehicle", back_populates="parking_sessions")

    parking_slot = relationship(
        "ParkingSlot", back_populates="parking_sessions"
    )

    payment = relationship(
        "Payment",
        back_populates="parking_session",
        uselist=False
    )


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("parking_sessions.session_id"),
        unique=True,
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

    payment_status: Mapped[str] = mapped_column(
        String(20), default="PENDING", nullable=False
    )

    payment_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    transaction_reference: Mapped[str | None] = mapped_column(
        String(100), unique=True
    )

    parking_session = relationship(
        "ParkingSession", back_populates="payment"
    )
