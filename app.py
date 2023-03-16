"""Blogly application."""

import os
# get rid of unused imports
from flask import Flask, redirect, request, render_template, jsonify
from models import connect_db
from models import User, Post
from flask_debugtoolbar import DebugToolbarExtension

DEFAULT_IMAGE_URL = "https://i.pinimg.com/474x/97/7f/e7/977fe798cf2c3a037e7aa9af6ce4b9d1.jpg"

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

    users = User.query.order_by(User.id).all()
    return render_template('user-list.html', users=users)


@app.get('/users/new')
def show_new_user_form():
    """Shows a form where we can create new users"""

    return render_template('add-user-form.html')


@app.post('/users/new')
def add_new_user():
    """Adds a new user to database and redirects to /users"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img_url"] or DEFAULT_IMAGE_URL

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    User.add_user(user)

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows infomation about user"""

    user = User.query.get_or_404(user_id)

    return render_template("user-details.html", user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """show edit page for user"""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user-form.html", user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Get data from edit page form and update in database"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img_url"]

    user = User().query.get_or_404(user_id)
    User.edit_user(user, first_name, last_name, image_url)

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user from database"""

    user = User().query.get_or_404(user_id)
    User.delete_user(user)

    return redirect('/users')
