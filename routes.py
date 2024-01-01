from app import app
from flask import render_template, request, redirect, session, abort
import database_methods
# import secrets
# import re
# import zxcvbn

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    

@app.route('/register', methods=["POST"]) #02
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        # Here we should make sure that the password is strong enough
        # And is is not in the list of most common passwords
        # to see if it is in most common passwords
        # we could use a library like zxcvbn
        # to do this, we should import zxcvbn
        # and use it to check the password
        # for example:
        # password_strength = zxcvbn.password_strength(password)
        # if password_strength < 3:
        #     error_msg = "Password is not strong enough"
        #     return render_template('try_again.html', error_msg=error_msg)
        # To see that the password includes at least one number, one uppercase letter and one lowercase letter
        # it could be done using regex
        # for example:
        # if len(password) < 8 or re.search('[0-9]', password) is None or re.search('[A-Z]', password) is None or re.search('[a-z]', password) is None:
        #     error_msg = "Password is not strong enough"
        #     return render_template('try_again.html', error_msg=error_msg)
        user_exists = database_methods.get_person(username)
        if user_exists == None and password == password2:
            # Here we sould hash the password
            # but this is not done
            # this is how it could be done:
            # importing werkzeug.security or other library
            # generating a hash from the password
            # storing the hash in the database
            # for example:
            # password_hash = werkzeug.security.generate_password_hash(password)
            # database_methods.add_person(username, password_hash)
            database_methods.add_person(username, password)
            return redirect('/')
        error_msg = "Username is already in use or passwords do not match"
        return render_template('try_again.html', error_msg=error_msg)

@app.route('/front_page', methods=["POST", "GET"]) #{csrf_token} #02 #07
def front_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here is a injection vulnerability
        # malicious user could use the following values
        # username = "arska"
        # password = "' OR id='1"
        # and being able to log in to arskas account
        user_data = database_methods.get_person_name_and_pass(username, password)
        try:
            if user_data == True:
            # After the proposed solution, the following code should be used
            # if user_data[0][0] == username and user_data[0][1] == password:
            #
            # Here we should check if the user exists and if the password is correct
            # database method should hash the password and compare the hashes
            # but this is not done
            # this is how it could be done:
            # importing werkzeug.security or other library
            # generating a hash from the password
            # comparing the hash with the hash in the database
            # if the hashes match, the password is correct
            # for example:
            # user_password_hash = database_methods.get_person_password_hash(username)
            # user_password = werkzeug.security.check_password_hash(user_password_hash, password)
            #user_password = database_methods.get_person_password(username, password)
                session["username"] = username
                # Here we should generate a new csrf token
                # but this is not done
                # this is how it could be done:
                # importing secrets
                # generating a new csrf token
                # session["csrf_token"] = secrets.token_hex(16)
                messages = database_methods.get_messages()
                return render_template('front_page.html', username=username, messages=messages)
        except Exception:
            pass
        error_msg = "Username or password is incorrect"
        return render_template('try_again.html', error_msg=error_msg)
    if request.method == "GET":
        username = session["username"]
        messages = database_methods.get_messages()
        return render_template('front_page.html', username=username, messages=messages)

@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        session.pop("username", None)
        # session.pop("csrf_token", None)
        return redirect('/')

@app.route('/my_messages/<username>', methods=["GET"]) #01
def my_messages(username):
    if request.method == "GET":
        # Here we have broken access control
        # this should be done with every request
        # and not only with GET requests
        # Here we should check the csrf token
        # but this is not done
        # this is how it could be done:
        # if session["csrf_token"] != request.args.get("csrf_token"):
            # abort(403)
        user_id = database_methods.get_person_id(username)
        messages = database_methods.get_my_messages(user_id)
        return render_template('my_messages.html', username=username, messages=messages)

@app.route('/message', methods=["POST"])
def message():
    if request.method == "POST":
        message = request.form["message"]
        return render_template('message.html', message=message)

@app.route('/add_message', methods=["POST"]) # 03
def add_message():
    if request.method == "POST":
        message = request.form["message"]
        username = session["username"]
        user_id = database_methods.get_person_id(username)
        database_methods.add_message(message, user_id)
        messages = database_methods.get_messages()
        return render_template('front_page.html', messages=messages)

@app.route('/delete_message', methods=["POST"])
def delete_message():
    if request.method == "POST":
        notes_id = request.form["message"]
        database_methods.delete_message_and_comments(notes_id)
        username = session["username"]
        user_id = database_methods.get_person_id(username)
        messages = database_methods.get_my_messages(user_id)
        return render_template('my_messages.html', username=username, messages=messages)

@app.route('/comment', methods=["POST"])
def comment():
    if request.method == "POST":
        notes_id = request.form["message"]
        message = database_methods.get_message_by_id(notes_id)
        comments = database_methods.get_comments(notes_id)
        return render_template('comment.html', message=message, comments=comments)
    
@app.route('/add_comment', methods=["POST"])
def add_comment():
    if request.method == "POST":
        message_id = request.form["message"]
        comment = request.form["comment"]
        username = session["username"]
        user_id = database_methods.get_person_id(username)
        database_methods.add_comment(comment, user_id, message_id)
        message = database_methods.get_message_by_id(message_id)
        comments = database_methods.get_comments(message_id)
        return render_template('comment.html', message=message, comments=comments)
