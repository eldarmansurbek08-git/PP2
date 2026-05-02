-- ============================================================
--  PhoneBook Extended — Stored Procedures & Functions (Practice 9)
--  Replaces / extends the Practice 8 objects.
--  Run schema.sql first.
-- ============================================================


-- ────────────────────────────────────────────────────────────
-- HELPER VIEW: full contact detail (used by multiple functions)
-- ────────────────────────────────────────────────────────────
CREATE OR REPLACE VIEW v_contacts AS
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name                                                         AS group_name,
        STRING_AGG(
            ph.phone || ' [' || COALESCE(ph.type, '?') || ']',
            ', '
            ORDER BY ph.type
        )                                                              AS phones,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g  ON g.id  = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at;


-- ============================================================
-- FUNCTION 1 — search_contacts(p_query)
-- Extends Practice 8: searches name, email, AND all phones.
-- ============================================================
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id         INT,
    name       VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            STRING_AGG(
                ph.phone || ' [' || COALESCE(ph.type, '?') || ']',
                ', '
                ORDER BY ph.type
            ),
            c.created_at
        FROM contacts c
        LEFT JOIN groups g  ON g.id = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        WHERE c.name  ILIKE '%' || p_query || '%'
           OR c.email ILIKE '%' || p_query || '%'
           OR EXISTS (
                SELECT 1 FROM phones p2
                WHERE  p2.contact_id = c.id
                  AND  p2.phone ILIKE '%' || p_query || '%'
              )
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY c.name;
END;
$$ LANGUAGE plpgsql;

-- Usage:
--   SELECT * FROM search_contacts('Ali');
--   SELECT * FROM search_contacts('gmail');
--   SELECT * FROM search_contacts('+7701');


-- ============================================================
-- FUNCTION 2 — get_contacts_page(limit, offset, sort_col)
-- Replaces Practice 8 version; now returns rich contact rows
-- and supports dynamic ORDER BY.
-- ============================================================
CREATE OR REPLACE FUNCTION get_contacts_page(
    page_limit  INT,
    page_offset INT,
    sort_col    TEXT DEFAULT 'name'   -- 'name' | 'birthday' | 'created_at'
)
RETURNS TABLE(
    id         INT,
    name       VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT,
    created_at TIMESTAMPTZ
) AS $$
DECLARE
    safe_col TEXT;
BEGIN
    -- Whitelist sort columns to prevent SQL injection
    safe_col := CASE sort_col
                    WHEN 'birthday'   THEN 'birthday'
                    WHEN 'created_at' THEN 'created_at'
                    ELSE                   'name'
                END;

    RETURN QUERY EXECUTE format(
        $q$
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            STRING_AGG(
                ph.phone || ' [' || COALESCE(ph.type,'?') || ']',
                ', '
                ORDER BY ph.type
            ),
            c.created_at
        FROM contacts c
        LEFT JOIN groups g  ON g.id = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY c.%I NULLS LAST
        LIMIT  %L
        OFFSET %L
        $q$,
        safe_col, page_limit, page_offset
    );
END;
$$ LANGUAGE plpgsql;

-- Usage:
--   SELECT * FROM get_contacts_page(10, 0);
--   SELECT * FROM get_contacts_page(10, 0, 'birthday');


-- ============================================================
-- PROCEDURE 1 — upsert_contact  (replaces Practice 8 version)
-- Upserts the contact record AND adds / updates a phone.
-- ============================================================
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name     VARCHAR,
    p_phone    VARCHAR,
    p_type     VARCHAR DEFAULT 'mobile',
    p_email    VARCHAR DEFAULT NULL,
    p_birthday DATE    DEFAULT NULL,
    p_group    VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
    v_group_id   INT;
BEGIN
    -- Resolve group name → id
    IF p_group IS NOT NULL THEN
        SELECT id INTO v_group_id FROM groups WHERE name = p_group;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Group "%" not found. Available: Family, Work, Friend, Other', p_group;
        END IF;
    END IF;

    -- Upsert contact (name is UNIQUE key)
    INSERT INTO contacts(name, email, birthday, group_id)
    VALUES (p_name, p_email, p_birthday, v_group_id)
    ON CONFLICT (name) DO UPDATE
        SET email    = COALESCE(EXCLUDED.email,    contacts.email),
            birthday = COALESCE(EXCLUDED.birthday, contacts.birthday),
            group_id = COALESCE(EXCLUDED.group_id, contacts.group_id)
    RETURNING id INTO v_contact_id;

    -- Add / update the phone
    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, COALESCE(p_type, 'mobile'))
    ON CONFLICT (contact_id, phone) DO UPDATE
        SET type = EXCLUDED.type;

    RAISE NOTICE '[UPSERT] % — % (%)', p_name, p_phone, COALESCE(p_type, 'mobile');
END;
$$;

