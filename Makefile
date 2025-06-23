# Makefile для проекта на Python (MVC, SQLite, pytest)

.PHONY: install test lint run

install:
	pip install -r requirements.txt

test:
	pytest -v

# lint:
# 	flake8 . || echo "flake8 не установлен или есть замечания"

run:
	python main.py