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