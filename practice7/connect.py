import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="your_user",
        password="1234",
        host="localhost",
        port="5432"
    )