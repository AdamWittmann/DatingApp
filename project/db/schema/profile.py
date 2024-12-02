"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Profile(db.Model):
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

    user = db.relationship('User', backref='profiles', lazy=True)

    def __init__(self, ProfileID, UserID, Gender, Age, Religion, Bio, GenderPreference, Photo, Created, Updated ):
        # remove pass and then initialize attributes
        self.ProfileID = ProfileID
        self.UserID = UserID
        self.Gender = Gender
        self.Age = Age
        self.Religion = Religion
        self.Bio = Bio
        self.GenderPreference = GenderPreference
        self.Photo = Photo
        self.Created = Created
        self.Updated = Updated


        def __repr__(self):
            # add text to the f-string
            return f"""
                ProfileID: {self.ProfileID}
                UserID: {self.UserID}
                Gender: {self.Gender}
                Age: {self.Age}
                Religion: {self.Religion}
                Bio: {self.Bio}
                GenderPreference: {self.GenderPreference}
                Photo: {self.Photo}
                Created: {self.Created}
                Updated: {self.Updated}
            """
            return self.__repr__()