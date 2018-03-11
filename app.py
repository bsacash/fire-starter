from flask import Flask, render_template, request
from helper import query, get_url, read_config

app = Flask(__name__)

@app.route('/',)
def index():
    db = read_config("config.config")

    # Get Bookmarks Toolbar ID
    q = "SELECT id, type, fk, parent, title from moz_bookmarks where title == 'Bookmarks Toolbar';"
    master_id = query(q,db,mode="one")[0]

    # Fetch all items in the BookMarks Toolbar folder
    q = "SELECT id, type, fk, parent, title from moz_bookmarks where parent == {0};".format(master_id)
    r = query(q,db,mode="all")

    #data2 = get_url(187,db)
    return render_template('index.html', data=r)

if __name__ == "__main__":
    app.run()
