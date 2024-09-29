from pydantic import BaseModel
from app.models import Thread
from app.models import Chat
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_engine import engine

class ThreadRead(BaseModel):
    id: int

async def get_default_thread():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the thread. There's only one thread.
            result = await session.execute(select(Thread))
            thread = result.scalars().first()

            if thread is None:
                return None

            return ThreadRead(id=thread.id)


