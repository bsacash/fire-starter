from flask import Flask, render_template, request, redirect
from helper import query, read_config, get_contents, url_or_search

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

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_input']
    base_search_url = "http://www.duckduckgo.com/?q="
    r = url_or_search(search_term, base_search_url)
    return redirect(r)

if __name__ == "__main__":
    app.run()