-- Usage:
--   CALL upsert_contact('Alice', '+77001112233', 'mobile', 'alice@gmail.com', '1990-05-20', 'Friend');
--   CALL upsert_contact('Alice', '+77009876543', 'work');   -- just add a work phone


-- ============================================================
-- PROCEDURE 2 — insert_many_contacts  (replaces Practice 8 version)
-- Parallel arrays: names, phones, phone types.
-- Returns invalid_entries as OUT param.
-- ============================================================
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names   TEXT[],
    p_phones  TEXT[],
    p_types   TEXT[],          -- pass NULL to default all types to 'mobile'
    OUT invalid_entries TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i           INT;
    v_name      TEXT;
    v_phone     TEXT;
    v_type      TEXT;
    v_cid       INT;
    bad         TEXT[] := '{}';
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Names and phones arrays must have equal length';
    END IF;

    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name  := TRIM(p_names[i]);
        v_phone := TRIM(p_phones[i]);
        v_type  := COALESCE(TRIM(p_types[i]), 'mobile');

        -- Validate phone
        IF v_phone !~ '^\+?[0-9]{10,15}$' THEN
            bad := array_append(bad, v_name || ' | ' || v_phone);
            RAISE NOTICE '[INVALID] % — bad phone: %', v_name, v_phone;
            CONTINUE;
        END IF;

        -- Validate type
        IF v_type NOT IN ('home', 'work', 'mobile') THEN
            v_type := 'mobile';
        END IF;

        -- Upsert contact then phone
        INSERT INTO contacts(name) VALUES (v_name)
        ON CONFLICT (name) DO NOTHING
        RETURNING id INTO v_cid;

        IF v_cid IS NULL THEN
            SELECT id INTO v_cid FROM contacts WHERE name = v_name;
        END IF;

        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_cid, v_phone, v_type)
        ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type;
    END LOOP;

    invalid_entries := CASE
        WHEN array_length(bad, 1) IS NULL THEN 'None'
        ELSE array_to_string(bad, ' | ')
    END;
END;
$$;

-- Usage:
--   CALL insert_many_contacts(
--       ARRAY['Bob','Eve','BadGuy'],
--       ARRAY['+77771234567','+77779876543','not-a-phone'],
--       ARRAY['work','mobile','mobile'],
--       NULL
--   );


-- ============================================================
-- PROCEDURE 3 — delete_contact  (replaces Practice 8 version)
-- Deletes from contacts; phones are removed via CASCADE.
-- ============================================================
CREATE OR REPLACE PROCEDURE delete_contact(
    p_username VARCHAR DEFAULT NULL,
    p_phone    VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
DECLARE
    v_cid  INT;
    v_name VARCHAR;
BEGIN
    IF p_username IS NOT NULL THEN
        DELETE FROM contacts
        WHERE  name = p_username
        RETURNING id, name INTO v_cid, v_name;

    ELSIF p_phone IS NOT NULL THEN
        SELECT c.id, c.name INTO v_cid, v_name
        FROM   contacts c
        JOIN   phones   p ON p.contact_id = c.id
        WHERE  p.phone = p_phone
        LIMIT  1;

        IF v_cid IS NOT NULL THEN
            DELETE FROM contacts WHERE id = v_cid;
        END IF;

    ELSE
        RAISE EXCEPTION 'Provide either p_username or p_phone';
    END IF;

    IF v_name IS NOT NULL THEN
        RAISE NOTICE '[DELETED] %', v_name;
    ELSE
        RAISE NOTICE '[NOT FOUND] No matching contact';
    END IF;
END;
$$;

-- Usage:
--   CALL delete_contact(p_username := 'Alice');
--   CALL delete_contact(p_phone    := '+77001112233');


-- ============================================================
-- PROCEDURE 4 (NEW) — add_phone
-- Adds a new phone number (or updates its type) for an existing contact.
-- ============================================================
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_cid INT;
BEGIN
    SELECT id INTO v_cid FROM contacts WHERE name = p_contact_name;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile (got: %)', p_type;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_cid, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type;

    RAISE NOTICE '[PHONE ADDED] % — % (%)', p_contact_name, p_phone, p_type;
END;
$$;

-- Usage:
--   CALL add_phone('Alice', '+77009998877', 'work');


-- ============================================================
-- PROCEDURE 5 (NEW) — move_to_group
-- Assigns a contact to a group; creates the group if absent.
-- ============================================================
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_gid INT;
BEGIN
    -- Create group if it doesn't exist yet
    INSERT INTO groups(name) VALUES (p_group_name) ON CONFLICT DO NOTHING;
    SELECT id INTO v_gid FROM groups WHERE name = p_group_name;

    UPDATE contacts
    SET    group_id = v_gid
    WHERE  name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    RAISE NOTICE '[MOVED] % → group "%"', p_contact_name, p_group_name;
END;
$$;

-- Usage:
--   CALL move_to_group('Alice', 'Family');
--   CALL move_to_group('Bob',   'Colleagues');   -- creates group Colleagues