import sqlite3
from models.book import Book
from models.reader import Reader
from models.loan import Loan
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="library.db"):
        self.connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def close(self):
        self.connection.close()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            year INTEGER,
            quantity INTEGER,
            available INTEGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            registration_date TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            reader_id INTEGER,
            loan_date TEXT,
            return_date TEXT,
            is_returned INTEGER,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(reader_id) REFERENCES readers(id)
        )''')
        self.connection.commit()

    # --- Book CRUD ---
    def add_book(self, book: Book):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO books (title, author, isbn, year, quantity, available)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (book.title, book.author, book.isbn, book.year, book.quantity, book.available))
        self.connection.commit()
        return cursor.lastrowid

    def get_book_by_id(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
        row = cursor.fetchone()
        if row:
            book = Book(row['title'], row['author'], row['isbn'], row['year'], row['quantity'])
            book.id = row['id']
            book.available = row['available']
            return book
        return None

    def get_all_books(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM books')
        books = []
        for row in cursor.fetchall():
            book = Book(row['title'], row['author'], row['isbn'], row['year'], row['quantity'])
            book.id = row['id']
            book.available = row['available']
            books.append(book)
        return books

    def update_book(self, book_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key}=?")
            values.append(value)
        if not fields:
            return False
        values.append(book_id)
        sql = f"UPDATE books SET {', '.join(fields)} WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(sql, values)
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_book(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def search_books(self, query):
        cursor = self.connection.cursor()
        like_query = f"%{query}%"
        cursor.execute('''SELECT * FROM books WHERE title LIKE ? OR author LIKE ?''', (like_query, like_query))
        books = []
        for row in cursor.fetchall():
            book = Book(row['title'], row['author'], row['isbn'], row['year'], row['quantity'])
            book.id = row['id']
            book.available = row['available']
            books.append(book)
        return books

    # --- Reader CRUD ---
    def add_reader(self, reader: Reader):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO readers (name, email, phone, registration_date)
                          VALUES (?, ?, ?, ?)''',
                       (reader.name, reader.email, reader.phone, reader.registration_date.isoformat()))
        self.connection.commit()
        return cursor.lastrowid

    def get_reader_by_id(self, reader_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM readers WHERE id=?', (reader_id,))
        row = cursor.fetchone()
        if row:
            reader = Reader(row['name'], row['email'], row['phone'])
            reader.id = row['id']
            reader.registration_date = datetime.fromisoformat(row['registration_date'])
            return reader
        return None

    def get_all_readers(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM readers')
        readers = []
        for row in cursor.fetchall():
            reader = Reader(row['name'], row['email'], row['phone'])
            reader.id = row['id']
            reader.registration_date = datetime.fromisoformat(row['registration_date'])
            readers.append(reader)
        return readers

    def update_reader(self, reader_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key}=?")
            values.append(value)
        if not fields:
            return False
        values.append(reader_id)
        sql = f"UPDATE readers SET {', '.join(fields)} WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(sql, values)
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_reader(self, reader_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM readers WHERE id=?', (reader_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    # --- Loan CRUD ---
    def add_loan(self, loan: Loan):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO loans (book_id, reader_id, loan_date, return_date, is_returned)
                          VALUES (?, ?, ?, ?, ?)''',
                       (loan.book_id, loan.reader_id, loan.loan_date.isoformat(), loan.return_date.isoformat(), int(loan.is_returned)))
        self.connection.commit()
        return cursor.lastrowid

    def get_loan_by_id(self, loan_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM loans WHERE id=?', (loan_id,))
        row = cursor.fetchone()
        if row:
            loan = Loan(row['book_id'], row['reader_id'], datetime.fromisoformat(row['loan_date']), datetime.fromisoformat(row['return_date']))
            loan.id = row['id']
            loan.is_returned = bool(row['is_returned'])
            return loan
        return None

    def get_all_loans(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM loans')
        loans = []
        for row in cursor.fetchall():
            loan = Loan(row['book_id'], row['reader_id'], datetime.fromisoformat(row['loan_date']), datetime.fromisoformat(row['return_date']))
            loan.id = row['id']
            loan.is_returned = bool(row['is_returned'])
            loans.append(loan)
        return loans

    def update_loan(self, loan_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key}=?")
            values.append(int(value) if key == 'is_returned' else value)
        if not fields:
            return False
        values.append(loan_id)
        sql = f"UPDATE loans SET {', '.join(fields)} WHERE id=?"
        cursor = self.connection.cursor()
        cursor.execute(sql, values)
        self.connection.commit()
        return cursor.rowcount > 0

    def get_reader_loans(self, reader_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM loans WHERE reader_id=?', (reader_id,))
        loans = []
        for row in cursor.fetchall():
            loan = Loan(row['book_id'], row['reader_id'], datetime.fromisoformat(row['loan_date']), datetime.fromisoformat(row['return_date']))
            loan.id = row['id']
            loan.is_returned = bool(row['is_returned'])
            loans.append(loan)
        return loans

    def get_overdue_loans(self):
        cursor = self.connection.cursor()
        now = datetime.now().isoformat()
        cursor.execute('SELECT * FROM loans WHERE is_returned=0 AND return_date<?', (now,))
        loans = []
        for row in cursor.fetchall():
            loan = Loan(row['book_id'], row['reader_id'], datetime.fromisoformat(row['loan_date']), datetime.fromisoformat(row['return_date']))
            loan.id = row['id']
            loan.is_returned = bool(row['is_returned'])
            loans.append(loan)
        return loans 