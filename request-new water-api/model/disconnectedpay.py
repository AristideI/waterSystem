from datetime import datetime
from db import db

class DisconnectedPayModel(db.Model):

    __tablename__ = 'disconnected_pay'

    _id = db.Column(db.Integer,primary_key=True)
    doc_name = db.Column(db.String(80))
    paymentdate = db.Column(db.DateTime,default=datetime.now)
    poc_code = db.Column(db.String(100),db.ForeignKey('poc.poc_code') )

    poc=db.relationship('PocModel',back_populates='disc_pays')


    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> "DisconnectedPayModel":
        return cls.query.get_or_404(_id)