from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .model import Event
from . import db
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html', user=current_user)


@views.route('/add-event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        description = request.form.get('description')

        if len(title) < 1:
            flash('Please add title for your event.', category='error')
        else:
            new_event = Event(title=title, date=date, description=description, user_id=current_user.id)
            flash('Your event added!', category='success')

            db.session.add(new_event)
            db.session.commit()

            return redirect(url_for('views.my_events'))

    return render_template('add_event.html', user=current_user, default_date=datetime.now().date())


@views.route('/<int:event_id>/edit_event', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get(int(event_id))

    if request.method == 'POST':
        new_title = request.form.get('title')
        new_date = request.form.get('date')
        new_description = request.form.get('description')

        if len(new_title) < 1:
            flash('Please add title for your event.', category='error')
        else:
            event.title = new_title
            event.date = new_date
            event.description = new_description
            flash('Your event updated!', category='success')

            db.session.commit()
            return redirect(url_for('views.my_events'))

    return render_template('edit_event.html', event=event, user=current_user, default_date=datetime.now().date())


@views.route('/<int:event_id>/delete_event')
@login_required
def delete_event(event_id):
    event = Event.query.get(int(event_id))

    db.session.delete(event)
    db.session.commit()
    flash('Your event deleted!', category='success')

    return redirect(url_for('views.my_events'))


@views.route('/my-events', methods=['GET', 'POST'])
@login_required
def my_events():
    events = Event.query.where(current_user.id == Event.user_id).order_by(Event.date).all()
    return render_template('my_events.html', user=current_user, events=events)