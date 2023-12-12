from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import DistrictModel
from schema import DistrictSchema,PlainDistrictSchema,PlainProvinceSchema

blp=Blueprint('district',__name__,description='operation on district')



@blp.route('/district')
class District(MethodView):

    @blp.response(200,DistrictSchema(many=True))
    def get(self):
        return DistrictModel.query.all()

    @blp.arguments(PlainDistrictSchema)
    @blp.response(201,DistrictSchema)
    def post(self,district_data):
        district= DistrictModel(**district_data)
        try:
            district.save()
            return district
        except:
            return abort(500,message="Error savingDistrict")



@blp.route('/district/<string:name>')
class DistrictbyName(MethodView):

    @blp.response(200,DistrictSchema)
    def get(self,name):
        return DistrictModel.find_by_id(name)



@blp.route('/province')
class Province(MethodView):

    @blp.response(200,PlainProvinceSchema(many=True))
    def get(self):
        return DistrictModel.query.distinct(DistrictModel.province)



@blp.route('/province/<string:name>')
class ProvincebyName(MethodView):

    @blp.response(200,PlainDistrictSchema(many=True))
    def get(self,name):
        return DistrictModel.query.filter(DistrictModel.province==name)

