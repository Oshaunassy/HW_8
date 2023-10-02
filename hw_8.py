import sqlite3

import cursor as cursor


def create_connection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


def insert_counties(conn, title):
    sql = '''INSERT INTO countries
    (title)
    VALUES(?)
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (title,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def insert_cities(conn, title, area, country_id):
    sql = '''INSERT INTO cities
    (title, area, country_id)
    VALUES(?, ?, ?)
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (title, area, country_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def insert_employees(conn, first_name, last_name, city_id):
    sql = '''INSERT INTO employees
    (first_name, last_name, city_id)
    VALUES(?, ?, ?)
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (first_name, last_name, city_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def display_cities(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM cities")
        cities = cursor.fetchall()
        if cities:
            print("Список городов:")
            for city_id, city_title in cities:
                print(f"{city_id}: {city_title}")
        else:
            print("В базе данных нет городов.")
    except sqlite3.Error as e:
        print(e)


def display_employees_by_city_id(conn, city_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.first_name, e.last_name, c.title AS country, ci.title AS city, ci.area
            FROM employees e
            JOIN cities ci ON e.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            WHERE ci.id = ?
        """, (city_id,))
        employees = cursor.fetchall()
        if employees:
            print(f"Сотрудники в выбранном городе:")
            for first_name, last_name, country, city, area in employees:
                print(f"Имя: {first_name}, Фамилия: {last_name}, Страна: {country}, Город: {city}, Площадь города: {area}")
            else:
                print("Сотрудники в выбранном городе не найдены.")

    except sqlite3.Error as e:
        print(e)


connection = create_connection('mydb.db')

if connection is not None:
    sql_create_countries = '''
        CREATE TABLE countries (
        id integer primary key autoincrement,
        title VARCHAR (200) NOT NULL
        )
        '''
    create_table(connection, sql_create_countries)
    insert_counties(connection, 'Kyrgyzstan')
    insert_counties(connection, 'Germany')
    insert_counties(connection, 'China')

    sql_create_cities = '''
                CREATE TABLE cities (
                id integer primary key autoincrement,
                title VARCHAR (200) NOT NULL,
                area FLOAT not null default 0,
                country_id integer,
                FOREIGN KEY (country_id) REFERENCES countries(id)
                )
                '''
    create_table(connection, sql_create_cities)
    insert_cities(connection, 'Bishkek', 127, 1)
    insert_cities(connection, 'Berlin', 891.8, 2)
    insert_cities(connection, 'Pekin', 16410, 3)

sql_create_employees = '''
        CREATE TABLE employees (
        id integer primary key autoincrement,
        first_name VARCHAR (200) NOT NULL,
        last_name VARCHAR (200) NOT NULL,
        city_id integer,
        FOREIGN KEY (city_id) REFERENCES cities(id)
        )
        '''
create_table(connection, sql_create_employees)
insert_employees(connection, 'Askar', 'Bakirov', 1)
insert_employees(connection, 'Henry', 'Freeman', 2)
insert_employees(connection, 'Shao', 'Leen', 3)
insert_employees(connection, 'Arthur', 'Osmonov', 1)
insert_employees(connection, 'Nicole', 'Kidman', 2)
insert_employees(connection, 'Ostap', 'Bender', 3)
insert_employees(connection, 'Pavel', 'Nikiforov', 1)
insert_employees(connection, 'Peter', 'Otta', 2)

print(
    "Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
display_cities(connection)

while True:
    city_id = int(input("Введите ID города (или 0 для выхода): "))
    if city_id == 0:
        break
    display_employees_by_city_id(connection, city_id)

connection.close()
