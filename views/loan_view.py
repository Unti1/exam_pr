import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class LoanView(ttk.Frame):
    def __init__(self, parent, loan_controller, book_controller, reader_controller):
        super().__init__(parent)
        self.loan_controller = loan_controller
        self.book_controller = book_controller
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_loans()

    def create_widgets(self):
        # Форма создания выдачи
        form = ttk.LabelFrame(self, text="Создать выдачу")
        form.pack(fill="x", padx=10, pady=5)
        self.book_id_var = tk.StringVar()
        self.reader_id_var = tk.StringVar()
        self.days_var = tk.StringVar(value="14")
        ttk.Label(form, text="ID книги:").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.book_id_var).grid(row=0, column=1)
        ttk.Label(form, text="ID читателя:").grid(row=0, column=2)
        ttk.Entry(form, textvariable=self.reader_id_var).grid(row=0, column=3)
        ttk.Label(form, text="Дней на выдачу:").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.days_var).grid(row=1, column=1)
        ttk.Button(form, text="Создать выдачу", command=self.create_loan).grid(row=1, column=3, pady=5)

        # Таблица выдач
        self.tree = ttk.Treeview(self, columns=("id", "book_id", "reader_id", "loan_date", "return_date", "is_returned"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("book_id", text="ID книги")
        self.tree.heading("reader_id", text="ID читателя")
        self.tree.heading("loan_date", text="Дата выдачи")
        self.tree.heading("return_date", text="Дата возврата")
        self.tree.heading("is_returned", text="Возвращена")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопка возврата
        ttk.Button(self, text="Отметить возврат выбранной книги", command=self.return_selected).pack(pady=5)

    def refresh_loans(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for loan in self.loan_controller.get_all_loans():
            self.tree.insert("", "end", values=(loan.id, loan.book_id, loan.reader_id, loan.loan_date.strftime("%Y-%m-%d"), loan.return_date.strftime("%Y-%m-%d"), "Да" if loan.is_returned else "Нет"))

    def create_loan(self):
        try:
            book_id = int(self.book_id_var.get())
            reader_id = int(self.reader_id_var.get())
            days = int(self.days_var.get())
            loan_date = datetime.now()
            return_date = loan_date + timedelta(days=days)
            self.loan_controller.create_loan(book_id, reader_id, loan_date, return_date)
            self.refresh_loans()
            self.book_id_var.set("")
            self.reader_id_var.set("")
            self.days_var.set("14")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def return_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        loan_id = self.tree.item(selected[0])["values"][0]
        self.loan_controller.return_book(loan_id)
        self.refresh_loans() 