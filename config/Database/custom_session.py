from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import Select

class CustomAsyncSession(AsyncSession):
    async def delete(self, instance):
        if hasattr(instance, "is_deleted"):
            instance.is_deleted = True  
            await self.commit()  
        else:
            raise IntegrityError("Hard delete is not allowed in this system.", params=None, orig=None)

    async def execute(self, statement, **kwargs):
        if isinstance(statement, Select): 
            model = getattr(statement.columns_clause_froms[0], "entity", None)

            if model and hasattr(model, "is_deleted"):
                if not kwargs.get("include_deleted", False):
                    statement = statement.where(model.is_deleted == False)

        return await super().execute(statement, **kwargs)

    async def scalars(self, statement, **kwargs):
        if isinstance(statement, Select):
            model = getattr(statement.columns_clause_froms[0], "entity", None)
            import pdb
            pdb.set_trace()
            if model and hasattr(model, "is_deleted"):
                if not kwargs.get("include_deleted", False):
                    statement = statement.where(model.is_deleted == False)

        return await super().scalars(statement, **kwargs)
