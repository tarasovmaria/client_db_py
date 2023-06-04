import psycopg2
conn = psycopg2.connect(database="clients_db", user="postgres", password="")
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(60) NOT NULL,
        last_name VARCHAR(60) NOT NULL,
        email VARCHAR(60) UNIQUE NOT NULL
        );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS client_phone(
        phone_id SERIAL PRIMARY KEY,
        number VARCHAR(11) UNIQUE NOT NULL,
        client_id INTEGER NOT NULL,
        FOREIGN KEY (client_id) EFERENCES clients (client_id)
        );
        """)
        conn.commit()

def add_client(conn, name, last_name, email, number=None):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO clients(name, last_name, email) VALUES(%s, %s, %s);""", (name, last_name, email))
        conn.commit()
        print(cur.fetchall())

def add_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO client_phone(client_id, number) VALUES(%s, %s);
    """, (client_id, number))
        conn.commit()
        print(cur.fetchall())

conn.close()