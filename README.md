# Student Learning Management App
**Nazaneen Baguaei | Spring 2026 | Queensborough Community College | 2026**

---

## Introduction

This is a full-stack web application built with Flask that helps students stay on top of their academic life. It brings together three core tools: a to-do list for tracking tasks and deadlines, a blog for writing about learning experiences, and an image upload section for storing and organizing notes.

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
    ├── new_post.html
    ├── view_post.html
    └── upload.html
```

---

## File Descriptions

### `app.py`
The main application file. Handles all routes, database logic, session management, and file uploads.

### `flask_db.db`
The SQLite database. Stores users, tasks, blog posts, comments, likes, and uploaded image records.

### `static/`

| File | Description |
|------|-------------|
| `style.css` | Stylesheet for the entire app — layout, colors, buttons, forms, and responsive design. |
| `script.js` | Handles client-side behavior including the image upload fetch request and form validation. |

### `templates/`

| File | Description |
|------|-------------|
| `base.html` | Shared layout that all pages extend. Includes navigation, footer, and links to CSS and JS. |
| `login.html` | Login page where users enter their email and password. |
| `signup.html` | Registration page for creating a new account. |
| `dashboard.html` | Landing page after login. Shows the user's name and links to all features. |
| `todo.html` | To-Do List page for creating, completing, and deleting tasks with categories and due dates. |
| `blog.html` | Blog feed showing all published posts with like and comment counts. |
| `new_post.html` | Form for writing and publishing a new blog post. |
| `view_post.html` | Individual post page with full content, comments, and a like button. |
| `upload.html` | Notes gallery where users can upload, preview, download, and delete images. |

---

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirects to login |
| `/login` | GET, POST | Authenticates user and starts session |
| `/signup` | GET, POST | Creates a new user account |
| `/dashboard` | GET | Main dashboard (login required) |
| `/todo` | GET | Displays the task list |
| `/todo/add` | POST | Adds a new task |
| `/todo/complete/<id>` | GET | Marks a task as completed |
| `/todo/delete/<id>` | GET | Deletes a task |
| `/blog` | GET | Displays all blog posts |
| `/blog/new` | GET, POST | Form to write and publish a new post |
| `/blog/post/<id>` | GET | Displays a single post with comments |
| `/blog/comment/<id>` | POST | Adds a comment to a post |
| `/blog/like/<id>` | GET | Toggles a like on a post |
| `/upload` | GET | Displays the notes gallery |
| `/upload/image` | POST | Handles image file upload |
| `/upload/delete/<id>` | GET | Deletes an uploaded image |
| `/logout` | GET | Clears session and redirects to login |

---

## Setup and Installation

**Requirements:** Python 3.x, Flask

```bash
pip install flask
```

To run the app:

```bash
python app.py
```

The database is created automatically on first run. The app will be available at `http://127.0.0.1:5000`.
