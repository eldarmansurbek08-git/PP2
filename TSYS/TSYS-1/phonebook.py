import csv
import json
import psycopg2
from datetime import datetime
from connect import get_connection

# =========================
# CONNECTION
# =========================

def get_conn():
    conn = get_connection()
    conn.autocommit = True
    return conn

# =========================
# INIT TABLES (3.1)
# =========================

def create_tables():
    conn = get_conn()
    with conn.cursor() as cur:

        cur.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """)

        cur.execute("""
        INSERT INTO groups(name)
        VALUES ('Family'),('Work'),('Friend'),('Other')
        ON CONFLICT DO NOTHING
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(100),
            birthday DATE,
            group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
            phone VARCHAR(20),
            type VARCHAR(10) CHECK (type IN ('home','work','mobile')) DEFAULT 'mobile',
            UNIQUE(contact_id, phone)
        )
        """)

    conn.close()


# =========================
# HELPERS
# =========================

def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except:
        return None


# =========================
# UPSERT CONTACT (3.3 + 3.4)
# =========================

def upsert_contact():
    name = input("Name: ")
    phone = input("Phone: ")

    if not name or not phone:
        print("Name & phone required")
        return

    email = input("Email: ") or None
    birthday = parse_date(input("Birthday (YYYY-MM-DD): "))
    p_type = input("Type (home/work/mobile): ") or "mobile"

    group = input("Group (Family/Work/Friend/Other): ") or None

    conn = get_conn()
    with conn.cursor() as cur:

        cur.execute("""
        CALL upsert_contact(%s,%s,%s,%s,%s,%s)
        """, (name, phone, p_type, email, birthday, group))

    conn.close()
    print("Saved")


# =========================
# SEARCH (3.2 + 3.4)
# =========================

def search():
    q = input("Search: ")

    conn = get_conn()
    with conn.cursor() as cur:

        cur.execute("""
        SELECT * FROM search_contacts(%s)
        """, (q,))

        rows = cur.fetchall()

    conn.close()

    for r in rows:
        print(r)


# =========================
# PAGINATION (3.2)
# =========================

def pagination():
    page_size = int(input("Page size: ") or 5)
    page = 1

    while True:
        offset = (page - 1) * page_size

        sort = input("Sort (name/birthday/created_at): ") or "name"

        conn = get_conn()
        with conn.cursor() as cur:

            cur.execute("""
            SELECT * FROM get_contacts_page(%s,%s,%s)
            """, (page_size, offset, sort))

            rows = cur.fetchall()

        conn.close()

        print(f"\nPAGE {page}")
        for r in rows:
            print(r)

        cmd = input("[n]ext [p]rev [q]uit: ")

        if cmd == "n":
            page += 1
        elif cmd == "p" and page > 1:
            page -= 1
        elif cmd == "q":
            break


# =========================
# CSV IMPORT (3.3)
# =========================

def import_csv():
    path = input("CSV file: ")

    conn = get_conn()

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get("name")
            phone = row.get("phone")
            email = row.get("email")
            birthday = parse_date(row.get("birthday"))
            p_type = row.get("type") or "mobile"
            group = row.get("group")

            if not name or not phone:
                continue

            with conn.cursor() as cur:
                cur.execute("""
                CALL upsert_contact(%s,%s,%s,%s,%s,%s)
                """, (name, phone, p_type, email, birthday, group))

    conn.close()
    print("CSV imported")


# =========================
# JSON EXPORT (3.3)
# =========================

def export_json():
    conn = get_conn()

    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM v_contacts
        """)

        rows = cur.fetchall()

    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "birthday": str(r[3]),
            "group": r[4],
            "phones": r[5],
            "created_at": str(r[6])
        })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Export done")


# =========================
# JSON IMPORT (3.3)
# =========================

def import_json():
    path = input("JSON file: ")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    conn = get_conn()

    for c in data:
        name = c["name"]
        email = c.get("email")
        birthday = parse_date(c.get("birthday"))
        group = c.get("group")

        phones = c.get("phones", [])

        with conn.cursor() as cur:

            cur.execute("""
            INSERT INTO contacts(name,email,birthday)
            VALUES (%s,%s,%s)
            ON CONFLICT (name) DO UPDATE
            SET email=EXCLUDED.email,
                birthday=EXCLUDED.birthday
            RETURNING id
            """, (name,email,birthday))

            cid = cur.fetchone()[0]

            if group:
                cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
                g = cur.fetchone()
                if g:
                    cur.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (g[0],cid))

            for p in phones:
                cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES (%s,%s,%s)
                ON CONFLICT DO NOTHING
                """, (cid, p["phone"], p.get("type","mobile")))

    conn.close()
    print("Imported")


# =========================
# MENU
# =========================

def main():
    create_tables()

    while True:
        print("""
1 Add contact
2 Search
3 Pagination
4 Import CSV
5 Export JSON
6 Import JSON
0 Exit
""")

        c = input("> ")

        if c == "1":
            upsert_contact()
        elif c == "2":
            search()
        elif c == "3":
            pagination()
        elif c == "4":
            import_csv()
        elif c == "5":
            export_json()
        elif c == "6":
            import_json()
        elif c == "0":
            break


if __name__ == "__main__":
    main()