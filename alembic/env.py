from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from config.settings import settings
from config.Database.base_model import mapped_metadata
from app.models import *

if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

target_metadata = mapped_metadata

def run_migrations(db_name, connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata[db_name]
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    for db_name, db_config in settings.DATABASES.items():
        url = (
            f"postgresql://{db_config['USER']}:{db_config['PASSWORD']}@"
            f"{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )
        context.configure(url=url, target_metadata=target_metadata[db_name])
        with context.begin_transaction():
            context.run_migrations()
else:
    for db_name, db_config in settings.DATABASES.items():
        sync_url = (
            f"postgresql://{db_config['USER']}:{db_config['PASSWORD']}@"
            f"{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )
        sync_engine = create_engine(sync_url, poolclass=pool.NullPool)

        with sync_engine.connect() as connection:
            run_migrations(db_name, connection)
