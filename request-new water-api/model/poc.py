from db import db

class PocModel(db.Model):

    __tablename__ = 'poc'

    poc_code = db.Column(db.String(100),primary_key=True)
    status = db.Column(db.String(80),default='connected')
    customer_email = db.Column(db.String(80), db.ForeignKey("customer.email"))

    customer=db.relationship('CustomerModel',back_populates='pocs')
    disc_pays=db.relationship('DisconnectedPayModel',back_populates='poc',lazy='dynamic')

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, _poccode: str) -> "PocModel":
        return cls.query.get_or_404(_poccode)

    
