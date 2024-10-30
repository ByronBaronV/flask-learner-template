"""
Examples of handling forms in Flask routes.
Shows different ways to process form data and handle file uploads.
"""

from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for flash messages


# === BASIC FORM HANDLING ===

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Example of basic form handling"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Basic validation
        if not username or not password:
            flash('Please fill in all fields')
            return redirect(url_for('login'))

        # Process the login (example only)
        if username == 'admin' and password == 'password':
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')


# === FORM WITH MULTIPLE INPUTS ===

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Example of handling multiple form inputs"""
    if request.method == 'POST':
        # Get all form data
        data = {
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password')
        }

        # Validation
        errors = []
        if not data['username']:
            errors.append('Username is required')
        if not data['email'] or '@' not in data['email']:
            errors.append('Valid email is required')
        if data['password'] != data['confirm_password']:
            errors.append('Passwords do not match')

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('register'))

        # Process registration...
        flash('Registration successful!')
        return redirect(url_for('home'))

    return render_template('register.html')


# === FILE UPLOAD HANDLING ===

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Helper function to check file extensions"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Example of file upload handling"""
    if request.method == 'POST':
        # Check if file was included in request
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload_file'))

        file = request.files['file']

        # Check if file was selected
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload_file'))

        # Process valid file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid file type')
            return redirect(url_for('upload_file'))

    return render_template('upload.html')


# === HANDLING CHECKBOX AND SELECT INPUTS ===

@app.route('/preferences', methods=['GET', 'POST'])
def update_preferences():
    """Example of handling various form input types"""
    if request.method == 'POST':
        # Checkboxes (returns None if not checked)
        notifications = request.form.get('notifications') == 'on'
        newsletter = request.form.get('newsletter') == 'on'

        # Select dropdown
        theme = request.form.get('theme')

        # Multiple select (returns list)
        interests = request.form.getlist('interests')

        # Radio buttons
        contact_method = request.form.get('contact_method')

        # Process preferences...
        flash('Preferences updated!')
        return redirect(url_for('home'))

    return render_template('preferences.html')


# === DEMO AREA ===
if __name__ == '__main__':
    app.run(debug=True)