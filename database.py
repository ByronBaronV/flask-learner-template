import sqlite3
from datetime import datetime
import os

# Configuration
DATABASE_FILE = 'blog_database.db'
UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Database Connection
def get_db_connection():
    """Create a database connection that allows accessing columns by name"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# Database Setup
def init_db():
    """Create the database tables if they don't exist"""
    conn = get_db_connection()

    # Posts table: stores blog post content
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Media table: tracks files associated with posts
    conn.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            media_type TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def seed_sample_data():
    """Add example blog posts to get started"""
    conn = get_db_connection()

    sample_posts = [
        (
            "My First Blog Post",
            "Hello! This is my first post on my personal blog. I'm excited to share my thoughts and experiences with you.",
            datetime.now()
        ),
        (
            "Learning Python",
            "Today I learned about Flask and SQLite. It's amazing how you can build a web application with just a few lines of code!",
            datetime.now()
        ),
        (
            "Weekend Adventures",
            "Went hiking with friends this weekend. The weather was perfect and we took lots of pictures!",
            datetime.now()
        )
    ]

    conn.executemany(
        'INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)',
        sample_posts
    )
    conn.commit()
    conn.close()


# Post Operations
def get_all_posts():
    """Get all posts with their media, newest first"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()

    # Add media to each post
    for post in posts:
        post = dict(post)
        post['media'] = get_post_media(post['id'])

    conn.close()
    return posts


def get_post(post_id):
    """Get a single post and its media by ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if post:
        post = dict(post)
        post['media'] = get_post_media(post['id'])

    conn.close()
    return post


def create_post(title, content):
    """Create a new post and return its ID"""
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                          (title, content))
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id


def update_post(post_id, title, content):
    """Update a post's title and content"""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                 (title, content, post_id))
    conn.commit()
    conn.close()


def delete_post(post_id):
    """Delete a post and all its associated media"""
    # Get media files before deleting the post
    media_files = get_post_media(post_id)

    # Delete post (cascades to media table)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    # Clean up media files from storage
    for media in media_files:
        file_path = os.path.join(UPLOAD_FOLDER, media['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)


# Media Operations
def add_media(post_id, filename, media_type):
    """Add a new media record for a post"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO media (post_id, filename, media_type)
        VALUES (?, ?, ?)
    ''', (post_id, filename, media_type))
    conn.commit()
    conn.close()


def get_post_media(post_id):
    """Get all media associated with a post"""
    conn = get_db_connection()
    media = conn.execute('''
        SELECT * FROM media
        WHERE post_id = ?
        ORDER BY created_at
    ''', (post_id,)).fetchall()
    conn.close()
    return media


def delete_media(media_id):
    """Delete a single media file and its database record"""
    conn = get_db_connection()

    # Get filename before deleting record
    media = conn.execute('SELECT filename FROM media WHERE id = ?', (media_id,)).fetchone()

    if media:
        # Remove database record
        conn.execute('DELETE FROM media WHERE id = ?', (media_id,))
        conn.commit()

        # Delete file from storage
        file_path = os.path.join(UPLOAD_FOLDER, media['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)

    conn.close()


# Script Initialization
if __name__ == '__main__':
    print("Initializing database...")
    init_db()

    print("Adding sample data...")
    seed_sample_data()

    print("Database setup complete! You can now run app.py")