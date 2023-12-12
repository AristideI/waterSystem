from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import DisconnectedPayModel
from schema import Disc_PaySchema,PlainDisc_PaySchema
from sqlalchemy import and_


blp=Blueprint('disconnectPay',__name__,description='operation on disconnectPay')


@blp.route('/disconnectPay')
class DisconnectPay(MethodView):

    @blp.response(200,Disc_PaySchema(many=True))
    def get(self):
        return DisconnectedPayModel.query.all()

    @blp.arguments(PlainDisc_PaySchema)
    @blp.response(200,Disc_PaySchema)
    def post(self,disc_pay):
        discp=DisconnectedPayModel(**disc_pay)
        try:
            discp.save()
            return discp
        except:
            return abort(500, message="Error saving payment ")
