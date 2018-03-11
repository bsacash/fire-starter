import sqlite3

def get_url(url_id,db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT url from moz_places where id == {id};".format(db=db, id=url_id))
    data = cur.fetchone()
    return data

def query(q,db,mode="all"):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(q)
        if mode == "all":
            data = cur.fetchall()
        else:
            data = cur.fetchone()
        return data
    # except sqlite3.Error, e:
    #     return e.args[0]
    except:
        return "ERROR"
    finally:
        if con:
            con.close()

def read_config(file_name):
    f = open(file_name, 'r')
    path = f.read().split(',')[0]
    return path

# fk = url lookup id in moz_places table (url_table)
# type 1 == bookmark
# type 2 == folder
# parent == folder id it belongs to


#url_table
# id, url, title,
