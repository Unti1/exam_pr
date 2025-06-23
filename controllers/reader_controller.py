from models.reader import Reader

class ReaderController:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_reader(self, name, email, phone):
        reader = Reader(name, email, phone)
        return self.db.add_reader(reader)

    def get_reader(self, reader_id):
        return self.db.get_reader_by_id(reader_id)

    def get_all_readers(self):
        return self.db.get_all_readers()

    def update_reader(self, reader_id, **kwargs):
        return self.db.update_reader(reader_id, **kwargs)

    def delete_reader(self, reader_id):
        return self.db.delete_reader(reader_id)

    def get_reader_loans(self, reader_id):
        return self.db.get_reader_loans(reader_id) 