from flask import Flask, render_template, request, redirect, url_for, flash
import database as db
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# File upload configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def allowed_file(filename, allowed_extensions):
    """Checks if the uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def handle_media_upload(files, post_id):
    """Process uploaded media files for a post
    Args:
        files: The files from request.files
        post_id: The ID of the post to attach media to
    """
    if not files:
        return

    for file in files.getlist('media'):
        if file.filename == '':
            continue

        if file and (allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS) or
                     allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS)):
            # Secure filename and add post_id to prevent naming conflicts
            filename = secure_filename(file.filename)
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{post_id}{ext}"

            # Save file and record in database
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            media_type = 'video' if allowed_file(filename, ALLOWED_VIDEO_EXTENSIONS) else 'image'
            db.add_media(post_id, filename, media_type)


# Basic Routes
@app.route('/')
def home():
    """Homepage - shows all posts"""
    posts = db.get_all_posts()
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View a single post
    Args:
        post_id: ID of the post to display
    """
    post = db.get_post(post_id)
    if post is None:
        return "Post not found", 404
    return render_template('post.html', post=post)


# Post Management Routes
@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new post
    GET: Show the create form
    POST: Process the form and create post
    """
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        content = request.form['content']

        # Create post and handle any uploaded files
        post_id = db.create_post(title, content)
        handle_media_upload(request.files, post_id)

        return redirect(url_for('home'))
    return render_template('create.html')


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    """Edit an existing post
    Args:
        post_id: ID of the post to edit
    GET: Show the edit form
    POST: Process the form and update post
    """
    post = db.get_post(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update post content
        title = request.form['title']
        content = request.form['content']
        db.update_post(post_id, title, content)

        # Handle any new uploaded files
        handle_media_upload(request.files, post_id)
        return redirect(url_for('home'))

    return render_template('edit.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a post and its media
    Args:
        post_id: ID of the post to delete
    """
    db.delete_post(post_id)  # This also deletes associated media
    return redirect(url_for('home'))


# Media Management Route
@app.route('/delete-media/<int:media_id>')
def delete_media(media_id):
    """Delete a single media item
    Args:
        media_id: ID of the media to delete
    """
    # Get post_id for redirect before deleting media
    conn = db.get_db_connection()
    media = conn.execute('SELECT post_id FROM media WHERE id = ?', (media_id,)).fetchone()
    conn.close()

    if media:
        post_id = media['post_id']
        db.delete_media(media_id)
        flash('Media deleted successfully')
        return redirect(url_for('edit', post_id=post_id))

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)