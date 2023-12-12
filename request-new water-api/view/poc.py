from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import PocModel
from schema import PocSchema,PlainPocSchema,PlainPocUpdateSchema
from sqlalchemy import and_


blp=Blueprint('poc',__name__,description='operation on poc')


@blp.route('/poc')
class Poc(MethodView):

    @blp.response(200,PocSchema(many=True))
    def get(self):
        return PocModel.query.all()

    @blp.arguments(PlainPocSchema)
    @blp.response(201,PocSchema)
    def post(self,hob_data):
        hob=PocModel(**hob_data)
        try:
            hob.save()
            return hob
        except:
            return abort(500,message="Error saving poc data")



@blp.route('/poc/<string:poc_code>')
class PocUpdate(MethodView):

    @blp.arguments(PlainPocUpdateSchema)
    @blp.response(200,PocSchema(many=True))
    def put(self,data,poc_code):
        poc=PocModel.find_by_id(poc_code)
        poc.status=data['status']
        try:
            poc.save()
            return poc
        except:
            return abort(500,message="Could not update poc status")

