from sqlalchemy.sql import text
from sqlalchemy.future import select
from config.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from .custom_session import CustomAsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

class DatabaseManager:
    def __init__(self):
        self.engines = {}
        self.sessions = {}

        if hasattr(settings, "DATABASES") and isinstance(settings.DATABASES, dict):
            for db_name, db_config in settings.DATABASES.items():
                engine = create_async_engine(self._create_connection_string(db_config), echo=True)
                self.engines[db_name] = engine
                self.sessions[db_name] = sessionmaker(
                    bind=engine, class_=CustomAsyncSession, expire_on_commit=False
                )

    @staticmethod
    def _create_connection_string(db_config):
        return (
            f"{db_config['ENGINE']}://{db_config['USER']}:{db_config['PASSWORD']}@"
            f"{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )

    @asynccontextmanager
    async def get_db(self, db_name="default"):
        if db_name not in self.sessions:
            raise ValueError(f"Database '{db_name}' not found in settings.")

        session = self.sessions[db_name]()
        try:
            yield session 
            await session.commit()  
        except Exception as e:
            await session.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            await session.close() 

    async def validate_connections(self):
        if not self.engines:
            print("No DATABASES found in settings. Skipping DB validation.")
            return

        for db_name, engine in self.engines.items():
            try:
                async with engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                print(f"Connected to {db_name} database successfully!")
            except SQLAlchemyError as e:
                print(f"Database Connection Error in {db_name}: {e}")
                exit(1)

    # utility function
    async def execute_db_operation(self, instance, db_name="default", operation="add"):
        try:
            async with self.get_db(db_name) as db:
                if operation == "custom":
                    return await instance(db)
            
                method = getattr(db, operation, None)
                if method:
                    method(instance) 

                await db.commit()
                if operation == "add":
                    await db.refresh(instance)

                if operation == "delete":
                    return instance in db

                return instance 
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Database operation '{operation}' failed: {e}")
            return False


    async def create(self, instance, db_name="default"):
        return await self.execute_db_operation(instance, db_name, "add")

    async def delete(self, instance, db_name="default"):
        return await self.execute_db_operation(db_name, instance, "delete")
    
    async def filter(self, model, filters, fetch_all=False, db_name="default"):
        async def operation(db):
            query = select(model)

            if filters:
                for key, value in filters.items():
                    query = query.where(getattr(model, key) == value)

            result = await db.scalars(query)
            return result.all() if fetch_all else result.first()

        return await self.execute_db_operation(operation, db_name, "custom")


db_manager = DatabaseManager()
