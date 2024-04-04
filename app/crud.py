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
