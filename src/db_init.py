from db_connect import get_db_connection

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute('''
        drop table if exists notes;
    ''')
    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute('''
        create table notes (
            id integer primary key,
            note text
        );
    ''')
    connection.commit()

def db_init():
    connection = get_db_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == '__main__':
    db_init()
