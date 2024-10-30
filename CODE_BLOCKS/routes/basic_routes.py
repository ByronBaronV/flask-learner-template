"""
Example code blocks for basic Flask routes.
Shows different route types and common patterns.
"""

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for flashing messages


# === BASIC ROUTE EXAMPLES ===

@app.route('/')
def home():
    """Basic route returning a template"""
    return render_template('home.html')


@app.route('/about')
def about():
    """Simple route returning text"""
    return 'About Page'


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Route handling both GET and POST methods"""
    if request.method == 'POST':
        # Process the form data
        email = request.form.get('email')
        message = request.form.get('message')

        # Do something with the data...
        print(f"Received message from {email}: {message}")

        # Flash a message to the user
        flash('Thank you for your message!')
        return redirect(url_for('home'))

    # If it's a GET request, show the contact form
    return render_template('contact.html')


# === ERROR HANDLING ROUTES ===

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 error page"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Custom 500 error page"""
    return render_template('500.html'), 500


# === REDIRECTING EXAMPLES ===

@app.route('/old-page')
def old_page():
    """Redirect example"""
    return redirect(url_for('home'))


@app.route('/external-redirect')
def external_redirect():
    """External redirect example"""
    return redirect('https://www.example.com')


# === TEMPLATE WITH VARIABLES ===

@app.route('/greet/<name>')
def greet(name):
    """Route with template variables"""
    return render_template('greet.html', name=name)


# === DEMO AREA ===
if __name__ == '__main__':
    app.run(debug=True)