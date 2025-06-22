#!/usr/bin/env python3
"""
Пример реализации для демонстрации структуры проекта
Этот файл показывает, как должны быть реализованы классы согласно заданию
"""

from datetime import datetime, timedelta
import re


class Book:
    """Модель книги - пример реализации"""
    
    def __init__(self, title, author, isbn, year, quantity):
        """
        Инициализация книги
        
        Args:
            title (str): Название книги
            author (str): Автор книги
            isbn (str): ISBN номер
            year (int): Год издания
            quantity (int): Количество экземпляров
        """
        # Валидация данных
        if not title or not title.strip():
            raise ValueError("Название книги не может быть пустым")
        if not author or not author.strip():
            raise ValueError("Автор книги не может быть пустым")
        if year < 0 or year > datetime.now().year:
            raise ValueError("Некорректный год издания")
        if quantity < 0:
            raise ValueError("Количество экземпляров не может быть отрицательным")
        
        self.id = None  # Будет установлен при сохранении в БД
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.year = year
        self.quantity = quantity
        self.available = quantity  # Изначально все экземпляры доступны
    
    def borrow_book(self):
        """Выдать книгу"""
        if self.available > 0:
            self.available -= 1
            return True
        return False
    
    def return_book(self):
        """Вернуть книгу"""
        if self.available < self.quantity:
            self.available += 1
            return True
        return False
    
    def is_available(self):
        """Проверить доступность книги"""
        return self.available > 0
    
    def to_dict(self):
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'quantity': self.quantity,
            'available': self.available
        }


class Reader:
    """Модель читателя - пример реализации"""
    
    def __init__(self, name, email, phone):
        """
        Инициализация читателя
        
        Args:
            name (str): Имя читателя
            email (str): Email адрес
            phone (str): Номер телефона
        """
        # Валидация данных
        if not name or not name.strip():
            raise ValueError("Имя читателя не может быть пустым")
        if not self._is_valid_email(email):
            raise ValueError("Некорректный email адрес")
        
        self.id = None  # Будет установлен при сохранении в БД
        self.name = name.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.registration_date = datetime.now()
    
    def _is_valid_email(self, email):
        """Проверка корректности email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def update_info(self, name=None, email=None, phone=None):
        """Обновить информацию о читателе"""
        if name is not None:
            if not name.strip():
                raise ValueError("Имя читателя не может быть пустым")
            self.name = name.strip()
        
        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Некорректный email адрес")
            self.email = email.strip()
        
        if phone is not None:
            self.phone = phone.strip()
    
    def to_dict(self):
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'registration_date': self.registration_date
        }


class Loan:
    """Модель выдачи книги - пример реализации"""
    
    def __init__(self, book_id, reader_id, loan_date, return_date):
        """
        Инициализация выдачи
        
        Args:
            book_id (int): ID книги
            reader_id (int): ID читателя
            loan_date (datetime): Дата выдачи
            return_date (datetime): Дата возврата
        """
        # Валидация данных
        if book_id <= 0:
            raise ValueError("ID книги должен быть положительным")
        if reader_id <= 0:
            raise ValueError("ID читателя должен быть положительным")
        if return_date <= loan_date:
            raise ValueError("Дата возврата должна быть позже даты выдачи")
        
        self.id = None  # Будет установлен при сохранении в БД
        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False
    
    def return_book(self):
        """Отметить книгу как возвращенную"""
        if not self.is_returned:
            self.is_returned = True
            return True
        return False
    
    def is_overdue(self):
        """Проверить просрочку"""
        if self.is_returned:
            return False
        return datetime.now() > self.return_date
    
    def to_dict(self):
        """Преобразовать в словарь"""
        return {
            'id': self.id,
            'book_id': self.book_id,
            'reader_id': self.reader_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date,
            'is_returned': self.is_returned
        }


# Пример использования
if __name__ == "__main__":
    print("Пример использования моделей:")
    
    # Создание книги
    try:
        book = Book("Война и мир", "Лев Толстой", "978-5-389-12345-6", 1869, 5)
        print(f"Создана книга: {book.title} - {book.author}")
        print(f"Доступно экземпляров: {book.available}")
        
        # Выдача книги
        if book.borrow_book():
            print(f"Книга выдана. Осталось: {book.available}")
        
        # Возврат книги
        if book.return_book():
            print(f"Книга возвращена. Доступно: {book.available}")
            
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    
    # Создание читателя
    try:
        reader = Reader("Иван Иванов", "ivan@example.com", "+7-999-123-45-67")
        print(f"Создан читатель: {reader.name} ({reader.email})")
        
        # Обновление информации
        reader.update_info(name="Иван Петров")
        print(f"Обновлен читатель: {reader.name}")
        
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
    
    # Создание выдачи
    try:
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)
        loan = Loan(1, 1, loan_date, return_date)
        print(f"Создана выдача: книга {loan.book_id}, читатель {loan.reader_id}")
        print(f"Просрочена: {loan.is_overdue()}")
        
    except ValueError as e:
        print(f"Ошибка валидации: {e}") 