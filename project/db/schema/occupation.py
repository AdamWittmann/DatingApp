"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Occupation(db.Model):
    __tablename__ = 'Occupation'
    OccupationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProfileID = db.Column(db.Integer)
    Job = db.Column(db.String(25))
    Salary = db.Column(db.Integer)

    def __init__(self, OccupationID, ProfileID, Job, Salary ):
        # remove pass and then initialize attributes
        self.OccupationID = OccupationID
        self.ProfileID = ProfileID
        self.Job = Job
        self.Salary = Salary


        def __repr__(self):
            # add text to the f-string
            return f"""
                OccupationID: {self.OccupationID}
                ProfileID: {self.ProfileID}
                Job: {self.Job}
                Salary: {self.Salary}
            """
            return self.__repr__()