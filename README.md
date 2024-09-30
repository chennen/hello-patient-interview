## Hello Patient ChatBot

This is a simple chat bot application for review by Hello Patient interviewers.

A logged-in user (no login system is provided for this example) may send a message to the chat bot. The chat bot will reply immediately with a nonsense phrase!

Chat messages are persisted across page loads/visits and client/server/database restarts.

## Postgres Data Model
<img width="692" alt="image" src="https://github.com/user-attachments/assets/c8f7da1b-3184-46f6-8411-354e11caea54">

### Tables

1. User - represents a user of the application who can type messages to the chat bot. Could be extended to also represent bot accounts.
   There is only one user called "Alice" for now.
1. Thread - a grouping for chat messages from users and bots. Could be extended to support different threads for a user, or for multiple users to chat in a single thread.
   There is only one thread (whose `id` is 1) for now.
1. Chat - represents a single message in a thread. If the message came from a bot, the `user_id` column is `NULL`.1. Chat - represents a single message in a thread. If the message came from a bot, the `user_id` column is `NULL`.

## FastAPI Backend

### Routes

1. `GET /users/me` - get the "Alice" user.
1. `GET /users/me/threads/default` - get "Alice"s thread.
1. `GET /threads/default/chats` - get the chat messages for the thread.
1. `POST /threads/default/chats` - save a user's input chat message to the thread. 


    Example request body:  

   ```json
   {
   "user_id": "1",
   "thread_id": "1",
   "message": "hello world"
   }
   ```

   Example cURL:

   ```
   curl -X POST "http://localhost:8000/threads/default/chats" \
      -H "Content-Type: application/json" \
      -d '{ "message": "hello world", "thread_id": "1", "user_id": "1" }'
   ```

1. `POST /threads/default/bot-chat` - generate a chat bot response to the provided chat message, and save the bot chat message to the thread.


   Example request body:

   ```json
   {
   "thread_id": "1",
   "message": "i want to know more about zebras"
   }
   ```

   Example cURL:

   ```
   curl -X POST "http://localhost:8000/threads/default/bot-chat" \
      -H "Content-Type: application/json" \
      -d '{ "message": "hello world", "thread_id": "1" }'
   ```

## NextJS Frontend

???

## Running the Application
The application is containerized and runs with docker and docker-compose.

### Required Software

1. Docker and Docker Compose

### Run the PostgreSQL database, NextJS frontend, and FastAPI backend

1. From the root directory, run `docker-compose up --build`
