from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import ClientRequestModel,BranchModel
from schema import ClientRequestSchema,PlainClientRequestSchema,PlainClientRequestDOCMTSchema,PlainClientRequestStatusSchema,PlainClientRequestBOQchema,PlainClientRequestpayUploadchema
from sqlalchemy import and_

blp=Blueprint('clientRequest',__name__,description='operation on client request')



@blp.route('/clientRequest')
class ClientRequest(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self):
        return ClientRequestModel.query.all()

    @blp.arguments(PlainClientRequestSchema)
    @blp.response(201,ClientRequestSchema)
    def post(self,clientRequest_data):
        clientrequest=ClientRequestModel(**clientRequest_data)
        try:
            clientrequest.save()
            return clientrequest
        except:
            return abort(500,message="Error saving clientRequest data")

    

@blp.route('/clientRequest/<int:_id>')
class ClientRequestbyId(MethodView):

    @blp.response(200,ClientRequestSchema)
    def get(self,_id):
        return ClientRequestModel.find_by_id(_id)

    @blp.arguments(PlainClientRequestDOCMTSchema)
    @blp.response(201,ClientRequestSchema)
    def put(self,clientRequest_data,_id):
        clt= ClientRequestModel.find_by_id(_id)
        clt.nid_doc=clientRequest_data['nid_doc']
        clt.upi_doc=clientRequest_data['upi_doc']
        try:
            clt.save()
            return clt
        except:
            return abort(500,message="unable to update client request")



@blp.route('/clientRequest/customer/<string:customer_email>')
class ClientRequestbycustEmail(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self,customer_email):
        return ClientRequestModel.query.filter(ClientRequestModel.customer_email==customer_email)



@blp.route('/clientRequest/cco/<string:cco_email>')
class ClientRequestbyccoEmail(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self,cco_email):
        return ClientRequestModel.query.filter(and_(ClientRequestModel.cco_email==cco_email,ClientRequestModel.status=='cco pending'))



@blp.route('/clientRequest/status/<int:_id>')
class ClientRequestStatus(MethodView):

    @blp.arguments(PlainClientRequestStatusSchema)
    @blp.response(201,ClientRequestSchema)
    def put(self,clientRequest_data,_id):

        clt= ClientRequestModel.find_by_id(_id)
        clt.status=clientRequest_data['status']
        clt.rej_reason=clientRequest_data.get('rej_reason') or clt.rej_reason
        if 'wdo' in clientRequest_data['status']:
            branch= BranchModel.find_by_id(clt.branch_code)
            clt.wdo_email=branch.wdos[0].email
        elif 'hob' in clientRequest_data['status']:
            branch= BranchModel.find_by_id(clt.branch_code)
            clt.hob_email=branch.hobs[0].email
        try:
            clt.save()
            return clt
        except:
            return abort(500,message="unable to update client request")




@blp.route('/clientRequest/wdo/<string:wdo_email>')
class ClientRequestbywdoEmail(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self,wdo_email):
        return ClientRequestModel.query.filter(and_(ClientRequestModel.wdo_email==wdo_email,ClientRequestModel.status=='wdo pending'))



@blp.route('/clientRequest/boq/<int:_id>')
class ClientRequestBoQ(MethodView):

    @blp.arguments(PlainClientRequestBOQchema)
    @blp.response(201,ClientRequestSchema)
    def put(self,clientRequest_data,_id):

        clt= ClientRequestModel.find_by_id(_id)
        clt.boq_doc=clientRequest_data['boq_doc']
        try:
            clt.save()
            return clt
        except:
            return abort(500,message="unable to update client request")



@blp.route('/clientRequest/hob/<string:hob_email>')
class ClientRequestbyhobEmail(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self,hob_email):
        return ClientRequestModel.query.filter(and_(ClientRequestModel.hob_email==hob_email,ClientRequestModel.status=='hob pending'))


@blp.route('/clientRequest/payment/<string:cust_email>')
class ClientRequestbypaymentEmail(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self,cust_email):
        return ClientRequestModel.query.filter(and_(ClientRequestModel.customer_email==cust_email,ClientRequestModel.status=='payment pending'))



@blp.route('/clientRequest/payUpload/<int:_id>')
class ClientRequestPayUpload(MethodView):

    @blp.arguments(PlainClientRequestpayUploadchema)
    @blp.response(201,ClientRequestSchema)
    def put(self,clientRequest_data,_id):

        clt= ClientRequestModel.find_by_id(_id)
        clt.payment=clientRequest_data['payment']
        try:
            clt.save()
            return clt
        except:
            return abort(500,message="unable to update client request")




@blp.route('/clientRequest/waitToConnect/<string:wdo_email>')
class ClientRequestbywaitToConnectEmail(MethodView):

    @blp.response(200,ClientRequestSchema(many=True))
    def get(self,wdo_email):
        return ClientRequestModel.query.filter(and_(ClientRequestModel.wdo_email==wdo_email,ClientRequestModel.status=='water connection pending'))