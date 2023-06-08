format_all:
	poetry run black .
	poetry run isort .
	poetry run flake8 .

test:
	poetry run ./manage.py test --parallel
