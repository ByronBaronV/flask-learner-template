"""
Examples of more advanced SQLite queries.
These examples assume you have tables for a blog with posts and comments.
"""

import sqlite3


def example_join_query():
    """Example of a JOIN query to get posts with their comment counts"""
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # JOIN query with comment count
    cursor.execute('''
        SELECT 
            posts.id,
            posts.title,
            posts.content,
            COUNT(comments.id) as comment_count
        FROM posts
        LEFT JOIN comments ON comments.post_id = posts.id
        GROUP BY posts.id
        ORDER BY posts.created_at DESC
    ''')

    posts_with_counts = cursor.fetchall()

    for post in posts_with_counts:
        print(f"Post: {post['title']}, Comments: {post['comment_count']}")

    conn.close()


def example_search_query():
    """Example of searching posts with LIKE"""
    conn = sqlite3.connect('your_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    search_term = '%python%'  # % is a wildcard
    cursor.execute('''
        SELECT * FROM posts 
        WHERE title LIKE ? OR content LIKE ?
    ''', (search_term, search_term))

    search_results = cursor.fetchall()
    conn.close()
    return search_results


def example_aggregate_query():
    """Example of using aggregate functions"""
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Get post counts by date
    cursor.execute('''
        SELECT 
            date(created_at) as post_date,
            COUNT(*) as post_count
        FROM posts
        GROUP BY date(created_at)
        HAVING post_count > 1
        ORDER BY post_date DESC
    ''')

    daily_counts = cursor.fetchall()
    conn.close()
    return daily_counts


# Note: These are more advanced examples.
# Start with basic_crud.py first and come back to these
# when you're comfortable with basic operations.

if __name__ == '__main__':
    print("Testing advanced queries...")
    example_join_query()