import sqlite3
from datetime import datetime
import os

DATABASE_FILE = 'blog_database.db'
UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db_connection():
    """Create a database connection and return the connection object"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


def init_db():
    """Initialize the database by creating tables"""
    conn = get_db_connection()

    # Create posts table with media support
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create media table to track uploads
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
    """Add sample blog posts to the database"""
    conn = get_db_connection()

    # Sample blog posts
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

    # Insert sample posts
    conn.executemany(
        'INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)',
        sample_posts
    )

    conn.commit()
    conn.close()


# Media operations
def add_media(post_id, filename, media_type):
    """Add a media file record to the database"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO media (post_id, filename, media_type)
        VALUES (?, ?, ?)
    ''', (post_id, filename, media_type))
    conn.commit()
    conn.close()


def get_post_media(post_id):
    """Get all media files for a specific post"""
    conn = get_db_connection()
    media = conn.execute('''
        SELECT * FROM media
        WHERE post_id = ?
        ORDER BY created_at
    ''', (post_id,)).fetchall()
    conn.close()
    return media


def delete_post_media(post_id):
    """Delete all media records for a post"""
    conn = get_db_connection()
    conn.execute('DELETE FROM media WHERE post_id = ?', (post_id,))
    conn.commit()
    conn.close()


# Existing database operations
def get_all_posts():
    """Retrieve all blog posts, ordered by creation date (newest first)"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()

    # Get media for each post
    for post in posts:
        post = dict(post)
        post['media'] = get_post_media(post['id'])

    conn.close()
    return posts


def get_post(post_id):
    """Retrieve a specific post by its ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()

    if post:
        post = dict(post)
        post['media'] = get_post_media(post['id'])

    conn.close()
    return post


def create_post(title, content):
    """Create a new blog post"""
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                          (title, content))
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id


def update_post(post_id, title, content):
    """Update an existing blog post"""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                 (title, content, post_id))
    conn.commit()
    conn.close()


def delete_post(post_id):
    """Delete a blog post and its media"""
    # First, get all media to delete files
    media_files = get_post_media(post_id)

    # Delete the post (will cascade delete media records)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    # Delete actual files
    for media in media_files:
        file_path = os.path.join(UPLOAD_FOLDER, media['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == '__main__':
    print("Initializing database...")
    init_db()

    print("Adding sample data...")
    seed_sample_data()

    print("Database setup complete! You can now run app.py")