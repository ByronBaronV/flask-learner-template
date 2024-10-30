from flask import Flask, render_template, request, redirect, url_for
import database as db

app = Flask(__name__)


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
        db.create_post(title, content)
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
        return redirect(url_for('home'))
    return render_template('edit.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Handle post deletion"""
    db.delete_post(post_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)