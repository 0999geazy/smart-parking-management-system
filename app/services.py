from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.algorithms import (
    ParkingSlotPriorityQueue,
    calculate_duration_minutes,
    calculate_parking_fee,
    normalize_registration,
)
from app.models import (
    ParkingSession,
    ParkingSlot,
    Payment,
    Tariff,
    Vehicle,
)


class ParkingError(Exception):
    pass


def get_dashboard_data(db: Session):
    slots = db.scalars(
        select(ParkingSlot).order_by(ParkingSlot.slot_number)
    ).all()

    available_count = sum(
        1 for slot in slots if slot.status == "AVAILABLE"
    )

    occupied_count = sum(
        1 for slot in slots if slot.status == "OCCUPIED"
    )

    return {
        "slots": slots,
        "total_slots": len(slots),
        "available_count": available_count,
        "occupied_count": occupied_count,
    }


def get_active_session(
    db: Session,
    registration_number: str
):
    registration_number = normalize_registration(
        registration_number
    )

    statement = (
        select(ParkingSession)
        .join(Vehicle)
        .where(
            Vehicle.registration_number == registration_number,
            ParkingSession.status == "ACTIVE",
        )
        .order_by(ParkingSession.session_id.desc())
    )

    return db.scalar(statement)


def record_vehicle_entry(
    db: Session,
    registration_number: str,
    vehicle_type: str = "CAR"
):
    registration_number = normalize_registration(
        registration_number
    )

    if not registration_number:
        raise ParkingError(
            "Vehicle registration number is required."
        )

    existing_session = get_active_session(
        db,
        registration_number
    )

    if existing_session:
        raise ParkingError(
            "This vehicle already has an active parking session."
        )

    available_slots = db.scalars(
        select(ParkingSlot)
        .where(ParkingSlot.status == "AVAILABLE")
        .order_by(ParkingSlot.slot_number)
    ).all()

    if not available_slots:
        raise ParkingError("Parking is full.")

    slot_queue = ParkingSlotPriorityQueue()
    slot_map = {}

    for priority, slot in enumerate(
        available_slots,
        start=1
    ):
        slot_queue.add_slot(
            priority,
            slot.slot_number
        )

        slot_map[slot.slot_number] = slot

    selected_slot_number = slot_queue.get_next_slot()

    selected_slot = slot_map[
        selected_slot_number
    ]

    vehicle = db.scalar(
        select(Vehicle).where(
            Vehicle.registration_number
            == registration_number
        )
    )

    if vehicle is None:
        vehicle = Vehicle(
            registration_number=registration_number,
            vehicle_type=vehicle_type.upper()
        )

        db.add(vehicle)
        db.flush()

    selected_slot.status = "OCCUPIED"

    parking_session = ParkingSession(
        vehicle_id=vehicle.vehicle_id,
        slot_id=selected_slot.slot_id,
        entry_time=datetime.now(),
        status="ACTIVE"
    )

    db.add(parking_session)

    try:
        db.commit()
        db.refresh(parking_session)
    except Exception:
        db.rollback()
        raise ParkingError(
            "Vehicle entry could not be recorded."
        )

    return parking_session


def calculate_exit_details(
    db: Session,
    registration_number: str
):
    parking_session = get_active_session(
        db,
        registration_number
    )

    if parking_session is None:
        raise ParkingError(
            "No active parking session was found."
        )

    tariff = db.scalar(
        select(Tariff)
        .where(Tariff.active.is_(True))
        .order_by(Tariff.tariff_id.desc())
    )

    if tariff is None:
        raise ParkingError(
            "No active parking tariff was found."
        )

    exit_time = datetime.now()

    duration_minutes = calculate_duration_minutes(
        parking_session.entry_time,
        exit_time
    )

    parking_fee = calculate_parking_fee(
        duration_minutes,
        tariff.first_hour_rate,
        tariff.additional_hour_rate
    )

    parking_session.exit_time = exit_time
    parking_session.duration_minutes = duration_minutes
    parking_session.amount_due = parking_fee

    db.commit()
    db.refresh(parking_session)

    return parking_session


def confirm_payment_and_exit(
    db: Session,
    session_id: int,
    payment_method: str = "SIMULATED"
):
    parking_session = db.get(
        ParkingSession,
        session_id
    )

    if parking_session is None:
        raise ParkingError(
            "Parking session was not found."
        )

    if parking_session.status != "ACTIVE":
        raise ParkingError(
            "This parking session has already been completed."
        )

    if parking_session.amount_due is None:
        raise ParkingError(
            "Parking fee has not been calculated."
        )

    existing_payment = db.scalar(
        select(Payment).where(
            Payment.session_id == session_id
        )
    )

    transaction_reference = (
        f"SIM-{session_id}-"
        f"{int(datetime.now().timestamp())}"
    )

    if existing_payment is None:
        payment = Payment(
            session_id=session_id,
            amount=parking_session.amount_due,
            payment_method=payment_method.upper(),
            payment_status="PAID",
            payment_time=datetime.now(),
            transaction_reference=transaction_reference
        )

        db.add(payment)

    else:
        existing_payment.amount = (
            parking_session.amount_due
        )

        existing_payment.payment_method = (
            payment_method.upper()
        )

        existing_payment.payment_status = "PAID"
        existing_payment.payment_time = datetime.now()

        existing_payment.transaction_reference = (
            transaction_reference
        )

    parking_slot = db.get(
        ParkingSlot,
        parking_session.slot_id
    )

    if parking_slot is None:
        db.rollback()

        raise ParkingError(
            "The allocated parking slot was not found."
        )

    parking_session.status = "COMPLETED"
    parking_slot.status = "AVAILABLE"

    try:
        db.commit()
        db.refresh(parking_session)
    except Exception:
        db.rollback()

        raise ParkingError(
            "Payment or vehicle exit could not be completed."
        )

    return {
        "session": parking_session,
        "barrier_status": "OPEN",
        "payment_status": "PAID",
        "transaction_reference": transaction_reference,
    }
