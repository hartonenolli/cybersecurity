from db import db
from sqlalchemy.sql import text

def get_person(username):
    sql = f"SELECT username FROM person WHERE username='{username}'"
    result = db.session.execute(text(sql))
    try:
        person = result.fetchone()[0]
        return person
    except TypeError:
        return None

# Here is a SQL injection vulnerability
# malicious user could use the following values
# username = "' OR '1'='1"
# password = "' OR '1'='1"
# and get all of the usernames and passwords
# This is fixed in the next function
#def get_person_password(username, password):
#    sql = "SELECT username, password FROM person WHERE username=:username AND password=:password"
#    result = db.session.execute(text(sql), {'username':username, 'password':password})
#    try:
#        user_data = result.fetchall()
#        return user_data
#    except Exception:
#        return None
def get_person_name_and_pass(username):
    sql = f"SELECT username, password FROM person WHERE username='{username}'"
    result = db.session.execute(text(sql))
    try:
        user_data = result.fetchall()
        return user_data
    except Exception:
        return None

#def get_person_password_hash(username):
#    sql = "SELECT password FROM person WHERE username=:username"
#    result = db.session.execute(text(sql), {'username':username})
#    try:
#        person_password = result.fetchone()[0]
#        return person_password
#    except Exception:
#        return None

def get_person_id(username):
    sql = "SELECT id FROM person WHERE username=:username"
    result = db.session.execute(text(sql), {'username':username})
    person_id = result.fetchone()[0]
    return person_id

def add_person(username, password):
    sql = "INSERT INTO person (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {'username':username, 'password':password})
    db.session.commit()

def add_message(message, user_id):
    sql = "INSERT INTO info_message (user_id, time, memo) VALUES (:user_id, NOW(), :message) "
    db.session.execute(text(sql), {'user_id':user_id, 'message':message})
    db.session.commit()

def get_messages():
    sql = "SELECT * FROM info_message"
    result = db.session.execute(text(sql))
    messages = result.fetchall()
    return messages

def get_message_by_id(notes_id):
    sql = "SELECT * FROM info_message WHERE id=:notes_id"
    result = db.session.execute(text(sql), {'notes_id':notes_id})
    message = result.fetchone()
    return message

def get_my_messages(user_id):
    sql = "SELECT * FROM info_message WHERE user_id=:user_id"
    result = db.session.execute(text(sql), {'user_id':user_id})
    messages = result.fetchall()
    return messages

def delete_message_and_comments(notes_id):
    sql = "DELETE FROM info_comment WHERE notes_id=:notes_id"
    db.session.execute(text(sql), {'notes_id':notes_id})
    sql = "DELETE FROM info_message WHERE id=:notes_id"
    db.session.execute(text(sql), {'notes_id':notes_id})
    db.session.commit()

def get_comments(notes_id):
    sql = "SELECT * FROM info_comment WHERE notes_id=:notes_id"
    result = db.session.execute(text(sql), {'notes_id':notes_id})
    comments = result.fetchall()
    return comments

def add_comment(comment, user_id, notes_id):
    sql = "INSERT INTO info_comment (user_id, notes_id, time, comment) VALUES (:user_id, :notes_id, NOW(), :comment) "
    db.session.execute(text(sql), {'user_id':user_id, 'notes_id':notes_id, 'comment':comment})
    db.session.commit()