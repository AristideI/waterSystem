from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import WdoModel
from schema import WdoSchema,PlainWdoSchema,PlainWdoLoginSchema
from sqlalchemy import and_

blp=Blueprint('wdo',__name__,description='operation on wdo')



@blp.route('/wdo')
class Wdo(MethodView):

    @blp.response(200,WdoSchema(many=True))
    def get(self):
        return WdoModel.query.all()

    @blp.arguments(WdoSchema)
    @blp.response(201,WdoSchema)
    def post(self,wdo_data):
        wdo=WdoModel(**wdo_data)
        try:
            wdo.save()
            return wdo
        except:
            return abort(500,message="Error saving wdo data")

    

@blp.route('/wdo/<string:email>')
class WdobyId(MethodView):

    @blp.response(200,WdoSchema)
    def get(self,email):
        return WdoModel.find_by_id(email)



@blp.route('/wdo/<string:email>/login')
class WdobyLogin(MethodView):

    @blp.arguments(PlainWdoLoginSchema)
    @blp.response(200,WdoSchema)
    def get(self,wdo_data,email):
        return WdoModel.query.filter(and_(WdoModel.email==email,WdoModel.password==wdo_data['password'])).first()