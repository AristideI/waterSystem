from db import db

class CustomerModel(db.Model):

    __tablename__ = 'customer'

    email = db.Column(db.String(100),primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(100))

    clientRequests=db.relationship('ClientRequestModel',back_populates='customer')
    pocs=db.relationship('PocModel',back_populates='customer')

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, _email: str) -> "CustomerModel":
        return cls.query.get_or_404(_email)

    
