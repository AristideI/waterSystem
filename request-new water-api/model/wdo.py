from db import db

class WdoModel(db.Model):

    __tablename__ = 'wateDistributionOfficer'

    email = db.Column(db.String(100),primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    password = db.Column(db.String(100))
    branch_code = db.Column(db.String(5), db.ForeignKey("branch.branch_code"))

    branch=db.relationship('BranchModel',back_populates='wdos')
    clientRequests=db.relationship('ClientRequestModel',back_populates='wdo')

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, _email: str) -> "WdoModel":
        return cls.query.get_or_404(_email)

    
