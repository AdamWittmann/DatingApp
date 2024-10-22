"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Matches(db.Model):
    __tablename__ = 'Matches'
    MatchID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID1 = db.Column(db.Integer)
    UserID2 = db.Column(db.Integer)
    MatchDate = db.Column(db.String(8))


    def __init__(self, MatchID, UserID1, UserID2, MatchDate ):
        # remove pass and then initialize attributes
        self.MatchID = MatchID
        self.UserID1 = UserID1
        self.UserID2 = UserID2
        self.MatchDate = MatchDate


        def __repr__(self):
            # add text to the f-string
            return f"""
                MatchID: {self.LikeID}
                UserID1: {self.UserID1}
                UserID2: {self.UserID2}
                MatchDate: {self.MatchDate}
            """
            return self.__repr__()