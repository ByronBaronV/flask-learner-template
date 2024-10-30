"""
Example code blocks for basic CRUD (Create, Read, Update, Delete) operations in SQLite.
Copy and modify these examples for your own database operations.
"""

import sqlite3
from datetime import datetime


# === CONNECTION EXAMPLES ===

def example_connection():
    """Example of creating a database connection"""
    # Basic connection
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Do your database operations here

    # Always close the connection
    conn.close()


def example_connection_with_row_factory():
    """Example of connection that allows accessing columns by name"""
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row  # This lets you access columns by name
    cursor = conn.cursor()

    # Now you can do: row['column_name'] instead of row[0]

    conn.close()


# === CREATE (INSERT) EXAMPLES ===

def example_insert_single():
    """Example of inserting a single record"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Single insert with parameters (safe from SQL injection)
    cursor.execute(
        'INSERT INTO users (username, email) VALUES (?, ?)',
        ('john_doe', 'john@example.com')
    )

    # Get the ID of the last inserted row
    last_id = cursor.lastrowid

    conn.commit()  # Don't forget to commit!
    conn.close()


def example_insert_many():
    """Example of inserting multiple records at once"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # List of users to insert
    users = [
        ('jane_doe', 'jane@example.com'),
        ('bob_smith', 'bob@example.com'),
        ('alice_jones', 'alice@example.com')
    ]

    # Insert multiple rows at once
    cursor.executemany(
        'INSERT INTO users (username, email) VALUES (?, ?)',
        users
    )

    conn.commit()
    conn.close()


# === READ (SELECT) EXAMPLES ===

def example_select_all():
    """Example of selecting all records"""
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select all rows
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()

    # Print each user
    for user in all_users:
        print(f"Username: {user['username']}, Email: {user['email']}")

    conn.close()


def example_select_filtered():
    """Example of selecting records with conditions"""
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select with WHERE clause
    username = 'john_doe'
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()  # Get just one result

    if user:
        print(f"Found user: {user['username']}")

    conn.close()


# === UPDATE EXAMPLES ===

def example_update():
    """Example of updating records"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Update a single record
    cursor.execute(
        'UPDATE users SET email = ? WHERE username = ?',
        ('new_email@example.com', 'john_doe')
    )

    # Check how many rows were affected
    rows_affected = cursor.rowcount
    print(f"Updated {rows_affected} rows")

    conn.commit()
    conn.close()


# === DELETE EXAMPLES ===

def example_delete():
    """Example of deleting records"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Delete with condition
    cursor.execute('DELETE FROM users WHERE username = ?', ('john_doe',))

    # Delete all records (be careful!)
    # cursor.execute('DELETE FROM users')

    conn.commit()
    conn.close()


# === ERROR HANDLING EXAMPLE ===

def example_with_error_handling():
    """Example of proper error handling"""
    conn = None
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Your database operations here
        cursor.execute('INSERT INTO users (username) VALUES (?)', ('new_user',))

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.rollback()  # Roll back any changes if there was an error

    finally:
        if conn:
            conn.close()  # Always close the connection


# === DEMO AREA ===
if __name__ == '__main__':
    # Test the example functions
    example_connection()
    example_connection_with_row_factory()
    example_insert_single()
    example_select_all()