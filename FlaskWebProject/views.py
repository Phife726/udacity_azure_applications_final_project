"""
Routes and views for the flask application.
"""

import logging
from flask import render_template, redirect, request, session, url_for
from config import Config
from FlaskWebProject import app, msal_app
from FlaskWebProject.forms import PostForm
from flask_login import current_user, login_user, logout_user, login_required
from FlaskWebProject.models import User, Post
import uuid

imageSourceUrl = 'https://'+ app.config['BLOB_ACCOUNT']  + '.blob.core.windows.net/' + app.config['BLOB_CONTAINER']  + '/'

@app.route('/')
@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    return render_template(
        'index.html',
        title='Home Page',
        posts=posts
    )

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        post = Post()
        post.save_changes(form, request.files['image_path'], current_user.id, new=True)
        return redirect(url_for('home'))
    return render_template(
        'post.html',
        title='Create Post',
        imageSource=imageSourceUrl,
        form=form
    )


@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get(int(id))
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        post.save_changes(form, request.files['image_path'], current_user.id)
        return redirect(url_for('home'))
    return render_template(
        'post.html',
        title='Edit Post',
        imageSource=imageSourceUrl,
        form=form
    )

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    session["state"] = str(uuid.uuid4())
    auth_url = msal_app.get_authorization_request_url(
        scopes=Config.SCOPE,
        state=session["state"],
        redirect_uri=url_for('get_a_token', _external=True),
    )
    return redirect(auth_url)

@app.route('/getAToken')
def get_a_token():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))  # No-OP. Goes back to Index page

    if "error" in request.args:  # Authentication/Authorization failure
        logging.warning("Invalid login attempt")
        return render_template("auth_error.html", result=request.args)

    if request.args.get('code'):
        result = msal_app.acquire_token_by_authorization_code(
            code=request.args.get('code'),
            scopes=Config.SCOPE,
            redirect_uri=url_for('get_a_token', _external=True),
        )
        if not result or "error" in result:
            logging.warning("Invalid login attempt")
            return render_template("auth_error.html", result=result)

        logging.info("admin logged in successfully")
        session["user"] = result.get("id_token_claims")
        # Note: In a real app, we'd use the 'name' property from session["user"] below
        # Here, we'll use the admin username for anyone who is authenticated by MS
        user = User.query.filter_by(username="admin").first()
        login_user(user)

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')
