"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Education(db.Model):
    __tablename__ = 'Education'
    EducationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer,db.ForeignKey('Profile.ProfileID'))
    Degree = db.Column(db.String(30))
    Major = db.Column(db.String(30))
    GraduationYear = db.Column(db.String(4))
    School = db.Column(db.String(30))

    profile = db.relationship('Profile', backref='education', lazy='select')

    def __init__(self, EducationID, ProfileID, Degree, Major, GraduationYear, School ):
        # remove pass and then initialize attributes
        self.EducationID = EducationID
        self.ProfileID = ProfileID
        self.Degree = Degree
        self.Major = Major
        self.GraduationYear = GraduationYear
        self.School = School


        def __repr__(self):
            # add text to the f-string
            return f"""
                EducationID: {self.FeatureID}
                ProfileID: {self.ProfileID}
                Degree: {self.HairColor}
                Major: {self.Height}
                GraduationYear: {self.Weight}
                School: {self.EyeColor}


            """
            return self.__repr__()