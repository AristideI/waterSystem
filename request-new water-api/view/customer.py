from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import CustomerModel
from schema import PlainCustomerSchema,PlainCustomerLoginSchema,CustomerSchema
from sqlalchemy import and_

blp=Blueprint('customer',__name__,description='operation on customer')



@blp.route('/customer')
class Customer(MethodView):

    @blp.response(200,CustomerSchema(many=True))
    def get(self):
        return CustomerModel.query.all()

    @blp.arguments(PlainCustomerSchema)
    @blp.response(201,CustomerSchema)
    def post(self,customer_data):
        customer=CustomerModel(**customer_data)
        try:
            customer.save()
            return customer
        except:
            return abort(500,message="Error saving customer")

    

@blp.route('/customer/<string:email>')
class CustomerbyId(MethodView):

    @blp.response(200,CustomerSchema)
    def get(self,email):
        return CustomerModel.find_by_id(email)


@blp.route('/customer/<string:email>/login')
class CustomerbyIdLogin(MethodView):

    @blp.arguments(PlainCustomerLoginSchema)
    @blp.response(200,CustomerSchema)
    def get(self,customer_data,email):
        return CustomerModel.query.filter(and_(CustomerModel.email==email, CustomerModel.password==customer_data['password'])).first()
