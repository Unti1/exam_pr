from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager):
        self.db = db_manager

    def create_loan(self, book_id, reader_id, loan_date, return_date):
        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db.add_loan(loan)

    def get_loan(self, loan_id):
        return self.db.get_loan_by_id(loan_id)

    def get_all_loans(self):
        return self.db.get_all_loans()

    def return_book(self, loan_id):
        loan = self.db.get_loan_by_id(loan_id)
        if loan and not loan.is_returned:
            loan.return_book()
            self.db.update_loan(loan_id, is_returned=True)
            return True
        return False

    def get_overdue_loans(self):
        return self.db.get_overdue_loans()

    def get_reader_loans(self, reader_id):
        return self.db.get_reader_loans(reader_id) 