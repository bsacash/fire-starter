import sqlite3

class Folder:
    def __init__(self, folder_id, title, parent="None"):
        self.id = folder_id
        self.title = title
        self.parent = parent

class Bookmark:
    def __init__(self, url_id, title, url="None", parent="None"):
        self.id = url_id
        self.title = title
        self.url = url
        self.parent = parent

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

def get_contents(parent):
    # Fetch all folder items in the parent folder
    q = "SELECT id, type, parent, title from moz_bookmarks where parent == {0} and type==2;".format(parent)
    folders = query(q,db,mode="all")
    folders = [Folder(folder_id = f[0], title = f[3]) for f in folders]




# fk = url lookup id in moz_places table (url_table)
# type 1 == bookmark
# type 2 == folder
# parent == folder id it belongs to


#url_table
# id, url, title,
