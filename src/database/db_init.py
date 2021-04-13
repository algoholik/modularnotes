from database.db_connect import get_db_connection

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute("drop table if exists notes;")
    cursor.execute("drop table if exists snippets;")
    cursor.execute("drop table if exists tags;")
    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("create table notes (id integer primary key, note text, updated datetime);")
    cursor.execute("create table snippets (id integer primary key, snippet text, updated datetime);")
    cursor.execute("create table tags (id integer primary key, tag text unique, updated datetime);")
    connection.commit()

def db_init():
    connection = get_db_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == '__main__':
    db_init()
