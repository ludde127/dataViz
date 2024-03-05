# Monke Town

## Setup

### Create `secret/secret.py` file
```py
IS_PRODUCTION = False or True
DJANGO_SECRET_KEY = "<secret key>"
POSTGRES__PASS = "<postgres password>"
POSTGRES__PORT = "<postgres port>"
```

### Setup a PostgreSQL server
You can setup a [PostgreSQL](https://www.postgresql.org/) server using their installer.
Then create a database in the postgres server called `dataViz`.

### Migrate db
```
python manage.py makemigrations
python manage.py migrate
```

## Run

```
python manage.py runserver
```