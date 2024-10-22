"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Likes(db.Model):
    __tablename__ = 'Likes'
    LikeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer)
    LikedUserID = db.Column(db.Integer)
    DateLiked = db.Column(db.String(8))


    def __init__(self, LikeID, UserID, LikedUserID, DateLiked ):
        # remove pass and then initialize attributes
        self.LikeID = LikeID
        self.UserID = UserID
        self.LikedUserID = LikedUserID
        self.DateLiked = DateLiked


        def __repr__(self):
            # add text to the f-string
            return f"""
                LikeID: {self.LikeID}
                UserID: {self.UserID}
                LikedUserID: {self.LikedUserID}
                DateLiked: {self.DateLiked}
            """
            return self.__repr__()