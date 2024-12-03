"""app.py: render and route to webpages"""

from flask import request, render_template, redirect, url_for, session, jsonify

from sqlalchemy import insert, text, select
from datetime import datetime

from db.server import app
from db.server import db

from db.schema.matches import Matches
from db.schema.likes import Likes
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
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    current_user = db.session.query(User).filter_by(Email=user_email).first()
    if not current_user:
        return redirect(url_for('login'))

    current_profile = db.session.query(Profile).filter_by(UserID=current_user.UserID).first()
    if not current_profile:
        return redirect(url_for('profileSettings'))

    # Fetch profiles matching the preferred gender
    preferred_profiles = (
        db.session.query(Profile, User)
        .join(User, Profile.UserID == User.UserID)
        .filter(Profile.Gender == current_profile.GenderPreference, Profile.UserID != current_user.UserID)
        .all()
    )

    if not preferred_profiles:
        return render_template("filtr.html", profile=None)

    selected_profile, selected_user = preferred_profiles[0]

    # Ensure the email exists in the dictionary to retrieve the picture
    selected_email = selected_user.Email
    picture_url = USER_PICTURES.get(selected_email, "static/images/default.jpg")

    profile_data = {
        "user_id": selected_user.UserID,
        "user_email": selected_email,  # Email retrieved from the User table
        "picture_url": picture_url,  # Picture retrieved from the dictionary
        "first_name": selected_user.FirstName,
        "last_name": selected_user.LastName,
        "age": selected_profile.Age,
        "bio": selected_profile.Bio,
    }

    return render_template("filtr.html", profile=profile_data)

@app.route('/like', methods=['POST'])
def like():
    try:
        # Get the email of the liked user from the frontend
        data = request.json
        liked_user_email = data.get('likedUserEmail')

        if not liked_user_email:
            return jsonify({"message": "Liked user email is missing."}), 400

        # Get the current logged-in user
        user_email = session.get('user_email')
        current_user = db.session.query(User).filter_by(Email=user_email).first()
        if not current_user:
            return jsonify({"message": "User not logged in."}), 403

        # Get the liked user's UserID
        liked_user = db.session.query(User).filter_by(Email=liked_user_email).first()
        if not liked_user:
            return jsonify({"message": "Liked user does not exist."}), 404

        # Insert the new like into the Likes table
        new_like = Likes(
            UserID=current_user.UserID,
            LikedUserID=liked_user.UserID,
            DateLiked=datetime.now().strftime('%Y%m%d')
        )
        db.session.add(new_like)
        db.session.commit()

        # Check for mutual like
        mutual_like = db.session.query(Likes).filter_by(UserID=liked_user.UserID, LikedUserID=current_user.UserID).first()

        if mutual_like:
            # Create a match if mutual like exists
            match = Matches(
                UserID1=current_user.UserID,
                UserID2=liked_user.UserID,
                MatchDate=datetime.now().strftime('%Y%m%d')
            )
            db.session.add(match)
            db.session.commit()

            # Return match details including phone number
            return jsonify({
                "message": "It's a match!",
                "match": True,
                "phoneNumber": liked_user.PhoneNumber
            })

        return jsonify({"message": "User liked successfully.", "match": False})

    except Exception as e:
        print(f"Error in /like route: {e}")
        return jsonify({"message": "Server error.", "error": str(e)}),
        
@app.route('/next-profile', methods=['GET'])
def next_profile():
    try:
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({"error": "User not logged in."}), 403

        current_user = db.session.query(User).filter_by(Email=user_email).first()
        if not current_user:
            return jsonify({"error": "Current user not found."}), 404

        current_profile = db.session.query(Profile).filter_by(UserID=current_user.UserID).first()
        if not current_profile:
            return jsonify({"error": "Current user profile not found."}), 404

        # Fetch the next profile matching the preferred gender
        preferred_profiles = (
            db.session.query(Profile, User)
            .join(User, Profile.UserID == User.UserID)
            .filter(Profile.Gender == current_profile.GenderPreference, Profile.UserID != current_user.UserID)
            .all()
        )

        if not preferred_profiles:
            return jsonify({"error": "No more profiles available."}), 404

        selected_profile, selected_user = preferred_profiles[0]
        profile_data = {
            "user_id": selected_user.UserID,
            "picture_url": USER_PICTURES.get(selected_user.Email, "static/images/default.jpg"),
            "first_name": selected_user.FirstName,
            "last_name": selected_user.LastName,
            "age": selected_profile.Age,
            "bio": selected_profile.Bio,
        }

        return jsonify(profile_data)

    except Exception as e:
        print(f"Error in /next-profile route: {e}")
        return jsonify({"error": "Server error.", "details": str(e)}), 500

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
