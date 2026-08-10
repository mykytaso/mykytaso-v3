# Makefile Usage


## Development


```bash
make dev
```

Runs `docker compose -f docker-compose.dev.yaml up`

<br>

```bash
make dev-rebuild
```

Same as `make dev` but adds `--build --force-recreate`. 
Used after changing `pyproject.toml`, `uv.lock`, or the `Dockerfile`. Slower, because dependencies are reinstalled.


---


## Database (local)

Runs locally and uses the database from `.env`:

```bash
make migrations   # create migration files after changing a model
make migrate      # apply migrations
make superuser    # create an admin account for /kerivnyk/
```

While `make dev` is running:

```bash
make docker-makemigrations
make docker-migrate
make docker-superuser
```


---


## Production database

You never pass the database name, user, or password. 
Each target reads `POSTGRES_USER` and `POSTGRES_DB` from inside the `db` container, so the credentials live in one place only (the `x-postgres-env` anchor in the compose file).

<br>

### Backup

```bash
make prod-db-backup
```

Writes `backups/mykytaso_db_<timestamp>.dump` — a compressed custom-format dump (`pg_dump -Fc`).
`backups/` is git-ignored.

<br>

### Restore

```bash
make prod-db-restore DUMP=backups/mykytaso_db_20260810_030000.dump
```

**This overwrites the current database.** It runs `pg_restore --clean --if-exists`, which drops the existing tables before recreating them. Take a backup first.

The target refuses to run if `DUMP=` is missing, or if the file does not exist or is empty.

**It only accepts `-Fc` custom-format `.dump` files** — the kind `make prod-db-backup` produces. 

<br>

### psql shell

```bash
make prod-dbshell
```

Opens an interactive `psql` session in the `db` container. Exit with `\q`.


---

## `make prod` — Do not run manually!

```makefile
prod:
	uv run manage.py migrate
	cp -r /app/frontend/static /tmp/
	uv run gunicorn app.asgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8012
```

- This is the `command:` of the `mykytaso_app` service in `docker-compose.production.yaml`. 
- Docker runs it automatically on every deploy. 
- It expects the paths of the production container (`/app`, `/tmp/static`) and will not work locally.

What happens during a deploy:

1. Apply database migrations.
2. Copy static files to `/tmp/static`, which is bind-mounted to `frontend/static` on the host so nginx can serve them.
3. Start Gunicorn with 4 Uvicorn workers on port `8012` (published on `127.0.0.1` only; nginx proxies to it).

---

## Warnings

- **Never run `docker compose -f docker-compose.production.yaml down -v` on the server.** The `-v` flag deletes the `db-data` volume, which is the entire production database.
- `make prod-db-restore` is destructive. Back up first.
- The deploy workflow copies `.env`, `docker-compose.production.yaml`, and this `Makefile` to the server. A Makefile change therefore reaches production on the next push — and overwrites any hand edit made on the server.


---


## Ruff

```bash
#  runs `lint` + `format-check`
make check   # before committing — checks, changes nothing

# runs `lint-fix` + `format`
make fix     # fixes what it can, then formats
```

The individual pieces:

| Command | Changes files? | Fails on problems? |
| --- | --- | --- |
| `make lint` | no | yes |
| `make lint-fix` | yes | yes |
| `make format` | yes | no |
| `make format-check` | no | yes |
| `make check-stats` | no | no |
