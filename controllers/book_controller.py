from models.book import Book

class BookController:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_book(self, title, author, isbn, year, quantity):
        book = Book(title, author, isbn, year, quantity)
        return self.db.add_book(book)

    def get_book(self, book_id):
        return self.db.get_book_by_id(book_id)

    def get_all_books(self):
        return self.db.get_all_books()

    def update_book(self, book_id, **kwargs):
        return self.db.update_book(book_id, **kwargs)

    def delete_book(self, book_id):
        return self.db.delete_book(book_id)

    def search_books(self, query):
        return self.db.search_books(query)

    def borrow_book(self, book_id):
        book = self.db.get_book_by_id(book_id)
        if book and book.borrow_book():
            self.db.update_book(book_id, available=book.available)
            return True
        return False

    def return_book(self, book_id):
        book = self.db.get_book_by_id(book_id)
        if book and book.return_book():
            self.db.update_book(book_id, available=book.available)
            return True
        return False 