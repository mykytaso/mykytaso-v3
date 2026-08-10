# Makefile Usage

All targets in the [`Makefile`](Makefile). Every Django command runs through `uv run`.

**Read the "Where to run" column before using a target.** Some targets only work on your laptop, some only on the production server, and one only works inside the production container.

---

## Quick reference

| Command | Where to run | What it does |
| --- | --- | --- |
| `make dev` | laptop | Start the dev environment (app + Postgres) |
| `make dev-rebuild` | laptop | Same, but rebuild the image from scratch |
| `make migrations` | laptop | Create new migration files |
| `make migrate` | laptop | Apply migrations |
| `make superuser` | laptop | Create an admin account |
| `make docker-makemigrations` | laptop | Create migrations inside the running dev container |
| `make docker-migrate` | laptop | Apply migrations inside the running dev container |
| `make docker-superuser` | laptop | Create an admin account inside the running dev container |
| `make check` | laptop | Lint + format check (no changes made) |
| `make fix` | laptop | Auto-fix lint issues + format the code |
| `make lint` | laptop | Lint only |
| `make lint-fix` | laptop | Lint and auto-fix |
| `make format` | laptop | Format the code |
| `make format-check` | laptop | Check formatting only |
| `make check-stats` | laptop | Lint statistics, never fails |
| `make prod-db-backup` | production host | Dump the production database to `backups/` |
| `make prod-db-restore DUMP=…` | production host | Restore the production database from a dump |
| `make prod-dbshell` | production host | Open `psql` on the production database |
| `make prod` | inside the prod container | Migrate, copy static files, start Gunicorn |

---

## Development

### `make dev`

```bash
make dev
```

Runs `docker compose -f docker-compose.yaml up`. Starts two containers:

- `mykyta_app` — Django dev server on <http://localhost:8000>
- `db` — PostgreSQL 18 on `localhost:5432`

The app waits for the database, runs `migrate`, then starts `runserver`. Your code is mounted into the container, so edits reload automatically. Stop with `Ctrl+C`.

Needs a `.env` file — copy `.env.example` and fill it in.

### `make dev-rebuild`

```bash
make dev-rebuild
```

Same as `make dev` but adds `--build --force-recreate`. Use it after changing `pyproject.toml`, `uv.lock`, or the `Dockerfile`. Slower, because dependencies are reinstalled.

---

## Database (local)

These run on your laptop and use the database from your `.env`.

```bash
make migrations   # create migration files after changing a model
make migrate      # apply migrations
make superuser    # create an admin account for /kerivnyk/
```

`make migrations` only writes files — it does not touch the database. Always review the generated file, then run `make migrate`.

### Same commands, but inside the dev container

Use these while `make dev` is running in another terminal. They are the right choice when your laptop cannot reach the database directly.

```bash
make docker-makemigrations
make docker-migrate
make docker-superuser
```

They run `docker compose exec web …`, so the dev containers must already be up.

---

## Code quality

Ruff does both linting and formatting. Config is in `pyproject.toml` (line length 100).

```bash
make check   # before committing — checks, changes nothing
make fix     # fixes what it can, then formats
```

The individual pieces, if you need them:

| Command | Changes files? | Fails on problems? |
| --- | --- | --- |
| `make lint` | no | yes |
| `make lint-fix` | yes | yes |
| `make format` | yes | no |
| `make format-check` | no | yes |
| `make check-stats` | no | no |

`make check` runs `lint` + `format-check`. `make fix` runs `lint-fix` + `format`. Use `check-stats` to see a summary of problems without the command failing.

---

## Production database

Run these on the production host, from `/home/mykyta/mykytaso-v3`. They talk to the `db` container defined in `docker-compose.production.yaml`.

You never pass the database name, user, or password. Each target reads `POSTGRES_USER` and `POSTGRES_DB` from inside the `db` container, so the credentials live in one place only (the `x-postgres-env` anchor in the compose file).

### Backup

```bash
make prod-db-backup
```

Writes `backups/mykytaso_db_<timestamp>.dump` — a compressed custom-format dump (`pg_dump -Fc`).

The dump is written to a `.tmp` file first and renamed only if `pg_dump` succeeds. So a file in `backups/` is always a complete backup, never a half-written one.

`backups/` is git-ignored. Copy important dumps off the server.

### Restore

```bash
make prod-db-restore DUMP=backups/mykytaso_db_20260810_030000.dump
```

**This overwrites the current database.** It runs `pg_restore --clean --if-exists`, which drops the existing tables before recreating them. Take a backup first.

The target refuses to run if `DUMP=` is missing, or if the file does not exist or is empty.

### psql shell

```bash
make prod-dbshell
```

Opens an interactive `psql` session in the `db` container. Exit with `\q`.

This is the replacement for the host `psql` command, which is gone now that PostgreSQL runs in Docker.

---

## `make prod` — do not run this yourself

```makefile
prod:
	uv run manage.py migrate
	cp -r /app/frontend/static /tmp/
	uv run gunicorn app.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8012
```

This is the `command:` of the `mykytaso_app` service in `docker-compose.production.yaml`. Docker runs it automatically on every deploy. It expects the paths of the production container (`/app`, `/tmp/static`) and will not work on your laptop.

It is listed here only so you know what happens during a deploy:

1. Apply database migrations.
2. Copy static files to `/tmp/static`, which is bind-mounted to `frontend/static` on the host so nginx can serve them.
3. Start Gunicorn with 4 Uvicorn workers on port `8012` (published on `127.0.0.1` only; nginx proxies to it).

---

## Warnings

- **Never run `docker compose -f docker-compose.production.yaml down -v` on the server.** The `-v` flag deletes the `db-data` volume, which is the entire production database.
- `make prod-db-restore` is destructive. Back up first.
- The deploy workflow copies only `.env` and `docker-compose.production.yaml` to the server. If you add or change a Makefile target, update the server checkout too, or the new target will not be there.