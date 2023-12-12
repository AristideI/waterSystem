from db import db

class DistrictModel(db.Model):

    __tablename__ = 'district'

    name = db.Column(db.String(80),primary_key=True)
    province = db.Column(db.String(80))

    sectors=db.relationship('SectorModel',back_populates='district')


    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _name: str) -> "DistrictModel":
        return cls.query.get_or_404(_name)

    