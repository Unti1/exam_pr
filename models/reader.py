from datetime import datetime
import re

class Reader:
    def __init__(self, name, email, phone):
        if not name or not name.strip():
            raise ValueError("Имя читателя не может быть пустым")
        if not self._is_valid_email(email):
            raise ValueError("Некорректный email адрес")
        self.id = None
        self.name = name.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.registration_date = datetime.now()

    def _is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def update_info(self, name=None, email=None, phone=None):
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
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'registration_date': self.registration_date
        } 