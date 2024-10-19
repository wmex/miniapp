# app.py

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash
from database import db, User  # Import the database and User model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change the database URI as needed
db.init_app(app)
@app.before_request
def create_tables():
    db.create_all()
# Registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
@app.route('/')
def home():
    return redirect(url_for('register'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user with hashed password
        new_user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))  # Redirect to a login page or another page
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    return "Login Page"

if __name__ == '__main__':
    app.run(debug=True)
