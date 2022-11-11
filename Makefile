project-init:
	python -m pip install -U pip pip-tools setuptools wheel
	python -m pip install -r requirements/dev.txt
	docker compose up -d db
	python manage.py migrate
