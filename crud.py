from models import User as User, Voice, Photo

from db_conf import db_session
db = db_session.session_factory()


def create_user(id, name):
    user = User(id=id, name=name)
    db.add(user)
    db.commit()
    return user

def create_voice(user_id, file_name):
    voice = Voice(file_name=file_name, user_id=user_id)
    db.add(voice)
    db.commit()
    return voice

def create_photo(user_id, file_name):
    photo = Photo(file_name=file_name, user_id=user_id)
    db.add(photo)
    db.commit()
    return photo

# Read
def get_user_by_id(user_id):
    return db.query(User).filter_by(id=user_id).first()

def get_voice_by_id(voice_id):
    return db.query(Voice).filter_by(id=voice_id).first()

def get_photo_by_id(photo_id):
    return db.query(Photo).filter_by(id=photo_id).first()

# Update
def update_user_name(user_id, new_name):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        user.name = new_name
        db.commit()
        return True
    return False

# Delete
def delete_user(user_id):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def delete_voice(voice_id):
    voice = db.query(Voice).filter_by(id=voice_id).first()
    if voice:
        db.delete(voice)
        db.commit()
        return True
    return False

def delete_photo(photo_id):
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if photo:
        db.delete(photo)
        db.commit()
        return True
    return False
