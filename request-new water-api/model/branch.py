from db import db

class BranchModel(db.Model):

    __tablename__ = 'branch'

    branch_code = db.Column(db.String(5),primary_key=True)
    name = db.Column(db.String(80))

    sectors=db.relationship('SectorModel',back_populates='branch')
    ccos=db.relationship('CcoModel',back_populates='branch')
    wdos=db.relationship('WdoModel',back_populates='branch')
    hobs=db.relationship('HobModel',back_populates='branch')
    clientRequests=db.relationship('ClientRequestModel',back_populates='branch')


    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> "BranchModel":
        return cls.query.get_or_404(_id)

    
