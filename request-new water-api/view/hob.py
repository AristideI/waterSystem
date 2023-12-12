from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import HobModel
from schema import HobSchema,PlainHobSchema,PlainHobLoginSchema
from sqlalchemy import and_

blp=Blueprint('hob',__name__,description='operation on hob')



@blp.route('/hob')
class Hob(MethodView):

    @blp.response(200,HobSchema(many=True))
    def get(self):
        return HobModel.query.all()

    @blp.arguments(HobSchema)
    @blp.response(201,HobSchema)
    def post(self,hob_data):
        hob=HobModel(**hob_data)
        try:
            hob.save()
            return hob
        except:
            return abort(500,message="Error saving hob data")

    

@blp.route('/hob/<string:email>')
class HobbyId(MethodView):

    @blp.response(200,HobSchema)
    def get(self,email):
        return HobModel.find_by_id(email)




@blp.route('/hob/<string:email>/login')
class HobbyLogin(MethodView):

    @blp.arguments(PlainHobLoginSchema)
    @blp.response(200,HobSchema)
    def get(self,hob_data,email):
        return HobModel.query.filter(and_(HobModel.email==email, HobModel.password==hob_data['password'])).first()