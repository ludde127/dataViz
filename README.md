# Yapity

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

```shell
python manage.py makemigrations
python manage.py migrate
```

## Run Django Server

```shell
python manage.py runserver
```

## Tailwind

If you're going to change the html templates and need to recompile tailwind:

### Setup

```shell
cd tailwind
pnpm i
```

### Run continuously in development

```shell
pnpm dev
```

### Build minified tailwind.css

```shell
pnpm build
```
