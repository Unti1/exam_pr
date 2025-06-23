from datetime import datetime

class Book:
    def __init__(self, title, author, isbn, year, quantity):
        if not title or not title.strip():
            raise ValueError("Название книги не может быть пустым")
        if not author or not author.strip():
            raise ValueError("Автор книги не может быть пустым")
        if year < 0 or year > datetime.now().year:
            raise ValueError("Некорректный год издания")
        if quantity < 0:
            raise ValueError("Количество экземпляров не может быть отрицательным")
        self.id = None
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.year = year
        self.quantity = quantity
        self.available = quantity

    def borrow_book(self):
        if self.available > 0:
            self.available -= 1
            return True
        return False

    def return_book(self):
        if self.available < self.quantity:
            self.available += 1
            return True
        return False

    def is_available(self):
        return self.available > 0

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'quantity': self.quantity,
            'available': self.available
        } 