import sqlite3
from datetime import datetime

DATABASE_FILE = 'blog_database.db'


def get_db_connection():
    """Create a database connection and return the connection object"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


def init_db():
    """Initialize the database by creating tables"""
    conn = get_db_connection()

    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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


# Database operations
def get_all_posts():
    """Retrieve all blog posts, ordered by creation date (newest first)"""
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return posts


def get_post(post_id):
    """Retrieve a specific post by its ID"""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post


def create_post(title, content):
    """Create a new blog post"""
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                 (title, content))
    conn.commit()
    conn.close()


def update_post(post_id, title, content):
    """Update an existing blog post"""
    conn = get_db_connection()
    conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                 (title, content, post_id))
    conn.commit()
    conn.close()


def delete_post(post_id):
    """Delete a blog post"""
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()


# Demo Area
if __name__ == '__main__':
    print("Initializing database...")
    init_db()

    print("Adding sample data...")
    seed_sample_data()

    print("Database setup complete! You can now run app.py")