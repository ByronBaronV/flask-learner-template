# Database Code Blocks

This folder contains example code blocks for working with SQLite in your Flask application. Each example is thoroughly documented and can be copied into your project.

## Quick Start
1. Copy the code you need from these examples
2. Modify table names, column names, and queries to match your needs
3. Always remember to close your database connections!

## Files in this Directory

- `basic_crud.py`: Basic Create, Read, Update, Delete operations
- `table_setup.py`: Examples of creating different types of tables
- `advanced_queries.py`: More complex queries including JOINs

## Common SQLite Types
- TEXT: For strings
- INTEGER: For whole numbers
- REAL: For decimal numbers
- BLOB: For binary data
- NULL: For null values

## Important Tips
1. Always use parameterized queries (?, ?) to prevent SQL injection
2. Close connections after using them
3. Use 'WITH' keyword for better connection handling
4. Remember to commit changes for INSERT, UPDATE, DELETE operations

## Common Issues
1. "Database is locked": Another connection is using the database
2. "No such table": Table doesn't exist or wrong table name
3. "No such column": Column name is misspelled or doesn't exist