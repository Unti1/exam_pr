import tkinter as tk
from tkinter import ttk, messagebox

class BookView(ttk.Frame):
    def __init__(self, parent, book_controller):
        super().__init__(parent)
        self.book_controller = book_controller
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self):
        # Форма добавления книги
        form = ttk.LabelFrame(self, text="Добавить книгу")
        form.pack(fill="x", padx=10, pady=5)
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        ttk.Label(form, text="Название:").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.title_var).grid(row=0, column=1)
        ttk.Label(form, text="Автор:").grid(row=0, column=2)
        ttk.Entry(form, textvariable=self.author_var).grid(row=0, column=3)
        ttk.Label(form, text="ISBN:").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.isbn_var).grid(row=1, column=1)
        ttk.Label(form, text="Год:").grid(row=1, column=2)
        ttk.Entry(form, textvariable=self.year_var).grid(row=1, column=3)
        ttk.Label(form, text="Кол-во:").grid(row=2, column=0)
        ttk.Entry(form, textvariable=self.quantity_var).grid(row=2, column=1)
        ttk.Button(form, text="Добавить", command=self.add_book).grid(row=2, column=3, pady=5)

        # Таблица книг
        self.tree = ttk.Treeview(self, columns=("id", "title", "author", "year", "available"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("year", text="Год")
        self.tree.heading("available", text="Доступно")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопка удаления
        ttk.Button(self, text="Удалить выбранную книгу", command=self.delete_selected).pack(pady=5)

    def refresh_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in self.book_controller.get_all_books():
            self.tree.insert("", "end", values=(book.id, book.title, book.author, book.year, book.available))

    def add_book(self):
        try:
            title = self.title_var.get()
            author = self.author_var.get()
            isbn = self.isbn_var.get()
            year = int(self.year_var.get())
            quantity = int(self.quantity_var.get())
            self.book_controller.add_book(title, author, isbn, year, quantity)
            self.refresh_books()
            self.title_var.set("")
            self.author_var.set("")
            self.isbn_var.set("")
            self.year_var.set("")
            self.quantity_var.set("")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        book_id = self.tree.item(selected[0])["values"][0]
        self.book_controller.delete_book(book_id)
        self.refresh_books() 