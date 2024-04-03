from dotenv import load_dotenv
from os import environ
from models import User as User, Voice, Photo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(".env")
db_url = environ["DATABASE_URL"]

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def create_user(id, name):
    user = User(id=id, name=name)
    session.add(user)
    session.commit()
    return user

def create_voice( user_id, file_name):
    voice = Voice(file_name=file_name, user_id=user_id)
    session.add(voice)
    session.commit()
    return voice

def create_photo(user_id, file_name):
    photo = Photo(file_name=file_name, user_id=user_id)
    session.add(photo)
    session.commit()
    return photo

# Read
def get_user_by_id(user_id):
    return session.query(User).filter_by(id=user_id).first()

def get_voice_by_id(voice_id):
    return session.query(Voice).filter_by(id=voice_id).first()

def get_photo_by_id(photo_id):
    return session.query(Photo).filter_by(id=photo_id).first()

# Update
def update_user_name(user_id, new_name):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.name = new_name
        session.commit()
        return True
    return False

# Delete
def delete_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

def delete_voice(voice_id):
    voice = session.query(Voice).filter_by(id=voice_id).first()
    if voice:
        session.delete(voice)
        session.commit()
        return True
    return False

def delete_photo(photo_id):
    photo = session.query(Photo).filter_by(id=photo_id).first()
    if photo:
        session.delete(photo)
        session.commit()
        return True
    return False
