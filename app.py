from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from forms import RegistrationForm, LoginForm, QRScanForm
import qrcode
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from models import User, Lecture, Attendance

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
            year=form.year.data if form.role.data == 'student' else None
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# QR Code Routes
@app.route('/generate_qr/<int:lecture_id>')
@login_required
def generate_qr(lecture_id):
    if current_user.role != 'instructor':
        return redirect(url_for('home'))
    
    lecture = Lecture.query.get_or_404(lecture_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"lecture:{lecture_id}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(app.config['QR_CODE_FOLDER'], f'lecture_{lecture_id}.png')
    img.save(qr_path)
    
    lecture.qr_code = qr_path
    db.session.commit()
    
    return redirect(url_for('instructor_dashboard'))

@app.route('/scan_qr', methods=['GET', 'POST'])
@login_required
def scan_qr():
    if current_user.role != 'student':
        return redirect(url_for('home'))
    
    form = QRScanForm()
    if form.validate_on_submit():
        # Process QR code scan and photo proof
        # This would be implemented with JavaScript in a real app
        flash('Attendance recorded successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('dashboard_student.html', form=form)

# Basic Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'instructor':
            return redirect(url_for('instructor_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard_admin.html')

@app.route('/instructor/dashboard')
def instructor_dashboard():
    return render_template('dashboard_instructor.html')

@app.route('/student/dashboard')
def student_dashboard():
    return render_template('dashboard_student.html')

if __name__ == '__main__':
    app.run(debug=True)
