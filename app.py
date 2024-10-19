# app.py

from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from database import db, User  # Import the database and User model
from forms import RegistrationForm, LoginForm  # Import forms from the forms module
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import BASE_URL

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change the database URI as needed
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for("register"))
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            is_hr = form.role.data == 'hr'
            is_candidate = form.role.data == 'candidate'
            new_user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                is_hr=is_hr,
                is_candidate=is_candidate
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(f"{BASE_URL}/login")
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)  # Log in the user
            flash('Login successful!', 'success')
            return redirect(f"{BASE_URL}/main")  # Redirect to the main page
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)
@app.route('/main')
@login_required
# Require login to access this route
def main():
    return render_template('main_page.html', username=current_user.username)

@app.route('/profile')
def profile():
    return render_template('profile.html', username=current_user.username)  # Create a profile.html template


if __name__ == '__main__':
    app.run(debug=False)
