"""
Examples of creating different types of database tables.
Shows various SQLite column types and constraints.
"""

import sqlite3


def example_create_basic_table():
    """Example of creating a simple table"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Basic table with common column types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def example_create_related_tables():
    """Example of creating tables with relationships"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Create a posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create a comments table that relates to posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


def example_create_table_with_constraints():
    """Example of a table with various constraints"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK (price > 0),
            stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            UNIQUE (name, category)
        )
    ''')

    conn.commit()
    conn.close()


# === DEMO AREA ===
if __name__ == '__main__':
    print("Creating example tables...")
    example_create_basic_table()
    example_create_related_tables()
    example_create_table_with_constraints()
    print("Tables created successfully!")