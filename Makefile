project-init:
	python -m pip install -U pip pip-tools setuptools wheel
	python -m pip install -r requirements/dev.txt
	python manage.py migrate
	python manage.py createsuperuser --email root@root.ru --username root -v 3
	python manage.py fill_db
