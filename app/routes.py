from app import flasko, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

# rute
@flasko.route("/")
@login_required
def home():
    user = {"name": "Edrick", "title": "My Blog"}
    posts = [
        {"author": "William", "judul": "To be or not to be"},
        {"author": "Miriam", "judul": "Matahari"},
        {"author": "Harry", "judul": "Live at london"},
    ]
    return render_template("index.html", posts=posts)


@flasko.route("/about")
def about():
    return render_template("about.html", title="About")


@flasko.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') 
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template("login.html", title="Log In", form=form)

@flasko.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@flasko.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # simpan ke database
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
