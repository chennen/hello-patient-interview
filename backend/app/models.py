from typing import List
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
    pass

# user_thread = Table(
#     "user_thread",
#     Base.metadata,
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
#     Column("thread_id", ForeignKey("thread.id"), primary_key=True),
# )

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    # threads: Mapped[List["thread"]] = relationship(secondary=user_thread)
    chats: Mapped[List["chat"]] = relationship("Chat", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"

class Thread(Base):
    __tablename__ = "thread"

    id: Mapped[int] = mapped_column(primary_key=True)
    # one thread to many chats
    chats: Mapped[List["chat"]] = relationship("Chat", back_populates="thread")
    # many users to many threads - support multiple users in each thread later
    # users: Mapped[List["user"]] = relationship(secondary=user_thread)

    def __repr__(self) -> str:
        return f"Thread(id={self.id!r})"


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text())
    time: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    # Many chats to one thread
    thread_id: Mapped[int] = mapped_column(ForeignKey("thread.id"))
    thread: Mapped[Thread] = relationship("Thread", back_populates="chats")
    # Many chats for one user
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional[User]] = relationship("User", back_populates="chats")
    
    def __repr__(self) -> str:
        return f"Chat(id={self.id!r}), userId={self.user_id!r}, messageText={self.message!r}, messageTime={self.time!r}, threadId={self.thread_id!r}"
