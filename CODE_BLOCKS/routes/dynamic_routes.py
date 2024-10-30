"""
Examples of dynamic Flask routes with URL parameters and query strings.
Shows how to handle variable parts in URLs.
"""

from flask import Flask, render_template, request, abort

app = Flask(__name__)


# === URL PARAMETER EXAMPLES ===

@app.route('/user/<username>')
def user_profile(username):
    """Route with string parameter"""
    return f'Profile page for {username}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Route with integer parameter"""
    # Example of handling non-existent resources
    if post_id > 100:  # Just an example condition
        abort(404)
    return f'Showing post {post_id}'


@app.route('/products/<category>/<int:product_id>')
def product_detail(category, product_id):
    """Route with multiple parameters"""
    return f'Product {product_id} in category {category}'


# === QUERY STRING EXAMPLES ===

@app.route('/search')
def search():
    """Route handling query strings"""
    # Get query parameters with defaults
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'newest')

    return f'Search for: {query} (Page {page}, Sort: {sort})'


@app.route('/filter')
def filter_items():
    """Route with multiple query parameters"""
    # Get all query parameters as a dictionary
    filters = request.args.to_dict()

    # Example: /filter?category=books&min_price=10&max_price=50
    return f'Filters applied: {filters}'


# === PATH CONVERTERS ===

@app.route('/files/<path:filepath>')
def serve_file(filepath):
    """Route with path converter for full paths"""
    return f'Would serve: {filepath}'


@app.route('/color/<any(red,green,blue):color>')
def show_color(color):
    """Route with custom converter for specific values"""
    return f'Selected color: {color}'


# === OPTIONAL PARAMETERS ===

@app.route('/page/')
@app.route('/page/<int:num>')
def show_page(num=1):
    """Route with optional parameter"""
    return f'Showing page {num}'


# === URL BUILDING EXAMPLES ===

@app.route('/url-examples')
def url_examples():
    """Examples of building URLs with url_for"""
    from flask import url_for

    # Build some example URLs
    urls = {
        'home': url_for('home'),
        'user': url_for('user_profile', username='john'),
        'search': url_for('search', q='flask', page=2),
        'product': url_for('product_detail', category='books', product_id=123)
    }

    return f'Example URLs: {urls}'


# === DEMO AREA ===
if __name__ == '__main__':
    app.run(debug=True)