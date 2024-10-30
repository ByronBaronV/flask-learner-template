from flask import Flask, render_template, request, redirect, url_for, flash
import database as db
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for flash messages

# Configure upload settings
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def allowed_file(filename, allowed_extensions):
    """Check if the file extension is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


def handle_media_upload(files, post_id):
    """Handle uploaded files for a post"""
    if not files:
        return

    for file in files.getlist('media'):
        if file.filename == '':
            continue

        if file and (allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS) or
                     allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS)):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{post_id}{ext}"

            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # Determine media type
            media_type = 'video' if allowed_file(filename, ALLOWED_VIDEO_EXTENSIONS) else 'image'
            db.add_media(post_id, filename, media_type)


@app.route('/')
def home():
    """Display all blog posts on the home page"""
    posts = db.get_all_posts()
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Display a single blog post"""
    post = db.get_post(post_id)
    if post is None:
        return "Post not found", 404
    return render_template('post.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Handle new post creation"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Create the post first to get the ID
        post_id = db.create_post(title, content)

        # Handle file uploads
        handle_media_upload(request.files, post_id)

        return redirect(url_for('home'))
    return render_template('create.html')


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    """Handle post editing"""
    post = db.get_post(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db.update_post(post_id, title, content)

        # Handle new file uploads
        handle_media_upload(request.files, post_id)

        return redirect(url_for('home'))
    return render_template('edit.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Handle post deletion"""
    db.delete_post(post_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)