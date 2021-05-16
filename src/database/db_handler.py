import datetime
from database.db_connect import get_db_connection

CONNECTION = get_db_connection()

def create_snip(sniptype: int, content: str, modified: datetime):
    '''
    Create new snip in database and return it
    '''
    cur = CONNECTION.cursor()
    sql = """   INSERT INTO Snips (sniptype, content, modified)
                VALUES (:sniptype, :content, :modified) """
    inj = {
        "sniptype": sniptype,
        "content": content,
        "modified": modified
    }
    lid = cur.execute(sql, inj).lastrowid
    sql = "SELECT * FROM Snips WHERE id=:lid"
    res = cur.execute(sql, {"lid": lid}).fetchone()
    CONNECTION.commit()
    return res

def update_snip(id: int, sniptype: int, content: str, modified: datetime):
    '''
    Update snip by id in database
    '''
    cur = CONNECTION.cursor()
    sql =   """
                UPDATE Snips
                SET sniptype=:sniptype, content=:content, modified=:modified
                WHERE id=:id
            """
    res = cur.execute(sql, {"sniptype": sniptype,
                            "content": content,
                            "modified": modified,
                            "id": id})
    CONNECTION.commit()

def load_snips():
    '''
    Return as dict() all snips drom database
    '''
    cur = CONNECTION.cursor()
    sql = "SELECT * FROM Snips"
    snips = cur.execute(sql).fetchall()
    CONNECTION.commit()
    return snips

def create_note(title: str, contents: list, modified: datetime):
    '''
    Create note in database and return it
    '''
    cur = CONNECTION.cursor()
    sql =   """
                INSERT INTO Notes (title, contents, modified)
                VALUES (:title, :contents, :modified)
            """
    inj =   {
                "title": title,
                "contents": ";".join([str(snip) for snip in contents]),
                "modified": modified
            }
    lid = cur.execute(sql, inj).lastrowid
    sql = "SELECT * FROM Notes WHERE id=:lid"
    res = cur.execute(sql, {"lid": lid}).fetchone()
    CONNECTION.commit()
    return res

def update_note(id: int, title: str, contents: list, modified: datetime):
    '''
    Update note
    '''
    cur = CONNECTION.cursor()
    sql =   """
                    UPDATE Notes
                    SET title=:title, contents=:contents, modified=:modified
                    WHERE id=:id
                """
    res = cur.execute(sql, {"title": title,
                            "contents": ";".join([str(snip) for snip in contents]),
                            "modified": modified,
                            "id": id})
    CONNECTION.commit()

def load_notes():
    '''
    Return as dict() all notes from database
    '''
    cur = CONNECTION.cursor()
    sql = "SELECT * FROM Notes"
    notes = cur.execute(sql).fetchall()
    CONNECTION.commit()
    return notes
