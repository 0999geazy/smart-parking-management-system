# Dynamic Database Design for the Smart Parking Management System

## Introduction

The Smart Parking Management System requires a dynamic database because information changes continuously as vehicles enter, occupy parking slots, make payments, and leave the parking facility.

The database must store current information as well as completed parking records. It should support the different modules of the system and allow information to be retrieved and updated efficiently.

The proposed database contains five main tables:

1. Vehicles
2. Parking Slots
3. Parking Sessions
4. Tariffs
5. Payments

---

## 1. Vehicles Table

The `vehicles` table stores information about vehicles that use the parking facility.

### Fields

| Field | Data Type | Description |
|---|---|---|
| vehicle_id | Integer | Primary key used to uniquely identify a vehicle |
| registration_number | Varchar | Vehicle registration number |
| vehicle_type | Varchar | Type of vehicle |
| created_at | DateTime | Date and time when the vehicle was first recorded |

### Important Rule

The registration number should be unique so that the same vehicle is not unnecessarily stored several times.

Example:

```text
vehicle_id: 1
registration_number: KDA123A
vehicle_type: Car
```

---

## 2. Parking Slots Table

The `parking_slots` table stores all parking spaces and their current status.

### Fields

| Field | Data Type | Description |
|---|---|---|
| slot_id | Integer | Primary key |
| slot_number | Varchar | Unique parking slot number |
| slot_type | Varchar | Type of parking slot |
| status | Varchar | Current slot status |

A parking slot can have a status such as:

```text
AVAILABLE
OCCUPIED
```

Example:

```text
slot_id: 3
slot_number: A03
slot_type: STANDARD
status: AVAILABLE
```

When a vehicle is allocated this slot, the status changes to:

```text
OCCUPIED
```

After the vehicle leaves, the status returns to:

```text
AVAILABLE
```

---

## 3. Parking Sessions Table

The `parking_sessions` table records every parking visit.

This table connects a vehicle to a parking slot and keeps track of the period between entry and exit.

### Fields

| Field | Data Type | Description |
|---|---|---|
| session_id | Integer | Primary key |
| vehicle_id | Integer | Foreign key referencing the vehicle |
| slot_id | Integer | Foreign key referencing the parking slot |
| entry_time | DateTime | Time the vehicle entered |
| exit_time | DateTime | Time the vehicle exited |
| duration_minutes | Integer | Total parking duration |
| amount_due | Decimal | Parking amount calculated |
| status | Varchar | Current parking session status |

Possible session statuses are:

```text
ACTIVE
COMPLETED
```

When a vehicle enters:

```text
entry_time = current time
exit_time = NULL
status = ACTIVE
```

When the vehicle leaves:

```text
exit_time = current time
duration_minutes = calculated duration
amount_due = calculated parking fee
status = COMPLETED
```

---

## 4. Tariffs Table

The `tariffs` table stores parking rates.

Keeping parking charges in the database allows management to change the rates without changing the program code.

### Fields

| Field | Data Type | Description |
|---|---|---|
| tariff_id | Integer | Primary key |
| tariff_name | Varchar | Name of the parking tariff |
| first_hour_rate | Decimal | Charge for the first hour |
| additional_hour_rate | Decimal | Charge for every additional hour |
| active | Boolean | Shows whether the tariff is currently in use |

Example:

```text
tariff_name: Standard Parking
first_hour_rate: KES 100
additional_hour_rate: KES 50
active: TRUE
```

The values above are example rates for the prototype and are not specified by the assignment.

---

## 5. Payments Table

The `payments` table stores information about payments made by drivers.

### Fields

| Field | Data Type | Description |
|---|---|---|
| payment_id | Integer | Primary key |
| session_id | Integer | Foreign key referencing the parking session |
| amount | Decimal | Amount paid |
| payment_method | Varchar | Method used to make payment |
| payment_status | Varchar | Result of the payment |
| payment_time | DateTime | Date and time of payment |
| transaction_reference | Varchar | Unique reference for the payment |

Possible payment statuses include:

```text
PENDING
PAID
FAILED
```

The exit barrier should only open when the payment status is:

```text
PAID
```

---

# Database Relationships

The main relationships are:

