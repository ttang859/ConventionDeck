CREATE TABLE IF NOT EXISTS convention_info (
    id TEXT PRIMARY KEY,
    convention_name TEXT,
    host_id TEXT,
    start TIMESTAMP,
    loc TEXT,
    vendor_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS registration (
    conv_id TEXT REFERENCES convention_info(id) ON DELETE CASCADE,
    attendee_id TEXT,
    PRIMARY KEY(conv_id, attendee_id)
);

CREATE TABLE IF NOT EXISTS vendor_booths (
    conv_id TEXT REFERENCES convention_info(id) ON DELETE CASCADE,
    vendor_id TEXT,
    booth_number INTEGER,
    PRIMARY KEY(conv_id, booth_number)
);
