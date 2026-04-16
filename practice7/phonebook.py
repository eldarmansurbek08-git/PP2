import psycopg2

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="eldar.mansurbek21.06icloud.com",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


def insert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Inserted!")


def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE name=%s",
        (new_phone, name)
    )
    conn.commit()
    print("Updated!")


def delete_contact():
    name = input("Enter name to delete: ")

    cur.execute(
        "DELETE FROM phonebook WHERE name=%s",
        (name,)
    )
    conn.commit()
    print("Deleted!")


def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1 - Add contact")
        print("2 - Update contact")
        print("3 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_contact()
        elif choice == "2":
            update_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Wrong option!")


main()

cur.close()
conn.close()