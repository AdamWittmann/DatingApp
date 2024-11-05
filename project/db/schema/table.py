"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Table(db.Model):
    __tablename__ = 'Tables'
    TableID = db.Column(db.Integer,primary_key=True, autoincrement=True)

    def __init__(self):
        # remove pass and then initialize attributes
        pass

    def __repr__(self):
        # add text to the f-string
        return f"""

        """
    
    def __repr__(self):
        return self.__repr__()