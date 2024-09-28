from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from app.seed import seed_user_if_needed
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_engine import engine
from app.models import User

seed_user_if_needed()

app = FastAPI()


class UserRead(BaseModel):
    id: int
    name: str


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)
