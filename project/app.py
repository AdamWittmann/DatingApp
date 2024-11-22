"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for, session
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.user import User
from db.schema.profile import Profile

app.secret_key = "your_unique_secret_key"
# create a webpage based off of the html in templates/index.html
USER_PICTURES = {
    "joe@foyc3.com": "static/images/Brock.png",
    "caden@foyc3.com": "static/images/Caden.png",
    "james@foyc3.com": "static/images/James.png",
    "chlorine@foyc3.com": "static/images/Chlorine.png",
    "alfredo@foyc3.com": "static/images/Alfredo.png",
    "camila@tables.com": "static/images/Camila.png",
    "valeria@tables.com": "static/images/Valeria.png",
    "maria@tables.com": "static/images/Maria.png",
    "mia@tables.com": "static/images/Mia.png",
    "nicole@tables.com": "static/images/Nicole.png",
}

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['Email']  # Retrieve the email from the form input

        # Check if the email already exists in the database
        with app.app_context():
            existing_user = db.session.query(User).filter_by(Email=email).first()

            if existing_user:
                # Email already exists; render the signup page with an error message
                error = "This email is already associated with an account."
                return render_template("signup.html", alert_message=error)

            # Email is not in the database; proceed to create the account
            query = insert(User).values(request.form)
            db.session.execute(query)
            db.session.commit()

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    # Render the signup page if the request method is GET
    return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        userEmail = request.form['Email']
        password = request.form['Password']

        user = db.session.query(User).filter_by(Email=userEmail).first()
        if user and user.Password == password:
            session['user_email'] = userEmail
            session['user_picture'] = USER_PICTURES.get(userEmail, "static/images/default.jpg")
            return redirect(url_for('filtr'))

        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/filtr')
def filtr():
    return render_template("filtr.html")

@app.route('/underConstruction')
def underConstruction():
    return render_template("underConstruction.html")

@app.route('/messages')
def messages():
    return render_template("messages.html")

@app.route('/profile')
def profile():
    user_picture = session.get('user_picture', "static/images/default.jpg")
    return render_template("profile.html", user_picture=user_picture)

@app.route('/profileSettings', methods=['GET', 'POST'])
def profileSettings():
    if request.method == 'POST':
        query  = insert(Profile).values(request.form)
            
        with app.app_context():
            db.session.execute((query))
            db.session.commit()
            return redirect(url_for('profile'))
    return render_template("profileSettings.html")

@app.route('/accountSettings', methods=['GET','POST'])
def accountSettings():
    if request.method == 'POST':
        email = request.form['email']
        currPassword = request.form['currPassword']
        newPassword = request.form['newPassword']
        
        userEmail = session.get('user_email')
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

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "Logout":
            session.clear() 
            return redirect(url_for('login'))

        elif action == "Delete Account" and userEmail:
            user = db.session.query(User).filter_by(Email=userEmail).first()

            if user:
                    db.session.delete(user)
                    db.session.commit()
                    session.clear() 
                    return redirect(url_for('signup'))
            else:
                return "User not found.", 404

    return render_template("settings.html")

if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)
