# Data Structures Used in the Smart Parking Management System

## Introduction

The Smart Parking Management System needs different data structures because the system performs different types of operations. These include storing parking slots, finding active vehicles quickly, processing vehicles in order, and grouping related parking information.

The choice of data structure affects how efficiently the system can store, search, update, and retrieve information.

---

## 1. Array or List

### Use in the System

A list is used to store the parking slots available in the parking facility.

Example:

```text
parkingSlots = [
    A01,
    A02,
    A03,
    A04,
    A05
]
```

Each parking slot can contain information such as:

- Slot ID
- Slot number
- Slot status
- Slot type

For example:

```text
A01 - AVAILABLE
A02 - OCCUPIED
A03 - AVAILABLE
```

### Reason for Use

A list is suitable because parking slots form a collection of similar items.

The system can move through the list to:

- Display all parking slots
- Count available slots
- Count occupied slots
- Search for an available slot
- Update a slot after vehicle entry or exit

The Parking Availability and Parking Slot Allocation modules can use this structure.

### Time Complexity

Accessing a slot by its index can take:

```text
O(1)
```

Searching through all parking slots for an available slot can take:

```text
O(n)
```

where `n` is the number of parking slots.

---

## 2. Hash Table or Dictionary

### Use in the System

A hash table can be used to store active parking sessions using the vehicle registration number as the key.

Conceptual example:

```text
activeVehicles = {
    "KDA123A": Session001,
    "KDB456B": Session002,
    "KDC789C": Session003
}
```

If vehicle `KDA123A` approaches the exit, the system can use its registration number to retrieve the corresponding active parking session.

### Reason for Use

The vehicle registration number is unique for each vehicle.

Using a hash table allows the system to find an active vehicle faster than searching every parking session one by one.

This is useful in:

- Vehicle Entry Module
- Parking Session Management Module
- Parking Duration Calculation Module
- Vehicle Exit Module

It can also help the system check whether a vehicle already has an active parking session.

### Time Complexity

Searching for a vehicle in a hash table has an average time complexity of:

```text
O(1)
```

Insertion also has an average complexity of:

```text
O(1)
```

Deletion has an average complexity of:

```text
O(1)
```

This makes a hash table suitable for fast vehicle lookup.

---

## 3. Queue

### Use in the System

A queue can be used when several vehicles are waiting to enter or leave the parking facility.

Example:

```text
FRONT

KDA123A
KDB456B
KDC789C

REAR
```

The first vehicle to arrive at the gate should normally be the first vehicle to be processed.

### Reason for Use

A queue follows the:

```text
First In, First Out
FIFO
```

principle.

This matches the normal order in which vehicles are served at an entrance or exit gate.

Typical queue operations include:

```text
enqueue()
dequeue()
peek()
```

The queue can therefore help organize vehicles waiting to be processed.

### Time Complexity

Adding a vehicle to the rear of a properly implemented queue takes:

```text
O(1)
```

Removing the vehicle at the front also takes:

```text
O(1)
```

---

## 4. Record or Object

### Use in the System

An object or record is used to group information that belongs to the same real-world item.

For example, a parking slot can be represented as:

```text
ParkingSlot
    slotID
    slotNumber
    status
```

A vehicle can be represented as:

```text
Vehicle
    vehicleID
    registrationNumber
    vehicleType
```

A parking session can contain:

```text
ParkingSession
    sessionID
    vehicle
    parkingSlot
    entryTime
    exitTime
    amountDue
    status
```

### Reason for Use

An object keeps related information together.

Instead of storing the registration number, parking slot, entry time, and session status separately, the system can keep them inside one parking session object.

This makes the program easier to organize, understand, and maintain.

Objects can be used throughout all modules of the system.

---

## 5. Set

### Use in the System

A set can be used to maintain identifiers of currently available parking slots.

Example:

```text
availableSlots = {
    A01,
    A03,
    A05,
    B02
}
```

### Reason for Use

A set does not allow duplicate values.

This helps prevent the same parking slot from accidentally appearing more than once in the collection of available spaces.

A set can also provide fast membership checks.

For example, the system can quickly determine whether:

```text
A03
```

is currently available.

### Time Complexity

Checking whether an item exists in a hash-based set has an average complexity of:

```text
O(1)
```

Adding and removing values also normally takes:

```text
O(1)
```

---

## 6. Priority Queue as an Improvement

### Use in the System

A priority queue can be used if the parking system is later improved to assign the most suitable parking space instead of simply selecting the first available slot.

For example:

```text
A01 - Priority 1
A02 - Priority 2
A03 - Priority 3
```

A smaller priority value could represent a parking space that is closer to the entrance.

### Reason for Use

A priority queue allows the system to select the highest-priority available parking slot efficiently.

This could improve the Parking Slot Allocation Module by assigning:

- The closest available slot
- A slot suitable for a particular vehicle type
- A specially designated parking slot

The first version of the system may use a simple list search. The priority queue is therefore an improvement that could be added later.

### Time Complexity

Viewing the highest-priority item can take:

```text
O(1)
```

Adding or removing an item from a heap-based priority queue normally takes:

```text
O(log n)
```

---

## Relationship Between Data Structures and System Modules

| Data Structure | Main Use | Related Modules |
|---|---|---|
| List / Array | Store and traverse parking slots | Availability, Slot Allocation |
| Hash Table / Dictionary | Fast lookup of active vehicles | Entry, Session, Duration, Exit |
| Queue | Process waiting vehicles in arrival order | Entry, Exit |
| Object / Record | Group related system information | All Modules |
| Set | Maintain unique available slot IDs | Availability, Slot Allocation |
| Priority Queue | Select the preferred parking slot | Slot Allocation |

---

## Why More Than One Data Structure Is Needed

No single data structure is ideal for every operation in the Smart Parking Management System.

A list is useful for displaying and traversing parking slots, but searching it can require checking several elements.

A hash table provides faster lookup when the vehicle registration number is known.

A queue is suitable when vehicles must be processed in arrival order.

A set prevents duplicate available parking-slot identifiers.

Objects or records make it possible to organize related information into meaningful entities.

The use of several suitable data structures therefore improves the organization and efficiency of the parking system.

## Conclusion

The Smart Parking Management System uses data structures according to the type of operation being performed. Lists support parking slot storage and traversal, hash tables provide fast access to active vehicle records, queues support first-in-first-out processing, sets maintain unique available parking slots, and objects organize related system data.

Choosing appropriate data structures makes the system easier to implement and helps improve the efficiency of important operations such as parking-space allocation and vehicle lookup.
