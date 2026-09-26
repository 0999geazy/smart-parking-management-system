INSERT INTO parking_slots (slot_number, slot_type, status)
VALUES
    ('A01', 'STANDARD', 'AVAILABLE'),
    ('A02', 'STANDARD', 'AVAILABLE'),
    ('A03', 'STANDARD', 'AVAILABLE'),
    ('A04', 'STANDARD', 'AVAILABLE'),
    ('A05', 'STANDARD', 'AVAILABLE'),
    ('B01', 'STANDARD', 'AVAILABLE'),
    ('B02', 'STANDARD', 'AVAILABLE'),
    ('B03', 'STANDARD', 'AVAILABLE'),
    ('B04', 'STANDARD', 'AVAILABLE'),
    ('B05', 'STANDARD', 'AVAILABLE');

INSERT INTO tariffs (
    tariff_name,
    first_hour_rate,
    additional_hour_rate,
    active
)
VALUES (
    'Standard Parking',
    100.00,
    50.00,
    TRUE
);
