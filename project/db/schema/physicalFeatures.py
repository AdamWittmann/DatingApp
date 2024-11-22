"""professor.py: create a table named professors in the marist database"""
from db.server import db

class PhysicalFeatures(db.Model):
    __tablename__ = 'PhysicalFeatures'
    FeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer,db.ForeignKey('profile.ProfileID'))    
    HairColor = db.Column(db.String(20))
    Height = db.Column(db.Integer)
    Weight = db.Column(db.Integer)
    EyeColor = db.Column(db.String(20))


    def __init__(self, FeatureID, ProfileID, HairColor, Height, Weight, EyeColor ):
        # remove pass and then initialize attributes
        self.FeatureID = FeatureID
        self.ProfileID = ProfileID
        self.HairColor = HairColor
        self.Height = Height
        self.Weight = Weight
        self.EyeColor = EyeColor


        def __repr__(self):
            # add text to the f-string
            return f"""
                FeatureID: {self.FeatureID}
                ProfileID: {self.ProfileID}
                HairColor: {self.HairColor}
                Height: {self.Height}
                Weight: {self.Weight}
                EyeColor: {self.EyeColor}


            """
            return self.__repr__()