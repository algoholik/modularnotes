from database.db_connect import get_db_connection
import utils

DATABASE_SCHEMA_FILE = utils.get_file_path("database/monoa-schema.sql")

def drop_tables(connection) -> None:
    ''' Clean up database file when making a new build '''
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Notes;")
    cursor.execute("DROP TABLE IF EXISTS Snips;")
    cursor.execute("DROP TABLE IF EXISTS Tags;")
    cursor.execute("DROP TABLE IF EXISTS Tagging;")
    cursor.execute("DROP TABLE IF EXISTS Categories;")
    cursor.execute("DROP TABLE IF EXISTS Categorisation;")
    connection.commit()

def create_tables(connection) -> None:
    ''' Create database tables from schema file '''
    cursor = connection.cursor()
    with open(DATABASE_SCHEMA_FILE) as schema_file:
        cursor.executescript(schema_file.read())
    connection.commit()

def db_init() -> None:
    ''' Initialize database file '''
    connection = get_db_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == '__main__':
    db_init()
