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

## Typescript and Tailwind

If you're going to change the typescript code or the html templates and need to recompile typescript or tailwind:

### Setup

```shell
cd node
pnpm i
```

### Run build script

The script will be watching for changes and continuously recompile, interrupt it using <kbd>Ctrl</kbd>+<kbd>C</kbd>.

```shell
pnpm build
```

### Adding new scripts

#### Standalone scripts

When adding new scripts, you can add a new standalone script if you put it directly in the [src](./node/src/) directory.
This script will have to be manually added to [base.html](./templates/base.html).

#### Imported scripts

Scripts can also be imported in other script files, this way they will all be bundled into one big script.
See [main.ts](./node/src/main.ts) for reference.
