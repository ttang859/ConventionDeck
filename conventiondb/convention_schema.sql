CREATE TABLE IF NOT EXISTS convention_info (
    id TEXT PRIMARY KEY,
    convention_name TEXT,
    host_id TEXT,
    start TIMESTAMP,
    loc TEXT,
    vendor_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS registered_attendees (
    id SERIAL PRIMARY KEY,
    conv_id TEXT,
    attende_id TEXT
);

CREATE TABLE IF NOT EXISTS vendor_booths (
    id SERIAL PRIMARY KEY,
    conv_id TEXT,
    vendor_id TEXT,
    booth_number TEXT
);
