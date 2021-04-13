import datetime
from database.db_connect import get_db_connection

connection = get_db_connection()

def insert_snippet(content: str):
    cur = connection.cursor()
    sql = "insert into snippets (snippet, updated) values (:content, :updated)"
    lid = cur.execute(sql, {"content": content, "updated": datetime.datetime.now()}).lastrowid
    sql = "select * from snippets where id=:lid"
    res = cur.execute(sql, {"lid": lid}).fetchone()
    connection.commit()
    return res

def update_snippet(id: int, content: str):
    cur = connection.cursor()
    sql = "update snippets set snippet=:content, updated=:updated where id=:id"
    lid = cur.execute(sql, {"content": content, "updated": datetime.datetime.now(), "id": id}).lastrowid
    sql = "select * from snippets where id=:lid"
    res = cur.execute(sql, {"lid": lid}).fetchone()
    connection.commit()
    return res

def load_snippets():
    cur = connection.cursor()
    sql = "select * from snippets"
    snippets = cur.execute(sql).fetchall()
    connection.commit()
    for snippet in snippets:
        yield { "id":       snippet['id'], 
                "snippet":  snippet['snippet'], 
                "updated":  snippet['updated']
                }


