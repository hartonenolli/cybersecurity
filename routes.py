from app import app
from flask import render_template, request, redirect, session
import database_methods

@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/register', methods=["POST"]) #02 03 07
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        user_exists = database_methods.get_person(username)
        if user_exists == None and password == password2:
            database_methods.add_person(username, password)
            return redirect('/')
        return redirect('/')

@app.route('/front_page', methods=["POST", "GET"]) #{csrf_token}
def front_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_exists = database_methods.get_person(username)
        user_password = database_methods.get_person_password(username, password)
        if user_exists == username and user_password == True:
            session["username"] = username
            messages = database_methods.get_messages()
            return render_template('front_page.html', username=username, messages=messages)
        return redirect('/')
    if request.method == "GET":
        username = session["username"]
        messages = database_methods.get_messages()
        return render_template('front_page.html', username=username, messages=messages)


@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        return redirect('/')

@app.route('/my_messages/<username>', methods=["GET"]) #01
def my_messages(username):
    if request.method == "GET":
        user_id = database_methods.get_person_id(username)
        messages = database_methods.get_my_messages(user_id)
        return render_template('my_messages.html', username=username, messages=messages)

@app.route('/message', methods=["POST"])
def message():
    if request.method == "POST":
        message = request.form["message"]
        return render_template('message.html', message=message)

@app.route('/add_message', methods=["POST"])
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