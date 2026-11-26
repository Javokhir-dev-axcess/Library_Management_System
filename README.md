This is simple CLI library management system i built with sqlite and python for university final project. 
It helps to manage books, users, and book borrowing records in a small library.
#What it can do?
- Add new books with title, author, genre, and publish year (admin password required)
- View books sorted by SQL (`ASC` / `DESC`) or sorted in Python
- Search books by keywords in title or author
- Delete books and check borrowing history
- Add, view, update, and delete library users
- Borrow and return books, which automatically update book status (`Available` / `Borrowed`) and dates
- View all borrowing records

What files do this folder include:

- `init_sqlite_db.py` — creates the `library.db` SQLite database and inserts sample data for books, users, and borrowings.
- `python_library.py` — main Python program with menu and database actions.
- `library.db` — SQLite database file storing the library data.
