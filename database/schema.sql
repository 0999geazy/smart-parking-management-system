CREATE TABLE vehicles (
    vehicle_id BIGSERIAL PRIMARY KEY,
    registration_number VARCHAR(20) NOT NULL UNIQUE,
    vehicle_type VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parking_slots (
    slot_id BIGSERIAL PRIMARY KEY,
    slot_number VARCHAR(10) NOT NULL UNIQUE,
    slot_type VARCHAR(30) NOT NULL DEFAULT 'STANDARD',
    status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',

    CONSTRAINT valid_slot_status
        CHECK (status IN ('AVAILABLE', 'OCCUPIED'))
);

CREATE TABLE tariffs (
    tariff_id BIGSERIAL PRIMARY KEY,
    tariff_name VARCHAR(100) NOT NULL,
    first_hour_rate DECIMAL(10,2) NOT NULL,
    additional_hour_rate DECIMAL(10,2) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT positive_first_hour_rate
        CHECK (first_hour_rate >= 0),

    CONSTRAINT positive_additional_hour_rate
        CHECK (additional_hour_rate >= 0)
);

CREATE TABLE parking_sessions (
    session_id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    slot_id BIGINT NOT NULL,
    entry_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMP,
    duration_minutes INTEGER,
    amount_due DECIMAL(10,2),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',

    CONSTRAINT fk_session_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),

    CONSTRAINT fk_session_slot
        FOREIGN KEY (slot_id)
        REFERENCES parking_slots(slot_id),

    CONSTRAINT valid_session_status
        CHECK (status IN ('ACTIVE', 'COMPLETED')),

    CONSTRAINT valid_duration
        CHECK (duration_minutes IS NULL OR duration_minutes >= 0),

    CONSTRAINT valid_amount_due
        CHECK (amount_due IS NULL OR amount_due >= 0)
);

CREATE TABLE payments (
    payment_id BIGSERIAL PRIMARY KEY,
    session_id BIGINT NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_reference VARCHAR(100) UNIQUE,

    CONSTRAINT fk_payment_session
        FOREIGN KEY (session_id)
        REFERENCES parking_sessions(session_id),

    CONSTRAINT valid_payment_status
        CHECK (payment_status IN ('PENDING', 'PAID', 'FAILED')),

    CONSTRAINT valid_payment_amount
        CHECK (amount >= 0)
);

CREATE UNIQUE INDEX one_active_session_per_vehicle
ON parking_sessions(vehicle_id)
WHERE status = 'ACTIVE';

CREATE UNIQUE INDEX one_active_vehicle_per_slot
ON parking_sessions(slot_id)
WHERE status = 'ACTIVE';

CREATE INDEX idx_vehicle_registration
ON vehicles(registration_number);

CREATE INDEX idx_parking_slot_status
ON parking_slots(status);

CREATE INDEX idx_parking_session_status
ON parking_sessions(status);

CREATE INDEX idx_payment_session
ON payments(session_id);
