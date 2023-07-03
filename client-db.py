import psycopg2
from pprint import pprint

def delete_db(con, cur):
    cur.execute("""
        DROP TABLE clients, client_phone CASCADE;
        """)
    
def create_db(con, cur):
# Функция, создающая структуру БД (таблицы).
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
            );""")


def add_client(con, cur, name, last_name, email, number=None):
# Функция, позволяющая добавить нового клиента.
    cur.execute("""INSERT INTO clients(name, last_name, email) VALUES(%s, %s, %s);""", (name, last_name, email))
    
        
def add_phone(con, cur, client_id, number):
# Функция, позволяющая добавить телефон для существующего клиента.
    cur.execute("""INSERT INTO client_phone(client_id, number) VALUES(%s, %s);
            """, (client_id, number))
def change_client_info(con, cur, client_id, name=None, last_name=None, email=None, number=None):
# Функция, позволяющая изменить данные о клиенте.
    if name is None:
        pass
    else:
        cur.execute("""
            UPDATE clients name=%s WHERE client_id=%s;
            """, (name, client_id))
    if last_name is None:
        pass
    else:
        cur.execute("""
            UPDATE clients last_name=%s WHERE client_id=%s;
            """, (last_name, client_id))
    if email is None:
        pass
    else:
        cur.execute("""
            UPDATE clients email=%s WHERE client_id=%s;
            """, (email, client_id))
    if number is None:
        pass
    else:
        cur.execute("""
            UPDATE client_phone number=%s WHERE client_id=%s;
            """, (number, client_id))
def delete_phone(con, cur, client_id, number):
# Функция, позволяющая удалить телефон для существующего клиента.
    cur.execute("""
    DELETE FROM client_phone WHERE client_id=%s AND number=%s;
    """, (client_id, number))

def delete_client(con, cur, client_id):
# Функция, позволяющая удалить существующего клиента.
    cur.execute("""
        DELETE FROM client_phone WHERE client_id=%s
    """, (client_id,))
    cur.execute("""
        DELETE FROM clients WHERE client_id=%s
    """, (client_id,))

def find_client(con, cur, name=None, last_name=None, email=None, number=None):
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if number is None:
        cur.execute("""
            SELECT c.client_id, c.name, c.last_name, c.email, cp.number FROM clients c
            LEFT JOIN client_phone cp ON c.client_id = cp.client_id
            WHERE c.name LIKE %s AND c.last_name LIKE %s
            AND c.email LIKE %s
            """, (name, last_name, email))
    else:
        cur.execute("""
            SELECT c.client_id, c.name, c.last_name, c.email, cp.number FROM clients c
            LEFT JOIN client_phone cp ON c.client_id = cp.client_id
            WHERE c.name LIKE %s AND c.last_name LIKE %s
            AND c.email LIKE %s AND cp.number like %s
            """, (name, last_name, email, last_name))
    return cur.fetchall()

if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="") as con:
        with con.cursor() as cur:
            delete_db(cur)
            create_db(con, cur)
            add_client(con, cur, "Micheal", "Dobrick", "heuyy38ryhdf@gmail.com")
            add_phone(con, cur, 1, "79877876543")
            change_client_info(con, cur, 1, "Loren", "Dobric", "heuyy38ryhdf@yahoo.com")
            change_client_info(con, cur, 1, "Lauren")
            delete_phone(con, cur, 1, "79877876543")
            pprint(find_client(con, cur, None, None, "heuyy38ryhdf@yahoo.com"))
            pprint(find_client(con, cur, "Loren"))
            pprint(find_client(con, cur, None, None, None, "79877876543"))
    con.close()
