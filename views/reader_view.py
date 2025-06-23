import tkinter as tk
from tkinter import ttk, messagebox

class ReaderView(ttk.Frame):
    def __init__(self, parent, reader_controller):
        super().__init__(parent)
        self.reader_controller = reader_controller
        self.create_widgets()
        self.refresh_readers()

    def create_widgets(self):
        # Форма добавления читателя
        form = ttk.LabelFrame(self, text="Добавить читателя")
        form.pack(fill="x", padx=10, pady=5)
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        ttk.Label(form, text="Имя:").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.name_var).grid(row=0, column=1)
        ttk.Label(form, text="Email:").grid(row=0, column=2)
        ttk.Entry(form, textvariable=self.email_var).grid(row=0, column=3)
        ttk.Label(form, text="Телефон:").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.phone_var).grid(row=1, column=1)
        ttk.Button(form, text="Добавить", command=self.add_reader).grid(row=1, column=3, pady=5)

        # Таблица читателей
        self.tree = ttk.Treeview(self, columns=("id", "name", "email", "phone"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Имя")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Телефон")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопка удаления
        ttk.Button(self, text="Удалить выбранного читателя", command=self.delete_selected).pack(pady=5)

    def refresh_readers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for reader in self.reader_controller.get_all_readers():
            self.tree.insert("", "end", values=(reader.id, reader.name, reader.email, reader.phone))

    def add_reader(self):
        try:
            name = self.name_var.get()
            email = self.email_var.get()
            phone = self.phone_var.get()
            self.reader_controller.add_reader(name, email, phone)
            self.refresh_readers()
            self.name_var.set("")
            self.email_var.set("")
            self.phone_var.set("")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        reader_id = self.tree.item(selected[0])["values"][0]
        self.reader_controller.delete_reader(reader_id)
        self.refresh_readers() 