- One vehicle can have many parking sessions over time.
- One parking slot can be used by many parking sessions at different times.
- One parking session is associated with one vehicle.
- One parking session is associated with one parking slot.
- One parking session can have a payment record.

The relationships can be represented as:

```text
VEHICLES
   |
   | 1
   |
   | M
   v
PARKING_SESSIONS
   |
   | M
   |
   | 1
   v
PARKING_SLOTS

PARKING_SESSIONS
   |
   | 1
   |
   | 1
   v
PAYMENTS

TARIFFS
   |
   |
Used by the fee calculation process
```

---

# Primary Keys and Foreign Keys

Primary keys uniquely identify records.

The proposed primary keys are:

```text
vehicles.vehicle_id

parking_slots.slot_id

parking_sessions.session_id

tariffs.tariff_id

payments.payment_id
```

Foreign keys connect related tables.

The main foreign keys are:

```text
parking_sessions.vehicle_id
    -> vehicles.vehicle_id

parking_sessions.slot_id
    -> parking_slots.slot_id

payments.session_id
    -> parking_sessions.session_id
```

---

# How the Database Changes Dynamically

## Before Vehicle Entry

A parking slot may contain:

```text
A03
Status: AVAILABLE
```

---

## After Vehicle Entry

The system:

1. Finds or creates the vehicle record.
2. Changes the selected parking slot to `OCCUPIED`.
3. Creates a new parking session.
4. Records the current entry time.
5. Sets the parking session status to `ACTIVE`.

Example:

```text
Vehicle: KDA123A
Slot: A03
Entry Time: 09:30
Exit Time: NULL
Status: ACTIVE
```

---

## During Vehicle Exit

The system:

1. Retrieves the active parking session.
2. Records the current exit time.
3. Calculates the parking duration.
4. Calculates the parking fee.
5. Creates a payment record.

Example:

```text
Entry Time: 09:30
Exit Time: 12:15
Duration: 165 minutes
Amount Due: KES 200
Payment Status: PAID
```

---

## After Successful Exit

The system:

1. Changes the parking session status to `COMPLETED`.
2. Changes the parking slot back to `AVAILABLE`.
3. Keeps the completed session and payment records for future reference.

Example:

```text
Parking Session: COMPLETED
Payment: PAID
Slot A03: AVAILABLE
```

This allows another vehicle to use the parking slot.

---

# Important Database Rules

The database should enforce the following rules:

1. Every vehicle must have a unique registration number.
2. Every parking slot must have a unique slot number.
3. An occupied parking slot cannot be allocated to another active vehicle.
4. A vehicle should not have more than one active parking session at the same time.
5. A parking session must reference an existing vehicle.
6. A parking session must reference an existing parking slot.
7. A payment must belong to an existing parking session.
8. The exit barrier should only open after successful payment.
9. Entry and exit times should be recorded automatically by the system.

---

# Proposed Entity Relationship Summary

```text
+----------------+
|    VEHICLES    |
+----------------+
| PK vehicle_id  |
| registration   |
| vehicle_type   |
+----------------+
        |
        | 1:M
        v
+----------------------+
|   PARKING_SESSIONS   |
+----------------------+
| PK session_id        |
| FK vehicle_id        |
| FK slot_id           |
| entry_time           |
| exit_time            |
| duration_minutes     |
| amount_due           |
| status               |
+----------------------+
        |
        | M:1
        v
+----------------+
| PARKING_SLOTS  |
+----------------+
| PK slot_id     |
| slot_number    |
| slot_type      |
| status         |
+----------------+

PARKING_SESSIONS
        |
        | 1:1
        v
+----------------+
|    PAYMENTS    |
+----------------+
| PK payment_id  |
| FK session_id  |
| amount         |
| method         |
| status         |
| payment_time   |
+----------------+

+----------------+
|    TARIFFS     |
+----------------+
| PK tariff_id   |
| tariff_name    |
| first_hour     |
| additional_hr  |
| active         |
+----------------+
```

---

## Conclusion

The proposed dynamic database supports the complete Smart Parking Management System. It stores vehicle information, parking slot availability, active and completed parking sessions, parking tariffs, and payment information.

The database changes continuously as vehicles enter and leave. This makes it possible for the system to display accurate parking availability, calculate parking duration and fees, confirm payment, and release parking slots after vehicles exit.
