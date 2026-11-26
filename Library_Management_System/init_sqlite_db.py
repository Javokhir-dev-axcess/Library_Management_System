import sqlite3


def build_library_db(db_name="library.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.executescript("""
        PRAGMA foreign_keys = OFF;
        DROP TABLE IF EXISTS borrowings;
        DROP TABLE IF EXISTS books;
        DROP TABLE IF EXISTS users;
        PRAGMA foreign_keys = ON;

        CREATE TABLE books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            genre TEXT,
            status TEXT DEFAULT 'Available' CHECK (status IN ('Available', 'Borrowed')),
            publish_year INTEGER
        );

        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        );

        CREATE TABLE borrowings (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            user_id INTEGER,
            borrow_date TEXT,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    """)

    books = [
        (1, "PYTHON CRASH COURSE", "Eric Matthes", "Programming", "Available", 1972),
        (2, "AUTOMATE THE BORING STUFF WITH PYTHON", "AL SWEIGART", "Programming", "Available", 2019),
        (3, "CODE COMPLETE", "Steve McConnell", "Programming", "Available", 2004),
        (4, "WORKING EFFECTIVELY WITH LEGACY CODE", "Michael Feathers", "Programming", "Available", 2004),
        (5, "THE ART OF COMPUTER PROGRAMMING", "Donald Knuth", "Programming", "Available", 2011),
        (6, "THE THREE-BODY PROBLEM", "Cixin Liu", "Science-Fiction", "Available", 2008),
        (7, "THE MARTIAN", "Andy Weir", "Science-Fiction", "Available", 2011),
        (8, "LEVIATHAN WAKES", "James Corey", "Science-Fiction", "Available", 2011),
        (9, "ANCILLARY JUSTICE", "Ann Leckie", "Science-Fiction", "Available", 2013),
        (10, "A MEMORY CALLED EMPIRE", "Arkady Martine", "Science-Fiction", "Borrowed", 2019),
        (11, "ATOMIC HABITS", "James Clear", "Self-Help", "Available", 2018),
        (12, "THE 7 HABITS OF HIGHLY EFFECTIVE PEOPLE", "Stephen Covery", "Self-Help", "Borrowed", 1989),
        (13, "THE POWER OF NOW", "Eckhart Tolle", "Self-Help", "Available", 1997),
        (14, "THINK AND GROW RICH", "Napoleon Hill", "Self-Help", "Available", 1937),
        (15, "HOW TO WIN FRIENDS AND INFLUENCE PEOPLE", "Dale Carnegie", "Self-Help", "Available", 1936),
        (16, "THE GUEST LIST", "Lucy Foley", "Thriller", "Available", 2020),
        (17, "THE GOOD DAUGHTER", "Karin Slaughter", "Thriller", "Available", 2017),
        (18, "THEY NEVER LEARN", "Layne Fargo", "Thriller", "Available", 2020),
        (19, "LONG BRIGHT RIVER", "Liz Moore", "Thiller", "Available", 2020),
        (20, "SHE RIDES SHOTGUN", "Jordan Harper", "Thriler", "Available", 2017),
        (23, "Hamsa", "Alisher Navai", "Poem", "Available", 1493),
    ]

    users = [
        (10, "Carienn Fowier", "cariennfowier@gmail.com"),
        (11, "Betty Daniels", "betty.daniels@gmailmail.com"),
        (12, "Charlie Brown", "charlie.brown@email.com"),
        (13, "David Wilson", "david.wilson@email.com"),
        (14, "Eve Adams", "eve.adams@email.com"),
        (15, "Karen Harris", "karen.harris@gmail.com"),
        (16, "Raymond Holbrook", "raymond.h@gmail.com"),
        (17, "Tommy Stafford", "stafford.tom@gmail.com"),
        (18, "Iris Ludwig", "ludwig.i@gmail.com"),
        (19, "Robert Jobe", "robert.j@gmail.com"),
        (20, "Monica Williams", "williams.monica@gmail.com"),
        (25, "Johhny Doe", "johnny@gmail.com"),
    ]

    borrowings = [
        (1, 1, 11, "2026-02-23", "2026-02-23"),
        (2, 1, 11, "2026-02-23", "2026-02-23"),
        (3, 10, 12, "2026-02-23", "2026-02-23"),
        (4, 1, 12, "2026-02-23", "2026-02-23"),
        (5, 12, 12, "2026-02-28", "2026-02-28"),
        (6, 12, 12, "2026-03-05", "2026-03-05"),
        (7, 12, 12, "2026-03-19", "2026-03-19"),
        (8, 12, 12, "2026-03-24", "2026-03-28"),
        (9, 12, 12, "2026-04-02", "2026-04-02"),
        (10, 12, 12, "2026-04-05", None),
        (11, 13, 13, "2026-04-08", "2026-04-08"),
        (12, 10, 10, "2026-04-09", None),
    ]

    cur.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)", books)
    cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
    cur.executemany("INSERT INTO borrowings VALUES (?, ?, ?, ?, ?)", borrowings)

    conn.commit()
    conn.close()
    print("Database created. ")


if __name__ == "__main__":
    build_library_db()