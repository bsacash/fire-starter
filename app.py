from flask import Flask, render_template, request
from helper import query, read_config

from helper import Bookmark, Folder

app = Flask(__name__)

@app.route('/',)
def index():
    db = read_config("config.config")

    # Get Bookmarks Toolbar ID
    q = "SELECT id from moz_bookmarks where title == 'Bookmarks Toolbar';"
    master_id = query(q,db,mode="one")[0]

    # Fetch all folder items in the Bookmarks Toolbar folder
    q = "SELECT id, type, parent, title from moz_bookmarks where parent == {0} and type==2;".format(master_id)
    folders = query(q,db,mode="all")
    folders = [Folder(folder_id = f[0], title = f[3]) for f in folders]

    #BOOKMARKS
    # Fetch all bookmark items in the Bookmarks Toolbar folder
    q = "SELECT id, type, fk, parent, title from moz_bookmarks where parent=={0} and type==1;".format(master_id)
    bookmarks = query(q,db,mode="all")
    bookmarks = [Bookmark(url_id = b[2], title = b[4]) for b in bookmarks]

    # Fetch bookmark urls (batch)
    url_ids = tuple([bm.id for bm in bookmarks])
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

    return render_template('index.html', bookmarks=bookmarks, folders=folders)

if __name__ == "__main__":
    app.run()
