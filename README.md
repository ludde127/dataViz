# Yapity

## Setup

### Create `secret/secret.py` file

```py
IS_PRODUCTION = False or True
DJANGO_SECRET_KEY = "<secret key>"
POSTGRES__PASS = "<postgres password>"
POSTGRES__PORT = "<postgres port>"
```

### Create `.yapenv` file

The `.yapenv` contain environment variables that will be loaded on startup.

#### `.yapenv`: Contains non-sensitive shared data that is tracked by git.

#### `.yapenv.local`: Contains environment variables used for local development.

```
ALLOWED_HOSTS = example.com,192.168.1.123
CSRF_TRUSTED_ORIGINS = https://example.com
CORS_ORIGIN_WHITELIST = https://example.com
```

#### `.yapenv.production`: Contains sensitive data used in the production build.

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

## Typescript

If you're going write typescript code and need to recompile the javascript files:

### Setup

```shell
cd typescript
pnpm i
```

### Run continuously in development

```shell
pnpm dev
```

### Build .js files

The typescript files will be compiled and placed in `static/js/compiled/`

```shell
pnpm build
```

### Add script to `base.html`

```html

<script type="module" src="{% static 'js/compiled/file.js' %}"></script>
```