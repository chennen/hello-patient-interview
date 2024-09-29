from pydantic import BaseModel
from app.models import User
from app.models import Thread
from app.models import Chat
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_engine import engine
from datetime import datetime
import random

class ChatRead(BaseModel):
    message: str
    username: str
    time: datetime

# Simplified query to get chat messages - there's only one thread so all chats belong to that thread
# QUESTION: How to get sqlalchemy to populate Chat's "user" field without joining in the query?
# ASSUMPTION: number of chats is "small". Could try pointing large buffered result set to response stream, or simply limit results to latest N chats
async def get_thread_messages(thread_id):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Chat, User).join(Chat.user, isouter=True).order_by(Chat.time))

            chats: list[ChatRead] = []
            for chunk in result.partitions():
                for row in chunk:
                    chats.append(ChatRead(
                        message=row.Chat.message, 
                        username="smartbot" if row.User is None else row.User.name,
                        time=row.Chat.time
                    ))

            return chats

async def save_chat_to_thread(user_id, message, thread_id):
    async with AsyncSession(engine) as session:
        async with session.begin():
            userResult = await session.execute(select(User))
            user = userResult.scalars().first()

            if user is None:
                return None
            now = datetime.utcnow()
            session.add(Chat(
                message=message,
                time=now,
                thread_id=thread_id,
                user_id=user.id,
            ))
            session.commit()

            return ChatRead(message=message, username=user.name, time=now)



async def generate_chatbot_response(message, thread_id):
    # TODO: call API to generate chatbot response message
    #       save the response message to the thread
    #       return a ChatRead representing the chatbot message

    # STOLEN FROM STACK OVERFLOW I'M NOT ASHAMED
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs") 
    adv = ("crazily", "dutifully", "foolishly", "merrily", "occasionally")
    def num(): 
        return random.randrange(0,5)

    bot_message = adj[num()] + ' ' + nouns[num()] + ' ' + verbs[num()] + ' ' + adv[num()] + '.'

    async with AsyncSession(engine) as session:
        async with session.begin():
            now = datetime.utcnow()
            session.add(Chat(
                message=bot_message,
                time=now,
                thread_id=thread_id,
            ))
        session.commit()

        return ChatRead(message=bot_message, username="smartbot", time=now)
