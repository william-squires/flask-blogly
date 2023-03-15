"""Blogly application."""

import os

from flask import Flask ,redirect, request, render_template, jsonify
from models import connect_db
from models import User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def show_home():
    """Redirects to list of users"""

    return redirect("/users")

@app.get('/users')
def show_users():
    """Show list of all users"""

    users = User.query.all()
    return render_template ('user-list.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """Shows a form where we can create new users"""

    return render_template('add-user-form.html')

@app.post('/users/new')
def add_new_user():
    """Adds a new user to database and redirects to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img_url"]

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    User.add_user(user)

    return redirect('/users')