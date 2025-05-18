from werkzeug.utils import secure_filename# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from models import db, User, Event, Interest
from forms import RegisterForm, LoginForm, EventForm, InterestForm
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(os.path.join(app.root_path, 'static/uploads'), exist_ok=True)


db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    events = Event.query.filter(Event.start_time > datetime.now()).order_by(Event.start_time).all()
    return render_template('home.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registered! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    my_events = Event.query.filter_by(creator_id=current_user.id).all()
    registered = [i.event for i in current_user.registrations]
    return render_template('dashboard.html', my_events=my_events, registered_events=registered)

@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            upload_path = os.path.join(app.root_path, 'static/uploads', filename)
            form.photo.data.save(upload_path)

        event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            category=form.category.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            creator_id=current_user.id,
            photo_filename=filename  # ✅ Save image name
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created!')
        return redirect(url_for('dashboard'))
    return render_template('create_event.html', form=form)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = InterestForm()
    if form.validate_on_submit():
        reg = Interest(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            num_people=form.num_people.data,
            user_id=current_user.id if current_user.is_authenticated else None,
            event_id=event.id
        )
        db.session.add(reg)
        db.session.commit()
        flash('Interest registered!')
        return redirect(url_for('view_event', event_id=event.id))
    return render_template('event_detail.html', event=event, form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
