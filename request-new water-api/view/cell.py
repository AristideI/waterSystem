from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import CellModel
from schema import CellSchema,PlainCellSchema

blp=Blueprint('cell',__name__,description='operation on cell')



@blp.route('/cell')
class Cell(MethodView):

    @blp.response(200,CellSchema(many=True))
    def get(self):
        return CellModel.query.all()

    @blp.arguments(CellSchema)
    @blp.response(201,CellSchema)
    def post(self,cell_data):
        cell=CellModel(**cell_data)
        try:
            cell.save()
            return cell
        except:
            return abort(500,message="Error saving cell data")



@blp.route('/cell/<int:_id>')
class CellbyId(MethodView):

    @blp.response(200,CellSchema)
    def get(self,_id):
        return CellModel.find_by_id(_id)