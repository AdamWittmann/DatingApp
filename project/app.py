"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.user import User

# create a webpage based off of the html in templates/index.html
userEmail = None

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        query  = insert(User).values(request.form)
        
        with app.app_context():
            db.session.execute((query))
            db.session.commit()

        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    global userEmail

    if request.method == 'POST':

        userEmail = request.form['Email']
        password = request.form['Password']

        user = db.session.query(User).filter_by(Email=userEmail).first()
        if user and user.Password == password:
            return redirect(url_for('settings'))

        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/filtr')
def filtr():
    return render_template("filtr.html")

@app.route('/messages')
def messages():
    return render_template("messages.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/profileSettings', methods=['GET', 'POST'])
def profileSettings():
    query  = insert(User).values(request.form)
        
    with app.app_context():
        db.session.execute((query))
        db.session.commit()
    return render_template("profileSettings.html")

@app.route('/accountSettings', methods=['GET','POST'])
def accountSettings():
    if request.method == 'POST':
        email = request.form['email']
        currPassword = request.form['currPassword']
        newPassword = request.form['newPassword']

        user = db.session.query(User).filter_by(Email=userEmail).first()
        if user and (user.Password == currPassword):
            user.Password = newPassword
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return "User Not Found", 404

    return render_template("accountSettings.html")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global userEmail

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "Logout":
            userEmail = None
            return redirect(url_for('login'))

        elif action == "Delete Account" and userEmail:
            user = db.session.query(User).filter_by(Email=userEmail).first()

            if user:
                    db.session.delete(user)
                    db.session.commit()
                    userEmail = None 
                    return redirect(url_for('signup'))
            else:
                return "User not found.", 404

    return render_template("settings.html")

if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)
