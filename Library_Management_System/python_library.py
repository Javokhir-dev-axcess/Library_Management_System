import sqlite3


class DatabaseManager:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                genre TEXT,
                status TEXT DEFAULT 'Available',
                publish_year INTEGER
            );

            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS borrowings (
                borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                user_id INTEGER,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        self.conn.commit()

    #Books
    def add_book(self, title, author, genre, publish_year):
        self.cur.execute(
            "INSERT INTO books (title, author, genre, publish_year, status) VALUES (?, ?, ?, ?, 'Available')",
            (title, author, genre, publish_year),
        )
        self.conn.commit()
        print(f"'{title}' added.")

    def get_books(self, sort_by="title", order="ASC"):
        allowed_cols = {"book_id", "title", "author", "genre", "publish_year", "status"}
        col = sort_by if sort_by in allowed_cols else "title"
        order = "DESC" if order.upper() == "DESC" else "ASC"
        rows = self.cur.execute(f"SELECT * FROM books ORDER BY {col} {order}").fetchall()
        return [dict(r) for r in rows]

    def search_books(self, keywords):
        words = keywords.split()[:3]
        if not words:
            return []
        parts = []
        params = []
        for w in words:
            parts.append("(title LIKE ? OR author LIKE ?)")
            params.extend([f"%{w}%", f"%{w}%"])
        sql = "SELECT * FROM books WHERE " + " AND ".join(parts)
        rows = self.cur.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def delete_book(self, book_id):
        try:
            self.cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            self.conn.commit()
            print("Book deleted." if self.cur.rowcount else "Book not found.")
        except sqlite3.IntegrityError:
            print("Cannot delete: book has borrowing history.")

    def set_book_status(self, book_id, status):
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", (status, book_id))
        self.conn.commit()

    def add_user(self, name, email):
        try:
            self.cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            print(f"User '{name}' added.")
        except sqlite3.IntegrityError:
            print("Email already exists.")

    def get_users(self):
        rows = self.cur.execute("SELECT * FROM users").fetchall()
        return [dict(r) for r in rows]

    def update_user(self, user_id, new_name, new_email):
        self.cur.execute(
            "UPDATE users SET name = ?, email = ? WHERE user_id = ?",
            (new_name, new_email, user_id),
        )
        self.conn.commit()
        print("User updated." if self.cur.rowcount else "User not found.")

    def delete_user(self, user_id):
        try:
            self.cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.conn.commit()
            print("User deleted." if self.cur.rowcount else "User not found.")
        except sqlite3.IntegrityError:
            print("Cannot delete: user has borrowing records.")

    # Borrowings
    def borrow_book(self, book_id, user_id):
        book = self.cur.execute("SELECT status FROM books WHERE book_id = ?", (book_id,)).fetchone()
        if not book:
            print("Book not found.")
            return
        if book["status"] != "Available":
            print("Book is not available.")
            return

        user = self.cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if not user:
            print("User not found.")
            return

        self.set_book_status(book_id, "Borrowed")
        self.cur.execute(
            "INSERT INTO borrowings (book_id, user_id, borrow_date) VALUES (?, ?, DATE('now'))",
            (book_id, user_id),
        )
        self.conn.commit()
        print("Book borrowed successfully.")

    def return_book(self, book_id):
        self.set_book_status(book_id, "Available")
        self.cur.execute(
            "UPDATE borrowings SET return_date = DATE('now') WHERE book_id = ? AND return_date IS NULL",
            (book_id,),
        )
        self.conn.commit()
        print("Book returned.")

    def get_borrowings(self):
        rows = self.cur.execute("SELECT * FROM borrowings").fetchall()
        return [dict(r) for r in rows]


def check_admin():
    return input("\nAdmin password: ") == "lms1234"


def main():
    db = DatabaseManager()

    while True:
        print("\n" + " LIBRARY SYSTEM ".center(30, "-"))
        print("1. View Books (SQL Sort)")
        print("2. Search Books")
        print("3. Add Book")
        print("4. Delete Book")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. View Books (Python Sort)")
        print("8. Add User")
        print("9. View Users")
        print("10. Delete User")
        print("11. Update User")
        print("12. Borrowing Records")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            col = input("Sort by (title / author): ").strip()
            order = input("Order (ASC / DESC): ").strip()
            for b in db.get_books(col, order):
                print(b)

        elif choice == "2":
            keys = input("Keywords: ").strip()
            res = db.search_books(keys)
            print("\n".join(str(r) for r in res) if res else "No books found.")

        elif choice == "3" and check_admin():
            try:
                title = input("Title: ")
                author = input("Author: ")
                genre = input("Genre: ")
                year = int(input("Publish Year: "))
                db.add_book(title, author, genre, year)
            except ValueError:
                print("Year must be a number.")

        elif choice == "4" and check_admin():
            try:
                db.delete_book(int(input("Book ID: ")))
            except ValueError:
                print("ID must be a number.")

        elif choice == "5":
            try:
                db.borrow_book(int(input("Book ID: ")), int(input("User ID: ")))
            except ValueError:
                print("IDs must be numbers.")

        elif choice == "6":
            try:
                db.return_book(int(input("Book ID: ")))
            except ValueError:
                print("ID must be a number.")

        elif choice == "7":
            books = db.get_books()
            for b in sorted(books, key=lambda x: (x["title"] or "").lower()):
                print(b)

        elif choice == "8" and check_admin():
            db.add_user(input("Full name: "), input("Email: "))

        elif choice == "9":
            for u in db.get_users():
                print(u)

        elif choice == "10" and check_admin():
            try:
                db.delete_user(int(input("User ID: ")))
            except ValueError:
                print("ID must be a number.")

        elif choice == "11" and check_admin():
            try:
                uid = int(input("User ID: "))
                db.update_user(uid, input("New name: "), input("New email: "))
            except ValueError:
                print("ID must be a number.")

        elif choice == "12":
            recs = db.get_borrowings()
            print("\n".join(str(r) for r in recs) if recs else "No records.")

        elif choice == "0":
            db.conn.close()
            print("Bye!")
            break

        else:
            print("Invalid choice or wrong password.")


if __name__ == "__main__":
    main()