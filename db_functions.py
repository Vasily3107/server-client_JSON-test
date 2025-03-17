import pyodbc
server   = 'localhost\SQLEXPRESS'
database = 'test_db'
table    = 'users'
dsn      = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

from user import User


def get_user_logins() -> list[str]:
    db_conn = pyodbc.connect(dsn)
    cursor = db_conn.cursor()

    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()

    cursor.close()
    db_conn.close()

    return list(map(lambda i: i[0], rows))


def find_user_in_db(user: User) -> bool:
    db_conn = pyodbc.connect(dsn)
    cursor = db_conn.cursor()

    cursor.execute(f'SELECT * FROM {table}')
    users = map(tuple, cursor.fetchall())

    cursor.close()
    db_conn.close()

    return (user.login, user.password) in users


def add_user_to_db(user: User) -> None:
    db_conn = pyodbc.connect(dsn)
    cursor = db_conn.cursor()

    insert_query = f'INSERT INTO {table} ([login], [password]) VALUES (?, ?)'
    values = (user.login, user.password)

    cursor.execute(insert_query, values)
    db_conn.commit()

    cursor.close()
    db_conn.close()