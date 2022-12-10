# Klack application

Разрабатываем свой собственный заменитель мессенджера Slack - **Klack**!

В ходе разработки разберемся, как разрабатывается API для таких приложений.

## Requirements

- Python 3.10

## Starting project

Для подготовки проекта к работе необходимо выполнить:

### OC Windows

```shell
python -m pip install -U pip pip-tools setuptools wheel
python -m pip install -r requirements/dev.txt
python manage.py migrate
python manage.py createsuperuser --email root@root.ru --username root -v 3
python manage.py fill_db
```

### ОС MacOS или Linux

```shell
make project-init
```

---

Затем необходимо выполнить тесты

```shell
python manage.py test
```

и запустить проект

```shell
python manage.py runserver
```

## Полезные ссылки

- [DRF Routing](https://www.django-rest-framework.org/api-guide/routers/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [DRF Filtering and Search](https://www.django-rest-framework.org/api-guide/filtering/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Factory_boy & Django ORM](https://factoryboy.readthedocs.io/en/latest/orms.html#django)
- [Faker: test data generation](https://faker.readthedocs.io/en/master/providers.html)
- [Data migrations](https://docs.djangoproject.com/en/4.1/topics/migrations/)
- [Custom management program](https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/)
- [drf-yasg: OpenAPI Specification generator](https://drf-yasg.readthedocs.io/en/stable/)
