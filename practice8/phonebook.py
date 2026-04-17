from connect import get_connection

conn = get_connection()
cur = conn.cursor()


def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute("CALL add_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Inserted!")


def update_contact():
    name = input("Enter name: ")
    phone = input("Enter new phone: ")

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Updated!")


def delete_contact():
    value = input("Enter name or phone: ")

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    print("Deleted!")


def search_contact():
    text = input("Search: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (text,))
    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1 - Add")
        print("2 - Update (Upsert)")
        print("3 - Delete")
        print("4 - Search")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            update_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            search_contact()
        elif choice == "0":
            break
        else:
            print("Wrong option!")


main()

cur.close()
conn.close()