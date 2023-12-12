from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import CfoModel
from schema import PlainCfoSchema,PlainCfoLoginSchema
from sqlalchemy import and_


blp=Blueprint('cfo',__name__,description='operation on cfo')


@blp.route('/cfo')
class Cfo(MethodView):

    @blp.response(200,PlainCfoSchema(many=True))
    def get(self):
        return CfoModel.query.all()

    @blp.arguments(PlainCfoSchema)
    @blp.response(201,PlainCfoSchema)
    def post(self,hob_data):
        hob=CfoModel(**hob_data)
        try:
            hob.save()
            return hob
        except:
            return abort(500,message="Error saving cfo data")

@blp.route('/cfo/<string:email>/login')
class CfobyLogin(MethodView):

    @blp.arguments(PlainCfoLoginSchema)
    @blp.response(200,PlainCfoSchema)
    def get(self,hob_data,email):
        return CfoModel.query.filter(and_(CfoModel.email==email, CfoModel.password==hob_data['password'])).first()