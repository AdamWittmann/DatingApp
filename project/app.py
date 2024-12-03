"""app.py: render and route to webpages"""

from flask import request, render_template, redirect, url_for, session, jsonify

from sqlalchemy import insert, text, select
import datetime
from db.server import app
from db.server import db

from db.schema.likes import Likes
from db.schema.matches import Matches
from db.schema.user import User
from db.schema.profile import Profile
from db.schema.education import Education
from db.schema.profile import Profile
from db.schema.occupation import Occupation
from db.schema.physicalFeatures import PhysicalFeatures

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
    # Fetch profiles of the opposite gender
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    current_user = db.session.query(User).filter_by(Email=user_email).first()
    if not current_user:
        return redirect(url_for('login'))

    current_profile = db.session.query(Profile).filter_by(UserID=current_user.UserID).first()
    if not current_profile:
        return redirect(url_for('profileSettings'))

    # Find profiles matching the user's gender preference
    opposite_profiles = db.session.query(Profile, User).join(User, Profile.UserID == User.UserID).filter(Profile.Gender == current_profile.GenderPreference, Profile.GenderPreference == current_profile.Gender).all()

    if not opposite_profiles:
        return render_template("filtr.html", profile=None)

    # Select the first profile from the result (for simplicity)
    selected_profile = opposite_profiles[0]
    profile_data = {
        "user_id": selected_profile.User.UserID,
        "picture_url": USER_PICTURES.get(selected_profile.User.Email, "static/images/default.jpg"),
        "prompt": f"{selected_profile.User.FirstName}, {selected_profile.User.LastName}"
    }

    return render_template("filtr.html", profile=profile_data)

@app.route('/like', methods=['POST'])
def like():
    data = request.json
    liked_user_id = data.get('likedUserID')

    user_email = session.get('user_email')
    current_user = db.session.query(User).filter_by(Email=user_email).first()
    if not current_user:
        return jsonify({"message": "User not logged in."}), 403

    # Check if the liked user liked back
    mutual_like = db.session.query(Likes).filter_by(UserID=liked_user_id, LikedUserID=current_user.UserID).first()

    if mutual_like:
        # Create a match if mutual
        match = Matches(UserID1=current_user.UserID, UserID2=liked_user_id, MatchDate=datetime.now().strftime('%Y%m%d'))
        db.session.add(match)
        db.session.commit()

        # Fetch phone numbers to display
        liked_user = db.session.query(User).filter_by(UserID=liked_user_id).first()
        return jsonify({"message": "It's a match!", "match": True, "phoneNumbers": [current_user.PhoneNumber, liked_user.PhoneNumber]})

    # If no mutual like, just add the like entry
    new_like = Likes(UserID=current_user.UserID, LikedUserID=liked_user_id, DateLiked=datetime.now().strftime('%Y%m%d'))
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"message": "User liked successfully.", "match": False})

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

# @app.route('/profileSettings', methods=['GET', 'POST'])
# def profileSettings():
#     if request.method == 'POST':
#         query  = insert(Profile).values(request.form)
    
#         with app.app_context():
#             db.session.execute((query))
#             db.session.commit()
#             return redirect(url_for('profile'))
#     return render_template("profileSettings.html")
@app.route('/profileSettings', methods=['GET', 'POST'])
def profileSettings(): 
    if request.method == 'POST':
        # Retrieve the current user's email from the session
        user_email = session.get('user_email')
        if not user_email:
            return "User not logged in", 401  # Return unauthorized if no user is logged in
        
        # Retrieve the UserID from the User table
        user = db.session.query(User).filter_by(Email=user_email).first()
        if not user:
            return "User not found", 404  # Return not found if the user does not exist
        
        # Extract the UserID
        user_id = user.UserID
        
        # Include the UserID in the form data for the Profile table
        profile_data = request.form.to_dict()
        profile_data['UserID'] = user_id
        
        # Insert the profile data into the Profile table
        query = insert(Profile).values(profile_data)
        with app.app_context():
            db.session.execute(query)
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
def is_profile_complete():
    # Step 1: Get the ProfileID using the email
    profile_id = get_profile_id_by_user_email()
    if not profile_id:
        return False

    # Step 2: Fetch the Profile and check required fields
    profile = Profile.query.filter_by(ProfileID=profile_id).first()
    if not profile:
        return False

    # Step 3: Check for required fields
    required_fields = [profile.Gender, profile.Age, profile.Religion, profile.Bio, profile.GenderPreference]
    return all(required_fields)  # Returns True if all fields are filled, False otherwise
@app.route('/check-profile', methods=['GET'])
def check_profile():
    try:
        complete = is_profile_complete()
        return jsonify({'profileComplete': complete})
    except Exception as e:
        print(f"Error checking profile: {e}")
        return jsonify({'profileComplete': False, 'error': 'Server error'}), 500

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
