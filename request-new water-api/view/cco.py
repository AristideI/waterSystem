from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import CcoModel
from schema import CcoSchema,PlainCcoSchema,PlainCcoLoginSchema
from sqlalchemy import and_

blp=Blueprint('cco',__name__,description='operation on cco')



@blp.route('/cco')
class Cco(MethodView):

    @blp.response(200,CcoSchema(many=True))
    def get(self):
        return CcoModel.query.all()

    @blp.arguments(CcoSchema)
    @blp.response(201,CcoSchema)
    def post(self,cco_data):
        cco=CcoModel(**cco_data)
        try:
            cco.save()
            return cco
        except:
            return abort(500,message="Error saving cco data")

    

@blp.route('/cco/<string:email>')
class CcobyId(MethodView):

    @blp.response(200,CcoSchema)
    def get(self,email):
        return CcoModel.find_by_id(email)



@blp.route('/cco/<string:email>/login')
class CcobyLogin(MethodView):

    @blp.arguments(PlainCcoLoginSchema)
    @blp.response(200,CcoSchema)
    def get(self,cco_data,email):
        return CcoModel.query.filter(and_(CcoModel.email==email,CcoModel.password==cco_data['password'])).first()