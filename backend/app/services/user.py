from pydantic import BaseModel
from app.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_engine import engine

class UserRead(BaseModel):
    id: int
    name: str

async def get_default_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                return None

            return UserRead(id=user.id, name=user.name)
