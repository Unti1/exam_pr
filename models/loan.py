from datetime import datetime

class Loan:
    def __init__(self, book_id, reader_id, loan_date, return_date):
        if book_id <= 0:
            raise ValueError("ID книги должен быть положительным")
        if reader_id <= 0:
            raise ValueError("ID читателя должен быть положительным")
        if return_date <= loan_date:
            raise ValueError("Дата возврата должна быть позже даты выдачи")
        self.id = None
        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False

    def return_book(self):
        if not self.is_returned:
            self.is_returned = True
            return True
        return False

    def is_overdue(self):
        if self.is_returned:
            return False
        return datetime.now() > self.return_date

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'reader_id': self.reader_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date,
            'is_returned': self.is_returned
        } 