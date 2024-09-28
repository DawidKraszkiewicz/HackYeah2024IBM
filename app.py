from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Models.User import db, User
from agents import TextProcessor
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use your DB connection string here
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET")  # For session management and CSRF protection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    session["logged_in"] = True
    session["suggestion"] = None
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                session["logged_in"] = True
                flash('Logged in successfully!', category='success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session["logged_in"] = False
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    if "logged_in" not in session:
        return redirect(url_for('home'))
    return render_template("dashboard.html", suggestion = session["suggestion"])


@app.route('/process_workout', methods=['POST'])
def process_workout():
    if "logged_in" not in session:
        return redirect(url_for('home'))
    text = request.form['input_workout']
    processor = TextProcessor()
    result = processor.workout_to_json(text)

    if isinstance(result, dict):
        result = json.dumps(result)

    suggestion = processor.suggest_workout(result)

    session["suggestion"] = suggestion
    return redirect(url_for('dashboard'))


@app.route('/history')
def history():
    if "logged_in" not in session:
        return redirect(url_for('home'))
    return render_template("history.html")