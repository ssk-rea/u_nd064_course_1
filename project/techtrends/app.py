import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
import init_db

num_count = 0


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    obj_post = connection.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    connection.close()
    return obj_post


def get_all_posts():
    connection = get_db_connection()
    list_posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return list_posts


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    list_posts = get_all_posts()
    app.logger.debug(f"All the posts retrieved.")

    return render_template('index.html', posts=list_posts)


@app.route('/init')
def init():
    init_db.init_local_db()
    app.logger.debug(f"DB initialized successfully.")
    return {'status': 'DB initialized successfully.'}


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def get_existing_post(post_id):
    obj_post = get_post(post_id)
    # print(f"post: {obj_post}, type: {type(obj_post)}, {obj_post[0]}, {obj_post['title']}")
    if obj_post is None:

        app.logger.debug(f"A non-existing article is accessed: {post_id}")
        return render_template('404.html'), 404
    else:

        app.logger.debug(f"An existing article is accessed: {post_id} {obj_post['title']}")
        return render_template('post.html', post=obj_post)


# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/about1')
def about1():
    return render_template('about1.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()

            app.logger.debug(f"New article created: {title}")

            return redirect(url_for('index'))

    return render_template('create.html')


# ================================================
@app.route('/healthz', methods=['GET'])
def healthz():
    response = app.response_class(
        response=json.dumps({
            "result": "OK - healthy"
        }),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Healthz request successful.')
    app.logger.debug('DEBUG message')
    return response


def count_db_conn():
    global num_count
    num_count += 1
    return num_count


def count_posts():
    list_posts = get_all_posts()
    return len(list_posts)


@app.route('/metrics', methods=['GET'])
def metrics():
    num_conn = count_db_conn()
    app.logger.debug(f'num_conn: {num_conn}')

    num_posts = count_posts()
    app.logger.debug(f'num_posts: {num_posts}')

    dict_metrics = {
        "db_connection_count": num_conn,
        "post_count": num_posts
    }
    app.logger.debug(f'{dict_metrics}')

    response = app.response_class(
        response=json.dumps(dict_metrics),
        status=200,
        mimetype='application/json'
    )

    app.logger.info('Metrics request successful.')
    return response


# ================================================

# start the application on port 3111
if __name__ == "__main__":
    # get_existing_post(1)
    logging.basicConfig(filename='py_app.log', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=3111)
