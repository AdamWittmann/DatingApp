"""professor.py: create a table named professors in the marist database"""
from db.server import db

class User(db.Model):
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


    def __init__(self, FirstName, LastName, Email, PhoneNumber, Password, CreditCardNum, ExpirationDate, SecurityCode, BillingAddress, IsSub, SubStart, SubEnd ):
        # remove pass and then initialize attributes
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.Password = Password
        self.CreditCardNum = CreditCardNum
        self.ExpirationDate = ExpirationDate
        self.SecurityCode = SecurityCode
        self.BillingAddress = BillingAddress
        self.IsSub = IsSub
        self.SubStart = SubStart
        self.SubEnd = SubEnd


    def __repr__(self):
        # add text to the f-string
        return f"""
            "FIRST NAME: {self.FirstName},
             LAST NAME: {self.LastName},
             EMAIL: {self.Email},
             PHONE NUMBER: {self.PhoneNumber},
             PASSWORD: {self.Password}
             CreditCardNum: {self.CreditCardNum}
             ExpirationDate: {self.ExpirationDate}
             SecurityCode: {self.SecurityCode}
             BillingAddress: {self.BillingAddress}
             IsSub: {self.IsSub}
             SubStart: {self.SubStart}
             SubEnd: {self.SubEnd}
        """
        return self.__repr__()