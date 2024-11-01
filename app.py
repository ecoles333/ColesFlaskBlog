import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'



# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #connect to db
    conn=  get_db_connection()
    #exec query to read all posts
    posts = conn.execute('SELECT * FROM posts').fetchall()
    #close connection
    conn.close()
    #send posts to index.html template for display
    return render_template('index.html', posts=posts)

# route to create a post
@app.route('/create/', methods= ('GET', 'POST'))
def create():
    if request.method == 'POST':
        #get title and content of post
        title = request.form['title']
        content = request.form['content']
        #stay on page and display error if no content submited

        #else make a db conn and insert new data
        if not title:
            flash("Title Required")
        elif not content:
            flash("Content required")
        else:
            conn = get_db_connection()
            #insert new data
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


app.run()