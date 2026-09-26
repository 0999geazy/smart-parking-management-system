# Algorithms for the Smart Parking Management System

## Introduction

The Smart Parking Management System is divided into eight proposed modules. Each module has an algorithm that describes the logical steps the system follows to perform its function.

The algorithms below are written in pseudocode so that the system logic can later be implemented using a programming language such as Python, Java, or C++.

---

## Algorithm 1: Parking Availability and Visual Display

### Purpose

To determine the number of available parking slots and display their current status to drivers before entry.

### Pseudocode

```text
ALGORITHM DisplayParkingAvailability

START

availableCount = 0
occupiedCount = 0

FOR each parkingSlot in parkingSlots

    IF parkingSlot.status = "AVAILABLE"
        availableCount = availableCount + 1
    ELSE IF parkingSlot.status = "OCCUPIED"
        occupiedCount = occupiedCount + 1
    END IF

END FOR

DISPLAY total number of parking slots
DISPLAY availableCount
DISPLAY occupiedCount

FOR each parkingSlot in parkingSlots
    DISPLAY parkingSlot.slotNumber and parkingSlot.status
END FOR

IF availableCount = 0
    DISPLAY "PARKING FULL"
END IF

STOP
```

---

## Algorithm 2: Vehicle Entry

### Purpose

To validate and record a vehicle when it arrives at the parking facility.

### Pseudocode

```text
ALGORITHM RecordVehicleEntry

START

READ vehicleRegistration

IF vehicleRegistration is empty
    DISPLAY "Vehicle registration number is required"
    STOP
END IF

SEARCH for an ACTIVE parking session
using vehicleRegistration

IF active session exists
    DISPLAY "Vehicle is already inside the parking area"
    STOP
END IF

CHECK number of available parking slots

IF available slots = 0
    DISPLAY "PARKING FULL"
    STOP
END IF

RECORD vehicleRegistration

CALL AllocateParkingSlot(vehicleRegistration)

STOP
```

---

## Algorithm 3: Parking Slot Allocation

### Purpose

To select an available parking slot and assign it to the arriving vehicle.

### Pseudocode

```text
ALGORITHM AllocateParkingSlot

START

selectedSlot = NULL

FOR each parkingSlot in parkingSlots

    IF parkingSlot.status = "AVAILABLE"
        selectedSlot = parkingSlot
        BREAK
    END IF

END FOR

IF selectedSlot = NULL
    DISPLAY "No parking slot is available"
    STOP
END IF

SET selectedSlot.status = "OCCUPIED"

SAVE selectedSlot

DISPLAY "Allocated Parking Slot: " + selectedSlot.slotNumber

CALL CreateParkingSession(vehicleRegistration, selectedSlot)

UPDATE parking availability display

STOP
```

---

## Algorithm 4: Parking Session Management

### Purpose

To create and maintain a parking session containing the vehicle, allocated parking slot, entry time, exit time, and session status.

### Pseudocode

```text
ALGORITHM CreateParkingSession

START

GENERATE unique sessionID

entryTime = CURRENT_DATE_TIME

CREATE new parkingSession

SET parkingSession.sessionID = sessionID
SET parkingSession.vehicleRegistration = vehicleRegistration
SET parkingSession.slotID = selectedSlot.slotID
SET parkingSession.entryTime = entryTime
SET parkingSession.exitTime = NULL
SET parkingSession.status = "ACTIVE"

SAVE parkingSession

DISPLAY "Vehicle entry recorded successfully"
DISPLAY entryTime
DISPLAY selectedSlot.slotNumber

STOP
```

---

## Algorithm 5: Parking Duration Calculation

### Purpose

To calculate the total amount of time a vehicle has spent in the parking facility.

### Pseudocode

```text
ALGORITHM CalculateParkingDuration

START

READ vehicleRegistration

SEARCH for ACTIVE parking session
using vehicleRegistration

IF active parking session does not exist
    DISPLAY "Active parking session not found"
    STOP
END IF

entryTime = parkingSession.entryTime

exitTime = CURRENT_DATE_TIME

durationMinutes = exitTime - entryTime

IF durationMinutes < 0
    DISPLAY "Invalid parking duration"
    STOP
END IF

SET parkingSession.exitTime = exitTime

RETURN durationMinutes

STOP
```

