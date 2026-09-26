from collections import deque
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import heapq


def normalize_registration(registration_number: str) -> str:
    return registration_number.strip().upper().replace(" ", "")


def count_available_slots(parking_slots) -> int:
    available_count = 0

    for slot in parking_slots:
        if slot.status == "AVAILABLE":
            available_count += 1

    return available_count


def find_first_available_slot(parking_slots):
    for slot in parking_slots:
        if slot.status == "AVAILABLE":
            return slot

    return None


def build_available_slot_set(parking_slots) -> set[str]:
    available_slots = set()

    for slot in parking_slots:
        if slot.status == "AVAILABLE":
            available_slots.add(slot.slot_number)

    return available_slots


def build_active_vehicle_map(parking_sessions) -> dict:
    active_vehicles = {}

    for session in parking_sessions:
        if session.status == "ACTIVE":
            active_vehicles[
                session.vehicle.registration_number
            ] = session

    return active_vehicles


def calculate_duration_minutes(
    entry_time: datetime,
    exit_time: datetime
) -> int:
    if exit_time < entry_time:
        raise ValueError("Exit time cannot be earlier than entry time.")

    duration = exit_time - entry_time

    return max(1, int(duration.total_seconds() / 60))


def calculate_parking_fee(
    duration_minutes: int,
    first_hour_rate: Decimal,
    additional_hour_rate: Decimal
) -> Decimal:
    if duration_minutes <= 0:
        raise ValueError("Parking duration must be greater than zero.")

    billable_hours = (duration_minutes + 59) // 60

    if billable_hours <= 1:
        fee = first_hour_rate
    else:
        additional_hours = billable_hours - 1

        fee = (
            first_hour_rate
            + Decimal(additional_hours) * additional_hour_rate
        )

    return fee.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


class VehicleQueue:
    def __init__(self):
        self._queue = deque()

    def enqueue(self, registration_number: str):
        registration_number = normalize_registration(
            registration_number
        )

        self._queue.append(registration_number)

    def dequeue(self):
        if not self._queue:
            return None

        return self._queue.popleft()

    def peek(self):
        if not self._queue:
            return None

        return self._queue[0]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)


class ParkingSlotPriorityQueue:
    def __init__(self):
        self._heap = []

    def add_slot(
        self,
        priority: int,
        slot_number: str
    ):
        heapq.heappush(
            self._heap,
            (priority, slot_number)
        )

    def get_next_slot(self):
        if not self._heap:
            return None

        priority, slot_number = heapq.heappop(
            self._heap
        )

        return slot_number

    def peek(self):
        if not self._heap:
            return None

        return self._heap[0][1]

    def is_empty(self) -> bool:
        return len(self._heap) == 0
