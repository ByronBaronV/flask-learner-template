# Python Flask Blog Project Template

Welcome to your final project template! This is a starting point for building your own web application using Flask. Don't worry if some of this seems complex - you can build your project step by step, and there are example code blocks to help you along the way.

## 🎯 Project Overview
This template is set up for a basic blog website where you can:
- View all posts on the home page
- Create new posts
- Edit existing posts
- Delete posts
- Style your pages with CSS

You can modify this template to build something completely different! The core features (database, web pages, forms) can be adapted for many types of projects.

## 📁 Project Structure
```
flask_learner_template/
├── static/                # CSS, images, etc.
│   └── css/
│       └── style.css     # Pre-made styles you can use
│
├── templates/            # Your HTML files
│   ├── base.html        # The main template other pages use
│   ├── home.html        # Home page
│   ├── post.html        # Single post view
│   ├── create.html      # Create post form
│   └── edit.html        # Edit post form
│
├── CODE_BLOCKS/          # Example code you can copy
│   ├── database/        # Database examples
│   ├── routes/          # Route examples
│   └── templates/       # Template examples
│
├── __init__.py          # Makes Python treat this folder as a package
├── app.py               # Your main application file
├── database.py          # Database setup and functions
└── requirements.txt     # Python packages needed
```

## 🚀 Getting Started

1. Make sure your virtual environment is activated (PyCharm should do this automatically)

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python database.py
   ```
   This will create your database file and add some sample data.

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and go to: `http://127.0.0.1:5000/`

## 📦 Package Versions
We're using these specific versions for stability:
- Flask==2.0.3
- Werkzeug==2.0.3
- flask-sqlalchemy==2.5.1

## 🔨 Building Your Project

1. Start by exploring the working blog example
2. Look through the CODE_BLOCKS folder for examples
3. Modify the HTML templates to change how pages look
4. Update the CSS to style your pages
5. Modify the database structure for your needs
6. Add new routes in app.py for new features

Remember to:
- Test your changes frequently
- Keep your code organized
- Comment your code to explain what it does
- Ask for help if you get stuck!

## 💡 Project Ideas
You could modify this template to build:
- A personal portfolio
- An online store
- A recipe collection
- A movie review site
- A student club website
- A photo gallery
- ...or anything else you can think of!

## 🆘 Getting Help
1. Check the comments in the code files
2. Look at the example CODE_BLOCKS
3. Ask your classmates
4. Ask your instructor
5. Google the error message if something's not working

## 🎉 Final Tips
- Start small and add features gradually
- Test each new feature before moving on
- It's okay to use the example code blocks - that's what they're for!
- Have fun building your project!

Good luck! Remember, every programmer started somewhere, and making mistakes is part of learning. 🌟