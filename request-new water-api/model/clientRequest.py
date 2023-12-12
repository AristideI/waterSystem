from datetime import datetime
from db import db

class ClientRequestModel(db.Model):

    __tablename__ = 'clientRequest'

    _id = db.Column(db.Integer,primary_key=True)
    province=db.Column(db.String(80))
    district=db.Column(db.String(80))
    sector=db.Column(db.String(80))
    cell=db.Column(db.String(80))
    village=db.Column(db.String(80))
    water_usage=db.Column(db.String(80))
    phone=db.Column(db.String(80))
    nid=db.Column(db.String(80))
    plotn=db.Column(db.String(80))
    nid_doc=db.Column(db.String(80))
    upi_doc=db.Column(db.String(80))
    payment=db.Column(db.String(80))
    request_date=db.Column(db.DateTime,default=datetime.now)
    status=db.Column(db.String(80),default='cco pending')
    customer_email=db.Column(db.String(80),db.ForeignKey('customer.email'))
    branch_code=db.Column(db.String(5),db.ForeignKey('branch.branch_code'))
    cco_email=db.Column(db.String(80),db.ForeignKey('customeCareOfficer.email'))
    wdo_email=db.Column(db.String(80),db.ForeignKey('wateDistributionOfficer.email'))
    hob_email=db.Column(db.String(80),db.ForeignKey('headOfBranch.email'))
    boq_doc=db.Column(db.String(80))
    rej_reason=db.Column(db.String(1000))


    customer=db.relationship('CustomerModel',back_populates='clientRequests')
    branch=db.relationship('BranchModel',back_populates='clientRequests')
    cco=db.relationship('CcoModel',back_populates='clientRequests')
    wdo=db.relationship('WdoModel',back_populates='clientRequests')
    hob=db.relationship('HobModel',back_populates='clientRequests')


    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id) -> "ClientRequestModel":
        return cls.query.get_or_404(_id)

    
