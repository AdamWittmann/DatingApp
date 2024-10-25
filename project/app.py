"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.user import User

# create a webpage based off of the html in templates/index.html
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        query  = insert(User).values(request.form)
        
        with app.app_context():
            db.session.execute((query))
            db.session.commit()

        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/filtr')
def filtr():
    return render_template("filtr.html")

@app.route('/messages')
def messages():
    return render_template("messages.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)

