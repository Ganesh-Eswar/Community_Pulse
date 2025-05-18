# app.py

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os, uuid

from config import Config
from models import db, User, Event, RSVP
from forms import RegisterForm, LoginForm, EventForm, RSVPForm
from utils import log_event_action, log_admin_action

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# =================== Utility Decorator ===================

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# =================== Public Routes ===================

@app.route('/')
def home():
    events = Event.query.filter(Event.approved == True, Event.status == 'active').order_by(Event.start_time).all()
    return render_template('home.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, phone=form.phone.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('home'))

# =================== User Dashboard ===================

@app.route('/dashboard')
@login_required
def dashboard():
    # All events created by the current user (approved or not)
    my_events = Event.query.filter_by(created_by=current_user.id).order_by(Event.start_time).all()

    # All RSVPs submitted by this user (if any)
    my_rsvps = RSVP.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', my_events=my_events, my_rsvps=my_rsvps)


# =================== Event Routes ===================

@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    print("[DEBUG] Entered create_event route")

    if request.method == 'POST':
        print("[DEBUG] Form errors:", form.errors)

    if form.validate_on_submit():
        print("[DEBUG] Form validated")

        photo_filenames = []
        if request.files.getlist('photos'):
            for file in request.files.getlist('photos'):
                if file.filename:
                    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(upload_path)
                    photo_filenames.append(filename)

        event = Event(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            location=form.location.data,
            lat=form.lat.data,
            lng=form.lng.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            photos=",".join(photo_filenames),
            created_by=current_user.id,
            approved=False,
            status='active'
        )

        db.session.add(event)
        db.session.commit()
        log_event_action(event.id, current_user.id, 'Created', f"Event '{event.title}' created")
        flash("Event submitted for approval.")
        return redirect(url_for('dashboard'))

    return render_template('create_event.html', form=form)


@app.route('/event/<string:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    form = RSVPForm()

    rsvps = RSVP.query.filter_by(event_id=event.id).all() if current_user.is_authenticated and (
        current_user.id == event.created_by or current_user.role == 'admin') else None

    if form.validate_on_submit() and not rsvps:
        rsvp = RSVP(
            event_id=event.id,
            user_id=current_user.id if current_user.is_authenticated else None,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            num_guests=form.num_guests.data
        )
        db.session.add(rsvp)
        db.session.commit()
        log_event_action(event.id, current_user.id if current_user.is_authenticated else None, 'RSVPd', f"{form.name.data} registered")
        flash('You have successfully registered your interest.')
        return redirect(url_for('event_detail', event_id=event.id))

    return render_template('event_detail.html', event=event, form=form, rsvps=rsvps)

@app.route('/event/<string:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.id != event.created_by and current_user.role != 'admin':
        abort(403)

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.category = form.category.data
        event.location = form.location.data
        event.lat = form.lat.data
        event.lng = form.lng.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data

        if request.files.getlist('photos'):
            new_photos = []
            for file in request.files.getlist('photos'):
                if file.filename:
                    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new_photos.append(filename)
            if event.photos:
                event.photos += "," + ",".join(new_photos)
            else:
                event.photos = ",".join(new_photos)

        db.session.commit()
        log_event_action(event.id, current_user.id, 'Updated', 'Event updated')
        flash('Event updated successfully.')
        return redirect(url_for('event_detail', event_id=event.id))

    return render_template('edit_event.html', form=form)

@app.route('/event/<string:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.id != event.created_by and current_user.role != 'admin':
        abort(403)

    db.session.delete(event)
    db.session.commit()
    log_event_action(event.id, current_user.id, 'Deleted', 'Event deleted')
    flash('Event deleted.')
    return redirect(url_for('dashboard'))

# =================== Admin Routes ===================
@app.route('/admin')
@admin_required
def admin_panel():
    from models import Event, User

    # Fetch event + creator user via JOIN
    pending_events = db.session.query(Event, User).join(User, Event.created_by == User.id)\
        .filter(Event.approved == False).all()

    # Get users to verify
    pending_users = User.query.filter(User.verified_organizer == False, User.role != 'admin').all()

    return render_template('admin_panel.html', pending_events=pending_events, pending_users=pending_users)



@app.route('/admin/approve/event/<string:event_id>')
@admin_required
def admin_approve_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.approved = True
    db.session.commit()
    log_admin_action(current_user.id, 'approve', event_id, 'Event approved')
    flash(f'Event "{event.title}" approved.')
    return redirect(url_for('admin_panel'))

@app.route('/admin/reject/event/<string:event_id>')
@admin_required
def admin_reject_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    log_admin_action(current_user.id, 'reject', event_id, 'Event rejected and deleted')
    flash(f'Event "{event.title}" rejected and deleted.')
    return redirect(url_for('admin_panel'))

@app.route('/admin/verify/user/<string:user_id>')
@admin_required
def admin_verify_user(user_id):
    user = User.query.get_or_404(user_id)
    user.verified_organizer = True
    db.session.commit()
    log_admin_action(current_user.id, 'verify_organizer', user_id, 'User verified as organizer')
    flash(f'User "{user.name}" verified as organizer.')
    return redirect(url_for('admin_panel'))

# =================== Run App ===================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        from models import User, Event
        from werkzeug.security import generate_password_hash
        from datetime import datetime, timedelta

        # ✅ Admin user
        admin_email = 'admin@pulse.com'
        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            admin = User(
                name='Admin',
                email=admin_email,
                phone='9999999999',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('[✔] Admin account created (admin@pulse.com / admin123)')
        else:
            print('[i] Admin already exists.')
    app.run(debug=True)
