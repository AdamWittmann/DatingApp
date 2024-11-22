"""app.py: render and route to webpages"""
from flask import request, render_template, redirect, url_for,jsonify
from sqlalchemy import insert, text, select

from db.server import app
from db.server import db

from db.schema.user import User
from db.schema.profile import Profile
from db.schema.education import Education
from db.schema.profile import Profile
from db.schema.occupation import Occupation
from db.schema.physicalFeatures import PhysicalFeatures

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
    return render_template("profile.html")

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

#education form submit query:
@app.route('/enterEducation', methods=['POST','GET'])
def enterEducation():
    if request.method == 'GET':
        # Render the education form for GET requests
        return render_template("enterEducation.html")
    if request.method =='POST':
        query  = insert(Education).values(request.form)
        with app.app_context():
            db.session.execute((query))
            db.session.commit()
        return render_template("enterEducation.html")

def get_user_id_by_email():
    user_email = session.get('userEmail')  # Retrieve from session
    if not user_email:
        return None

    user = User.query.filter_by(Email=user_email).first()
    if user:
        return user.UserID  # Assuming 'UserID' is the primary key
    return None

def get_profile_id_by_user_email():
    # Step 1: Get UserID from the User schema
    user_id = get_user_id_by_email()
    if not user_id:
        return None

    # Step 2: Query the Profile schema using UserID
    profile = Profile.query.filter_by(UserID=user_id).first()
    if profile:
        return profile.ProfileID
    return None

@app.route('/check-profile', methods=['GET'])
def check_profile():
    profile_id = get_profile_id_by_user_email()  # Use the updated helper
    if not profile_id:
        return jsonify({'profileComplete': False, 'error': 'Profile not found'}), 404

    complete = is_schema_complete(profile_id)
    return jsonify({'profileComplete': complete})

@app.route('/enterOccupation', methods=['GET', 'POST'])
def enterOccupation():
    # if request.method == 'GET':
    if request.method == 'POST':
        query = insert(Occupation).values(request.form)
        with app.app_context():
            db.session.execute((query))
            db.session.commit()
    
    return render_template("enterOccupation.html")
@app.route('/physicalFeatures', methods=['GET','POST'])
def physicalFeatures():
    if request.method == 'POST':
        query = insert(PhysicalFeatures).values(request.form)
        with app.app_context():
            db.session.execute((query))
            db.session.commit()
    return render_template("physicalFeatures.html")

    

    return jsonify({'message': 'Physical features saved successfully!'})
if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)
