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
app.config['SECRET_KEY'] = "shhhh-quiet!"

connect_db(app)

# debug = DebugToolbarExtension(app)

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

    user = User.query.get_or_404(user_id)
    user.edit_user(first_name, last_name, image_url)

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user from database"""

    user = User.query.get_or_404(user_id)
    
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

######################################################
@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Showd new post form for user"""

    user = User.query.get_or_404(user_id)

    return render_template("new-post-form.html", user=user)

@app.post('/users/<int:user_id>/posts/new')
def create_new_post(user_id):
    """Creates new user post"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    Post.add_new_post(post)

    return redirect(f'/users/{ user_id }')    

@app.get('/posts/<int:post_id>')
def show_post_info(post_id):
    """Shows post information for an individual post"""

    post = Post.query.get_or_404(post_id)

    return render_template('post-detail-page.html', post=post)

@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Shows form to edit post"""

    post = Post.query.get_or_404(post_id)

    return render_template('post-edit-page.html', post=post)

@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Updates post in database"""

    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.get_or_404(post_id)

    post.edit_post(title, content)

    return redirect(f'/users/{post.user.id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes post"""

    post = Post.query.get_or_404(post_id)
    id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{id}')

