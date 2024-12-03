.. _`Resources`:

Resources
=========
This section describes class and functions private to DatingApp. It is intended to document how the application works

DatingApp.db.schema.education.py
-------------------------------------

Takes user's education info

.. py:class:: Education(db.model)
    _tablename__ = 'Education'
    EducationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer,db.ForeignKey('Profile.ProfileID'))
    Degree = db.Column(db.String(30))
    Major = db.Column(db.String(30))
    GraduationYear = db.Column(db.String(4))
    School = db.Column(db.String(30))
    

DatingApp.db.schema.likes.py
-------------------------------------

stores information regarding likes

.. py:class:: Likes(db.model)
    __tablename__ = 'Likes'
    LikeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    LikedUserID = db.Column(db.Integer)
    DateLiked = db.Column(db.String(8))
    
    

DatingApp.db.schema.matches.py
-------------------------------------

stores information regarding matches

.. py:class:: Matches(db.model)
    __tablename__ = 'Matches'
    MatchID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID1 = db.Column(db.Integer)
    UserID2 = db.Column(db.Integer)
    MatchDate = db.Column(db.String(8))
    
    

DatingApp.db.schema.occupation.py
-------------------------------------

stores information regarding user's occupation/salary

.. py:class:: Occupation(db.model)
    __tablename__ = 'Occupation'
    OccupationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer, db.ForeignKey('Profile.ProfileID'))
    Job = db.Column(db.String(25))
    Salary = db.Column(db.Integer)
    
DatingApp.db.schema.physicalFeatures.py
-------------------------------------

stores information about users physical features

.. py:class:: PhysicalFeatures(db.model)
    __tablename__ = 'PhysicalFeatures'
    FeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer,db.ForeignKey('Profile.ProfileID'))    
    HairColor = db.Column(db.String(20))
    Height = db.Column(db.Integer)
    Weight = db.Column(db.Integer)
    EyeColor = db.Column(db.String(20))

DatingApp.db.schema.profile.py
-------------------------------------

stores information about user's profile

.. py:class:: Profile(db.model)
    __tablename__ = 'Profile'
    ProfileID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    Gender = db.Column(db.String(255))
    Age = db.Column(db.Integer)
    Religion = db.Column(db.String(255))
    Bio = db.Column(db.String(255))
    GenderPreference = db.Column(db.String(25))
    Photo = db.Column(db.LargeBinary)
    Created = db.Column(db.String(8))
    Updated = db.Column(db.String(8))

DatingApp.db.schema.user.py
-------------------------------------

stores information about users


.. py:class:: User(db.model)
    __tablename__ = 'User'
    UserID = db.Column(db.Integer,primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(40))
    LastName = db.Column(db.String(40))
    Email = db.Column(db.String(40))
    PhoneNumber = db.Column(db.String(12))
    Password = db.Column(db.String(256))
    CreditCardNum = db.Column(db.String(12))
    ExpirationDate = db.Column(db.String(4))
    SecurityCode = db.Column(db.Integer)
    BillingAddress = db.Column(db.String(255))
    IsSub = db.Column(db.Boolean)
    SubStart = db.Column(db.String(6))
    SubEnd = db.Column(db.String(6))



DatingApp.db.server
------------------------
Creats all database tables

DatingApp.static.css.accountSettings.css
-------------------------------------
Style for account settings page

DatingApp.static.css.educationOccupation.css
-------------------------------------
Style for education occupation page

DatingApp.static.css.filtr.css
-------------------------------------
Style for filr page

DatingApp.static.css.login.css
-------------------------------------
Style for login page

DatingApp.static.css.messages.css
-------------------------------------
Style for messages page

DatingApp.static.css.physicalFeatures.css
-------------------------------------
Style for physical features page

DatingApp.static.css.profile.css
-------------------------------------
Style for profile page

DatingApp.static.css.profileSettings.css
-------------------------------------
Style for profile settings page

DatingApp.static.css.settings.css
-------------------------------------
Style for settings page

DatingApp.static.css.signup.css
-------------------------------------
Style for sign up page

DatingApp.static.css.underConstruction.css
-------------------------------------
Style for under construction page

DatingApp.static.js.settings
------------------------------------
javascript for settings page

function: areYouSure- deletes account

DatingApp.static.js.signup
------------------------------------
javascript for signup page

function: showAlert- popup message

DatingApp.templates.accountSettings.html
-------------------------------------
Account settings page


DatingApp.templates.enterEducation.html
-------------------------------------
enter education page

part of profile setup

DatingApp.templates.enterOccupation.html
-------------------------------------
enter occupation page

part of profile setup

DatingApp.templates.filtr.html
-------------------------------------
filtr home page

main page for user interaction, allows users o view other user's and eithier "smash" or "pass" on thier profile

DatingApp.templates.login.html
-------------------------------------
Login page


DatingApp.templates.messages.html
-------------------------------------
messages page

DatingApp.templates.physicalFeatures.html
-------------------------------------
physical features page

user's enter thier physical features part of profile setup

DatingApp.templates.profile.html
-------------------------------------
profile page

user can view thier profile change thier picture and buy premium services

DatingApp.templates.profileSettings.html
-------------------------------------
profile settings page

settings for specifcally the user's profile

DatingApp.templates.settings.html
-------------------------------------
settings page


DatingApp.templates.signup.html
-------------------------------------
signup page

for users to signup with filtr

DatingApp.templates.underConstruction.html
-------------------------------------
under construction page

placeholder for pages that are being worked on.

DatingApp.app
------------------
Sets up functionality of webpages and holds query's needed for the application

