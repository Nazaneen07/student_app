# ET721 Final Project — Student Learning Management App
**By Nazaneen Baguaei | Spring 2026 | Queensborough Community College**

---

## Introduction

The Student Learning Management App is a full-stack web application built using the Flask framework. The purpose of this application is to enhance students' productivity and improve their overall learning experience.

The platform provides a user-friendly interface that integrates essential academic tools:
- A **task management (To-Do List)** system for tracking assignments and deadlines
- A **blogging platform** for sharing learning experiences and study tips
- An **image upload feature** for storing and organizing handwritten or digital notes

---

## Repository Structure

```
ET721_project_student_app/
├── app.py
├── flask_db.db
├── README.md
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── base.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── todo.html
    ├── blog.html
    └── upload.html
```

---

## File Descriptions

### `app.py`
The main Flask application file. Contains all route definitions, database connection logic, and session management.

### `flask_db.db`
The SQLite database file. Stores all user accounts, tasks, blog posts, and uploaded image records.

---

### `static/` Folder

| File | Description |
|------|-------------|
| `style.css` | Main stylesheet for the entire application. Controls layout, colors, buttons, forms, and responsive design. |
| `script.js` | JavaScript file for client-side functionality, including password validation on login and signup forms. |

---

### `templates/` Folder

| File | Description |
|------|-------------|
| `base.html` | Base template that all other pages extend. Contains the shared HTML structure, navigation, footer, and links to CSS and JS files. |
| `login.html` | Login page where users enter their email and password to access the app. |
| `signup.html` | Signup page where new users create an account with a username, email, and password. |
| `dashboard.html` | Main landing page after login. Displays the user's name and navigation cards linking to the To-Do List, Blog, and Upload features. |
| `todo.html` | To-Do List page where users can create, update, delete, and mark tasks as completed. |
| `blog.html` | Blog page where users can write and publish posts about their learning experiences. |
| `upload.html` | Image upload page where users can upload, preview, and download images of their notes. |

---

## Routes Defined in `app.py`

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirects to the login page |
| `/login` | GET, POST | Displays login form; authenticates user and starts session |
| `/signup` | GET, POST | Displays signup form; creates new user in the database |
| `/dashboard` | GET | Displays the main dashboard (requires login) |
| `/todo` | GET | Displays the To-Do List page (requires login) |
| `/blog` | GET | Displays the Blog page (requires login) |
| `/upload` | GET | Displays the Image Upload page (requires login) |
| `/logout` | GET | Clears session and redirects to login |

---

## Setup and Installation

### Requirements
- Python 3.x
- Flask

### Install Dependencies
```bash
pip install flask
```

### Initialize the Database
Run this once in the terminal before starting the app:
```bash
python -c "
import sqlite3
conn = sqlite3.connect('flask_db.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')
conn.commit()
conn.close()
print('Database ready!')
"
```


---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite