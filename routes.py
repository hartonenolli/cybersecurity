from app import app
from flask import render_template, request, redirect, session
import database_methods

@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/front_page', methods=["POST", "GET"])
def front_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_exists = database_methods.get_person(username)
        user_password = database_methods.get_person_password(username, password)
        if user_exists == username and user_password == True:
            session["username"] = username
            messages = database_methods.get_messages()
            return render_template('front_page.html', messages=messages)
        return redirect('/')
    if request.method == "GET":
        messages = database_methods.get_messages()
        return render_template('front_page.html', messages=messages)


@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        return redirect('/')

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