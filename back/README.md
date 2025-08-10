# Easy Test Backend

## Alembic Migrations

Alembic is used to manage database schema migrations. All commands should be run from within the `back` directory (or by prefixing with `cd back && ...`).

### Creating a New Migration

To automatically generate a new migration script based on changes to the SQLAlchemy models:

```bash
poetry run alembic revision --autogenerate -m "A descriptive message for the migration"
```

### Applying Migrations

To apply all pending migrations to the database:

```bash
poetry run alembic upgrade head
```

### Downgrading Migrations

To revert the last migration:

```bash
poetry run alembic downgrade -1
```

To revert to a specific migration version:

```bash
poetry run alembic downgrade <revision_hash>
```

### Checking Status

To see the current status of migrations:

```bash
poetry run alembic current
