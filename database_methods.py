from db import db
from sqlalchemy.sql import text

def get_person(username):
    sql = "SELECT username FROM person WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    try:
        person = result.fetchone()[0]
        return person
    except TypeError:
        return None

def get_person_password(username, password):
    sql = "SELECT password FROM person WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    person_password = result.fetchone()[0]
    if person_password == password:
        return True
    return False

def get_person_id(username):
    sql = "SELECT id FROM person WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    person_id = result.fetchone()[0]
    return person_id

def add_message(message, user_id):
    sql = "INSERT INTO info_message (user_id, time, memo) VALUES (:user_id, NOW(), :message) "
    db.session.execute(text(sql), {'user_id':user_id, 'message':message})
    db.session.commit()

def get_messages():
    sql = "SELECT * FROM info_message"
    result = db.session.execute(text(sql))
    messages = result.fetchall()
    return messages