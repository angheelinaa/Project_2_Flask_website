from flask import Blueprint, render_template, request, redirect, url_for, flash
from .model import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Success logging!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.my_events'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('This email does not exist.', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists.', category='error')
        elif len(email) < 5:
            flash('Enter a valid email address (5+ characters).', category='error')
        elif len(first_name) < 1:
            flash('Please enter your name.', category='error')
        elif len(password) < 8:
            flash('Please use 8+ characters for your password.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, 'sha256'))
            flash('Account created!', category='success')

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            return redirect(url_for('views.add_event'))

    return render_template('sign_up.html', user=current_user)


@auth.route('/<int:user_id>/delete_user')
@login_required
def delete_user(user_id):
    user = User.query.get(int(user_id))

    db.session.delete(user)
    db.session.commit()
    flash('Your account deleted!', category='success')

    return redirect(url_for('views.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))