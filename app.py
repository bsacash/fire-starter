from flask import Flask, render_template, request
from helper import query, read_config, get_contents

from helper import Bookmark, Folder

app = Flask(__name__)

@app.route('/')
def index():
    db = read_config("config.config")

    # Get Bookmarks Toolbar ID
    q = "SELECT id from moz_bookmarks where title == 'Bookmarks Toolbar';"
    master_id = query(q,db,mode="one")[0]

    folders, bookmarks = get_contents(master_id, db)

    return render_template('index.html', bookmarks=bookmarks, folders=folders)

@app.route('/folder', methods=['POST'])
def folder():
    folder_id = request.form['folder_click']

    db = read_config("config.config")

    folders, bookmarks = get_contents(folder_id,db)

    return render_template('index.html', bookmarks=bookmarks, folders=folders)

if __name__ == "__main__":
    app.run()
