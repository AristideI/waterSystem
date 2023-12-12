from db import db

class SectorModel(db.Model):

    __tablename__ = 'sector'

    _id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    district_name = db.Column(db.String(80),db.ForeignKey('district.name'))
    branch_code=db.Column(db.String(5),db.ForeignKey('branch.branch_code'))

    district=db.relationship('DistrictModel',back_populates='sectors')
    cells=db.relationship('CellModel',back_populates='sector')
    branch=db.relationship('BranchModel',back_populates='sectors')
    


    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> "SectorModel":
        return cls.query.get_or_404(_id)

    
