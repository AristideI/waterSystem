from db import db

class CfoModel(db.Model):

    __tablename__ = 'customerFieldOfficer'

    email = db.Column(db.String(100),primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(100))

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, _email: str) -> "CfoModel":
        return cls.query.get_or_404(_email)

    
