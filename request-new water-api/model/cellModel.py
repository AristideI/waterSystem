from db import db

class CellModel(db.Model):

    __tablename__ = 'cell'

    _id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    sector_id = db.Column(db.Integer,db.ForeignKey('sector._id'))

    sector=db.relationship('SectorModel',back_populates='cells')

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> "CellModel":
        return cls.query.get_or_404(_id)

    
