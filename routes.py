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
    

@app.route('/register', methods=["POST"])
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
        # and use it to check the password strength
        user_exists = database_methods.get_person(username)
        if user_exists == None and password == password2:
            # Here we sould hash the password
            # but this is not done
            # this is how it could be done:
            # importing werkzeug.security or other library
            # generating a hash from the password
            # storing the hash in the database
            database_methods.add_person(username, password)
            return redirect('/')
        error_msg = "Username is already in use or passwords do not match"
        return render_template('try_again.html', error_msg=error_msg)
    # if request.method == "POST":
    #     username = request.form["username"]
    #     password = request.form["password"]
    #     password2 = request.form["password2"]
    #     password_strength = zxcvbn.password_strength(password)
    #     if password_strength < 3:
    #         error_msg = "Password is not strong enough"
    #         return render_template('try_again.html', error_msg=error_msg)
    #     if len(password) < 8 or re.search('[0-9]', password) is None or re.search('[A-Z]', password) is None or re.search('[a-z]', password) is None:
    #         error_msg = "Password is not strong enough"
    #         return render_template('try_again.html', error_msg=error_msg)
    #     if username == password:
    #         error_msg = "Username and password cannot be the same"
    #         return render_template('try_again.html', error_msg=error_msg)
    #     user_exists = database_methods.get_person(username)
    #     if user_exists == None and password == password2:
    #         password_hash = werkzeug.security.generate_password_hash(password)
    #         database_methods.add_person(username, password_hash)
    #         return redirect('/')
    #     error_msg = "Username is already in use or passwords do not match"
    #     return render_template('try_again.html', error_msg=error_msg)

@app.route('/front_page', methods=["POST", "GET"])
def front_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Here is a injection vulnerability
        # malicious user could use the following values
        # username = "arska"
        # password = "' OR id='1"
        # and being able to log in to arskas account
        # database method should return only the username and password
        # now it return Boolean
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
                session["username"] = username
                # Here we should generate a new csrf token
                # and store it in the session
                # we should start by importin secrets
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
    # if request.method == "POST":
    #     username = request.form["username"]
    #     password = request.form["password"]
    #     hashed_password = werkzeug.security.generate_password_hash(password)
    #     user_data = database_methods.get_person_name_and_pass(username, hashed_password)
    #     try:
    #         if user_data[0][0] == username and user_data[0][1] == hashed_password:
    #             session["username"] = username
    #             session["csrf_token"] = secrets.token_hex(16)
    #             messages = database_methods.get_messages()
    #             return render_template('front_page.html', username=username, messages=messages)
    #     except Exception:
    #         pass
    #     error_msg = "Username or password is incorrect"
    #     return render_template('try_again.html', error_msg=error_msg)
    # if request.method == "GET":
    #     username = session["username"]
    #     messages = database_methods.get_messages()
    #     return render_template('front_page.html', username=username, messages=messages)

@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        session.pop("username", None)
        # session.pop("csrf_token", None)
        return redirect('/')

@app.route('/my_messages/<username>', methods=["GET"]) #01
def my_messages(username):
    if request.method == "GET":
        user_id = database_methods.get_person_id(username)
        messages = database_methods.get_my_messages(user_id)
        return render_template('my_messages.html', username=username, messages=messages)
    # Here we have broken access control
    # method should be POST
    # app should check if the user is logged in
    # but this is not done
    # this is how it could be done:
    # if request.method == "POST":
    #     username = session["username"]
    #     if username != username:
    #         abort(403)
    #     user_id = database_methods.get_person_id(username)
    #     messages = database_methods.get_my_messages(user_id)
    #     return render_template('my_messages.html', username=username, messages=messages)

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
        return render_template('front_page.html', username=username, messages=messages)

@app.route('/delete_message', methods=["POST"])
def delete_message():
    if request.method == "POST":
        notes_id = request.form["message"]
        database_methods.delete_message_and_comments(notes_id)
        username = session["username"]
        user_id = database_methods.get_person_id(username)
        messages = database_methods.get_my_messages(user_id)
        return render_template('my_messages.html', username=username, messages=messages)

@app.route('/delete_user/<username>', methods=["GET"])
def delete_user(username):
    if request.method == "GET":
        if session["username"] != username:
            abort(403)
        return render_template('delete_user.html', username=username)
    # Here we should check the csrf token
    # and the method should be POST
    # but this is not done
    # this is how it could be done:
    # if request.method == "POST":
    #    if session["username"] != username:
    #    if session["csrf_token"] != request.form["csrf_token"]:
    #        abort(403)
    #    return render_template('delete_user.html', username=username)

@app.route('/delete_confirm/<username>', methods=["GET"])
def delete_user_confirm(username):
    if request.method == "GET":
        if session["username"] != username:
            abort(403)
        user_id = database_methods.get_person_id(username)
        database_methods.delete_user_and_messages(user_id)
        session.pop("username", None)
        return redirect('/')
    # Here we should check the csrf token
    # and the method should be POST
    # but this is not done
    # this is how it could be done:
    # if request.method == "POST":
    #    if session["username"] != username:
    #        abort(403)
    #    if session["csrf_token"] != request.form["csrf_token"]:
    #        abort(403)
    #    user_id = database_methods.get_person_id(username)
    #    database_methods.delete_user_and_messages(user_id)
    #    session.pop("username", None)
    #    return redirect('/')


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
