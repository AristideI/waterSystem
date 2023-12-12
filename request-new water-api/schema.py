from marshmallow import fields,Schema


class PlainBranchSchema(Schema):
    branch_code = fields.String(required=True)
    name = fields.String(required=True)

class PlainDistrictSchema(Schema):
    name = fields.String(required=True)
    province = fields.String(required=True)

class PlainProvinceSchema(Schema):
    province = fields.String(required=True)

class PlainSectorSchema(Schema):
    _id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    branch_code=fields.String(required=True)

class PlainPocSchema(Schema):
    poc_code = fields.String(required=True)
    status = fields.String()
    customer_email=fields.String(required=True)

class PlainDisc_PaySchema(Schema):
    _id = fields.Integer(dump_only=True)
    poc_code = fields.String(required=True)
    doc_name=fields.String(required=True)

class PlainPocUpdateSchema(Schema):
    status = fields.String(required=True)

class PlainCellSchema(Schema):
    _id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

class PlainCustomerSchema(Schema):
    email = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    password = fields.String(load_only=True)

class PlainCustomerLoginSchema(Schema):
    password = fields.String(load_only=True)

class PlainCcoSchema(Schema):
    email = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    password = fields.String(load_only=True)

class PlainCcoLoginSchema(Schema):
    password = fields.String(load_only=True)

class PlainWdoSchema(Schema):
    email = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    password = fields.String(load_only=True)

class PlainWdoLoginSchema(Schema):
    password = fields.String(load_only=True)

class PlainHobSchema(Schema):
    email = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    password = fields.String(load_only=True)

class PlainCfoSchema(Schema):
    email = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    phone = fields.String(required=True)
    password = fields.String(load_only=True)

class PlainHobLoginSchema(Schema):
    password = fields.String(load_only=True)

class PlainCfoLoginSchema(Schema):
    password = fields.String(load_only=True)

class PlainClientRequestSchema(Schema):
    _id = fields.Integer(dump_only=True)
    province=fields.String(required=True)
    district=fields.String(required=True)
    sector=fields.String(required=True)
    cell=fields.String(required=True)
    village=fields.String(required=True)
    water_usage=fields.String(required=True)
    phone=fields.String(required=True)
    nid=fields.String(required=True)
    plotn=fields.String(required=True)
    nid_doc=fields.String()
    upi_doc=fields.String()
    payment=fields.String()
    request_date=fields.DateTime()
    status=fields.String()
    customer_email=fields.String(required=True)
    branch_code=fields.String(required=True)
    cco_email=fields.String(required=True)
    boq_doc=fields.String()
    rej_reason=fields.String()

class PlainClientRequestDOCMTSchema(Schema):
    nid_doc=fields.String(required=True)
    upi_doc=fields.String(required=True)

class PlainClientRequestBOQchema(Schema):
    boq_doc=fields.String(required=True)

class PlainClientRequestpayUploadchema(Schema):
    payment=fields.String(required=True)

class PlainClientRequestStatusSchema(Schema):
    status=fields.String(required=True)
    rej_reason=fields.String()
    
class BranchSchema(PlainBranchSchema):
    sectors=fields.List(fields.Nested(PlainSectorSchema()),dump_only=True)
    ccos=fields.List(fields.Nested(PlainCcoSchema()),dump_only=True)
    wdos=fields.List(fields.Nested(PlainWdoSchema()),dump_only=True)
    hobs=fields.List(fields.Nested(PlainHobSchema()),dump_only=True)
    clientRequests=fields.List(fields.Nested(PlainClientRequestSchema()),dump_only=True)

class DistrictSchema(PlainDistrictSchema):
    sectors=fields.List(fields.Nested(PlainSectorSchema()),dump_only=True)

class PocSchema(PlainPocSchema):
    customer=fields.Nested(PlainCustomerSchema(),dump_only=True)

class SectorSchema(PlainSectorSchema):
    district_name = fields.String(required=True)
    district=fields.Nested(PlainDistrictSchema(),dump_only=True)
    cells=fields.List(fields.Nested(PlainCellSchema()),dump_only=True)
    branch=fields.Nested(PlainBranchSchema(),dump_only=True)

class CellSchema(PlainCellSchema):
    sector_id =  fields.Integer(required=True)
    sector=fields.Nested(PlainCellSchema(),dump_only=True)

class CcoSchema(PlainCcoSchema):
    branch_code = fields.String(required=True)
    branch=fields.Nested(PlainBranchSchema(),dump_only=True)
    clientRequests=fields.List(fields.Nested(PlainClientRequestSchema()),dump_only=True)

class HobSchema(PlainHobSchema):
    branch_code = fields.String(required=True)
    branch=fields.Nested(PlainBranchSchema(),dump_only=True)
    clientRequests=fields.List(fields.Nested(PlainClientRequestSchema()),dump_only=True)

class WdoSchema(PlainWdoSchema):
    branch_code = fields.String(required=True)
    branch=fields.Nested(PlainBranchSchema(),dump_only=True)
    clientRequests=fields.List(fields.Nested(PlainClientRequestSchema()),dump_only=True)

class ClientRequestSchema(PlainClientRequestSchema):
    wdo_email=fields.String()
    hob_email=fields.String()
    customer=fields.Nested(PlainCustomerSchema(),dump_only=True)
    branch=fields.Nested(PlainBranchSchema(),dump_only=True)
    cco=fields.Nested(PlainCcoSchema(),dump_only=True)
    wdo=fields.Nested(PlainWdoSchema(),dump_only=True)
    hob=fields.Nested(PlainHobSchema(),dump_only=True)

class PlainSendMailSchema(Schema):
    sendto=fields.String()
    verification_code=fields.String()
    username=fields.String()
    _id=fields.String()
    title=fields.String()

class CustomerSchema(PlainCustomerSchema):
    pocs=fields.List(fields.Nested(PlainPocSchema()),dump_only=True)

class Disc_PaySchema(PlainDisc_PaySchema):
    paymentdate=fields.DateTime()
    poc = fields.Nested(PlainPocSchema(),dump_only=True)    

class PLainSendMailResponseSchema(Schema):
    result=fields.String()
