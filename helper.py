import sqlite3
import tldextract
import string

class Folder:
    def __init__(self, folder_id, title, parent="None"):
        self.id = folder_id
        self.title = title
        self.parent = parent
        self.color_start = [1,1,1]
        self.color_mid = [1,1,1]
        self.color_end = [1,1,1]

    # Generate RGB values from title name
    def colors(self):
        try: # TODO account for strings of two letters or less
            start = list(map(lambda x:x, self.title[:3].lower()))
            end = list(map(lambda x:x, self.title[-3:].lower()))
        except:
            start = ["a","a","a"]
            end = ["z","z","z"]

        color_map = {char:int(str(index)+"5") for index, char in enumerate(string.ascii_lowercase)}
        # TODO breaks on non ascii lowercase
        start = list(map(lambda x: color_map[x],start))
        end = list(map(lambda x: color_map[x],end))

        # Generate middle RGB value that leads towards "end" RGB value
        mid = list(map(lambda x:round(sum(x)/3), list(zip(start,end,end))))
        self.color_start = start
        self.color_mid = mid
        self.color_end = end




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

def get_contents(parent, db):
    # Fetch all folder items in the parent folder
    q = "SELECT id, type, parent, title from moz_bookmarks where parent == {0} and type==2;".format(parent)
    folders = query(q,db,mode="all")
    folders = [Folder(folder_id = f[0], title = f[3]) for f in folders]

    # Fetch all bookmark items in the parent folder
    q = "SELECT id, type, fk, parent, title from moz_bookmarks where parent=={0} and type==1;".format(parent)
    bookmarks = query(q,db,mode="all")
    bookmarks = [Bookmark(url_id = b[2], title = b[4]) for b in bookmarks]

    # Fetch Bookmark urls (batch)
    url_ids = tuple([bm.id for bm in bookmarks])
    if len(url_ids) == 0: # empty case
        q = "SELECT id, url from moz_places WHERE id in ()"
    elif len(url_ids) < 2: # handle 1-tuple
        q = "SELECT id, url from moz_places WHERE id in ({0})".format(url_ids[0])
    else:
        q = "SELECT id, url from moz_places WHERE id in {0}".format(url_ids)
    r = query(q, db, mode="all")
    r = {entry[0]:entry[1] for entry in r}

    #Join urls with Bookmarks
    for bm in bookmarks:
        temp_id = bm.id
        try:
            bm.url = r[bm.id]
        except:
            pass

    return (folders, bookmarks)

# Check if a search string is a URL
def url_or_search(string,base_search_url):
    string_split = string.split()
    if len(string_split) > 1:
        return base_search_url + str(string)
    elif len(string_split) == 1:
        subdomain, domain, suffix =  tldextract.extract(string)
        if suffix:
            if subdomain: # ignores if an http is already present
                return "https://" + str(string)
            else:
                return "https://www." + str(string)
        else:
            return base_search_url + str(string)
    else:
        return base_search_url + str(string)





# fk = url lookup id in moz_places table (url_table)
# type 1 == bookmark
# type 2 == folder
# parent == folder id it belongs to


#url_table
# id, url, title,
