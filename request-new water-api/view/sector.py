from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import SectorModel
from schema import SectorSchema,PlainSectorSchema

blp=Blueprint('sector',__name__,description='operation on sector')



@blp.route('/sector')
class Sector(MethodView):

    @blp.response(200,SectorSchema(many=True))
    def get(self):
        return SectorModel.query.all()

    @blp.arguments(SectorSchema)
    @blp.response(201,SectorSchema)
    def post(self,sector_data):
        sector=SectorModel(**sector_data)
        try:
            sector.save()
            return sector
        except:
            return abort(500,message="Error saving sector")

    

@blp.route('/sector/<int:_id>')
class SectorbyId(MethodView):

    @blp.response(200,SectorSchema)
    def get(self,_id):
        return SectorModel.find_by_id(_id)