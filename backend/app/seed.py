from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db_engine import sync_engine
from app.models import User
from app.models import Thread


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(User)).scalar_one_or_none() is not None:
                print("User already exists, skipping seeding")
                return
            print("Seeding user")
            session.add(User(name="Alice"))
            session.commit()

def seed_thread_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(Thread)).scalar_one_or_none() is not None:
                print("Thread already exists, skipping seeding")
                return
            print("Seeding thread")
            session.add(Thread())
            session.commit()
