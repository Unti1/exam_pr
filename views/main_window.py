import tkinter as tk
from tkinter import ttk
from views.book_view import BookView
from views.reader_view import ReaderView
from views.loan_view import LoanView

class MainWindow(tk.Tk):
    def __init__(self, book_controller, reader_controller, loan_controller):
        super().__init__()
        self.title("Система управления библиотекой")
        self.geometry("800x600")
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.loan_controller = loan_controller

        tab_control = ttk.Notebook(self)
        self.book_tab = BookView(tab_control, self.book_controller)
        self.reader_tab = ReaderView(tab_control, self.reader_controller)
        self.loan_tab = LoanView(tab_control, self.loan_controller, self.book_controller, self.reader_controller)

        tab_control.add(self.book_tab, text="Книги")
        tab_control.add(self.reader_tab, text="Читатели")
        tab_control.add(self.loan_tab, text="Выдачи")
        tab_control.pack(expand=1, fill="both") 