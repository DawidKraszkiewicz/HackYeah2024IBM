from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from Models.User import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use your DB connection string here
app.config['SECRET_KEY'] = 'your_secret_key'  # For session management and CSRF protection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/rejestracja', methods=['GET'])
def show_register():
    return render_template('rejestracja.html')

@app.route('/logowanie')
def show_login():
    return render_template('templates/logowanie.html')

# ----- Actions -----
# These routes handle the form submissions for registration and login

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Check if the email is already registered
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists.')
        return redirect(url_for('show_register'))

    # Hash the password and create a new user
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    
    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! Please log in.')
    return redirect(url_for('show_login'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Fetch the user from the database by email
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and if the password is correct
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id  # Store user id in session
        flash('Login successful!')
        return redirect(url_for('dashboard'))  # Redirect to a protected page (e.g., dashboard)
    else:
        flash('Invalid email or password.')
        return redirect(url_for('show_login'))

# Protected route (example)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('show_login'))
    return "Welcome to your dashboard!"

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('show_login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
