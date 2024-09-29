from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from app.seed import seed_thread_if_needed
from app.seed import seed_user_if_needed
from app.services.user import get_default_user
from app.services.thread import get_default_thread
from app.services.chat import get_thread_messages
from app.services.chat import save_chat_to_thread
from app.services.chat import generate_chatbot_response

# This isn't the right place for these I bet!
seed_user_if_needed()
seed_thread_if_needed()

app = FastAPI()

# could be /users/{id}
@app.get("/users/me")
async def get_my_user():
    user = await get_default_user()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# could be /users/{id}/threads - get all, maybe name them or something
# combined with /users/{id}/threads/{id} - get one, could make a UI to select conversation
# add POST /users/{id}/threads - create new thread to round out functionality
@app.get("/users/me/threads/default")
async def get_my_thread():
    thread = await get_default_thread()
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

# could be /threads/{id}/chat - get all the messages for a thread
# need also POST /threads/{id}/chat/ - create a message for a thread, only support one user
#     and POST /threads/{id}/bot-chat - create a chatbot message for a thread
@app.get("/threads/default/chats")
async def get_my_thread_messages():
    thread = await get_default_thread()
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    chats = await get_thread_messages(thread.id)

    # Can this actually happen?
    if chats is None:
        raise HTTPException(status_code=404, detail="No chats found")

    return chats

class UserChatRequest(BaseModel):
    message: str
    thread_id: int
    user_id: int

@app.post("/threads/default/chats")
async def create_thread_message(user_chat: UserChatRequest):
    chat = await save_chat_to_thread(
        user_id=user_chat.user_id,
        message=user_chat.message,
        thread_id=user_chat.thread_id,
    )
    if chat is None:
        raise HTTPException(status_code=400, detail="Could not save chat")

    return chat

class BotMessageRequest(BaseModel):
    message: str
    thread_id: int

@app.post("/threads/default/bot-chat")
async def create_bot_response_for_my_thread(bot_message: BotMessageRequest):
    chat = await generate_chatbot_response(bot_message.message, bot_message.thread_id)
    if chat is None:
        raise HTTPException(status_code=400, detail="Could not save bot response")

    return chat
