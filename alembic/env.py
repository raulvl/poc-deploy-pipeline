import os

from alembic import context
from sqlalchemy import create_engine, pool

config = context.config


def get_url():
    # Mismo patrón que conn_sync en service-hub/src/config.py
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    psc_ip = os.environ.get("PSC_IP", "127.0.0.1")
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ["DB_NAME"]
    return f"postgresql+psycopg2://{user}:{password}@{psc_ip}:{port}/{name}"


def run_migrations_online():
    engine = create_engine(get_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None,  # migraciones manuales (no autogenerate)
            include_schemas=True,
            version_table="alembic_version",
            version_table_schema="poc",  # alembic_version vive dentro del schema poc
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
