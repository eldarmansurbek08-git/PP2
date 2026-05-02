-- =========================
-- PHONEBOOK SCHEMA 
-- =========================

-- DROP TABLES (optional for reset)
DROP TABLE IF EXISTS phones CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS groups CASCADE;

-- =========================
-- GROUPS TABLE
-- =========================
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups(name)
VALUES ('Family'),('Work'),('Friend'),('Other')
ON CONFLICT DO NOTHING;


-- =========================
-- CONTACTS TABLE
-- =========================
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


-- =========================
-- PHONES TABLE (1 → many)
-- =========================
CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) DEFAULT 'mobile'
        CHECK (type IN ('home','work','mobile')),

    UNIQUE(contact_id, phone)
);