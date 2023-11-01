from app import app
from flask import render_template, request, redirect, session
import database_methods

@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/front_page', methods=["POST"])
def front_page():
    if request.method == "POST":
        username = request.form["username"]
        user_exists = database_methods.get_person(username)
        if user_exists == username:
            session["username"] = username
            return render_template('front_page.html')
        return redirect('/')


@app.route('/logout', methods=["POST"])
def logout():
    if request.method == "POST":
        return redirect('/')
