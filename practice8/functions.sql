CREATE OR REPLACE FUNCTION search_contacts(p TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.name, pb.phone
    FROM phonebook pb
    WHERE pb.name ILIKE '%' || p || '%'
       OR pb.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM phonebook
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;