"""
Nazaneen Baguaei,
May 19, 2026
Final Project: Student Learning Management App
"""
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# ------------------
# FILE UPLOAD CONFIG
# ------------------
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ------------------
# DATABASE CONNECTION
# ------------------
def get_db():
    conn = sqlite3.connect("flask_db.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------
# DATABASE SETUP
# ------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'academic',
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    # blog posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    # comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    # likes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            UNIQUE(post_id, user_id),
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    # images table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            subject TEXT DEFAULT 'general',
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# ------------------
# HELPER FUNCTIONS
# ------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_id():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
    user = cursor.fetchone()
    conn.close()
    return user['id']

# ------------------
# LOADING PAGE
# ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------
# LOGIN ROUTING
# ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(""" SELECT * FROM users WHERE email = ? AND password = ? """, (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password")
    return render_template("login.html")

# ------------------
# SIGNUP ROUTING
# ------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(""" INSERT INTO users (username, email, password) VALUES (?,?,?) """, (username, email, password))
            conn.commit()
            flash("Account created successfully!")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        finally:
            conn.close()
    return render_template('signup.html')

# ------------------
# DASHBOARD ROUTING
# ------------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# ------------------
# TO-DO LIST ROUTING
# ------------------
@app.route('/todo')
def todo():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY completed ASC, due_date ASC", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return render_template('todo.html', username=session['username'], tasks=tasks)

@app.route('/todo/add', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    category = request.form['category']
    due_date = request.form['due_date']
    user_id = get_user_id()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO tasks (user_id, title, category, due_date) VALUES (?,?,?,?) """, (user_id, title, category, due_date))
    conn.commit()
    conn.close()
    flash("Task added!")
    return redirect(url_for('todo'))

@app.route('/todo/complete/<int:task_id>')
def complete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

@app.route('/todo/delete/<int:task_id>')
def delete_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

# ------------------
# BLOG ROUTING
# ------------------
@app.route('/blog')
def blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT posts.*, users.username,
        (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count,
        (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) as comment_count
        FROM posts JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
    """)
    posts = cursor.fetchall()
    conn.close()
    return render_template('blog.html', username=session['username'], posts=posts)

@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        user_id = get_user_id()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO posts (user_id, title, content, category) VALUES (?,?,?,?) """, (user_id, title, content, category))
        conn.commit()
        conn.close()
        flash("Post published!")
        return redirect(url_for('blog'))
    return render_template('new_post.html', username=session['username'])

@app.route('/blog/post/<int:post_id>')
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT posts.*, users.username,
        (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) as like_count
        FROM posts JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    """, (post_id,))
    post = cursor.fetchone()
    cursor.execute("""
        SELECT comments.*, users.username FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ? ORDER BY comments.created_at ASC
    """, (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return render_template('view_post.html', username=session['username'], post=post, comments=comments)

@app.route('/blog/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    user_id = get_user_id()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO comments (post_id, user_id, content) VALUES (?,?,?) """, (post_id, user_id, content))
    conn.commit()
    conn.close()
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/blog/like/<int:post_id>')
def like_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (?,?)", (post_id, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        # already liked — unlike it
        cursor.execute("DELETE FROM likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('view_post', post_id=post_id))

# ------------------
# IMAGE UPLOAD ROUTING
# ------------------
@app.route('/upload')
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = get_user_id()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE user_id = ? ORDER BY uploaded_at DESC", (user_id,))
    images = cursor.fetchall()
    conn.close()
    return render_template('upload.html', username=session['username'], images=images)

@app.route('/upload/image', methods=['POST'])
def upload_image():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == "":
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        subject = request.form.get('subject', 'general')
        user_id = get_user_id()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO images (user_id, filename, subject) VALUES (?,?,?) """, (user_id, filename, subject))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Image uploaded successfully!', 'filename': filename})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/upload/delete/<int:image_id>')
def delete_image(image_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM images WHERE id = ?", (image_id,))
    img = cursor.fetchone()
    if img:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], img['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
        conn.commit()
    conn.close()
    flash("Image deleted.")
    return redirect(url_for('upload'))

# ------------------
# LOGOUT ROUTING
# ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------
# RUN APP
# ------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)