---

## Algorithm 6: Parking Fee and Payment

### Purpose

To calculate the amount payable based on the parking duration and confirm payment before allowing the vehicle to exit.

### Pseudocode

```text
ALGORITHM CalculateFeeAndProcessPayment

START

GET durationMinutes

GET active parking tariff from database

billableHours = CEILING(durationMinutes / 60)

IF billableHours <= 1
    parkingFee = firstHourRate
ELSE
    additionalHours = billableHours - 1

    parkingFee =
        firstHourRate +
        (additionalHours * additionalHourRate)
END IF

DISPLAY "Parking Duration: " + durationMinutes
DISPLAY "Amount Due: KES " + parkingFee

REQUEST payment

IF payment is successful

    SET paymentStatus = "PAID"

    RECORD payment amount
    RECORD payment date and time
    RECORD payment status

    SAVE payment

    DISPLAY "Payment Successful"

ELSE

    SET paymentStatus = "FAILED"

    DISPLAY "Payment Failed"
    DISPLAY "Barrier remains closed"

END IF

RETURN paymentStatus

STOP
```

---

## Algorithm 7: Vehicle Exit and Barrier Control

### Purpose

To allow a vehicle to leave only after successful payment and release its parking slot.

### Pseudocode

```text
ALGORITHM ProcessVehicleExit

START

READ vehicleRegistration

SEARCH for ACTIVE parking session

IF active parking session does not exist
    DISPLAY "Vehicle record not found"
    KEEP barrier CLOSED
    STOP
END IF

CALL CalculateParkingDuration

CALL CalculateFeeAndProcessPayment

IF paymentStatus != "PAID"
    KEEP barrier CLOSED
    DISPLAY "Payment is required before exit"
    STOP
END IF

SET barrierStatus = "OPEN"

DISPLAY "Barrier Open"
DISPLAY "Vehicle may exit"

CONFIRM vehicle has exited

SET parkingSession.status = "COMPLETED"

SET allocatedParkingSlot.status = "AVAILABLE"

SAVE parkingSession

SAVE parkingSlot

SET barrierStatus = "CLOSED"

UPDATE parking availability display

DISPLAY "Exit completed successfully"

STOP
```

---

## Algorithm 8: Dynamic Database Management

### Purpose

To store and update information generated by the parking system.

### Pseudocode

```text
ALGORITHM ManageDatabase

START

RECEIVE operation
RECEIVE data

IF operation = "VEHICLE_ENTRY"

    INSERT vehicle if it does not already exist

    INSERT parking session

    UPDATE parking slot
    SET status = "OCCUPIED"

ELSE IF operation = "PAYMENT"

    INSERT payment record

ELSE IF operation = "VEHICLE_EXIT"

    UPDATE parking session
    SET exit time
    SET parking fee
    SET status = "COMPLETED"

    UPDATE parking slot
    SET status = "AVAILABLE"

END IF

IF database operation is successful

    COMMIT changes

ELSE

    ROLLBACK changes

    DISPLAY "Database operation failed"

END IF

STOP
```

---

## Overall Algorithm Flow

The eight algorithms work together in the following sequence:

```text
Driver Approaches Parking
        |
        v
Display Available Parking Slots
        |
        v
Record Vehicle Entry
        |
        v
Allocate Parking Slot
        |
        v
Create Parking Session
        |
        v
Vehicle Parks
        |
        v
Vehicle Requests Exit
        |
        v
Calculate Parking Duration
        |
        v
Calculate Parking Fee
        |
        v
Process Payment
        |
        v
Payment Successful?
     /        \
   No          Yes
   |            |
Barrier       Open Barrier
Closed           |
                 v
             Vehicle Exits
                 |
                 v
          Release Parking Slot
                 |
                 v
          Complete Parking Session
                 |
                 v
       Update Display and Database
```

## Conclusion

The algorithms describe how the proposed modules work together to automate the parking process. They ensure that parking availability is displayed before entry, vehicles are recorded when they arrive, parking time and fees are calculated automatically, payment is confirmed before exit, and parking records are continuously updated in the database.
