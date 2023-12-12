from flask.views import MethodView
from flask_smorest import abort,Blueprint
from model import BranchModel
from schema import BranchSchema,PlainBranchSchema

blp=Blueprint('branch',__name__,description='operation on branch')



@blp.route('/branch')
class Branch(MethodView):

    @blp.response(200,BranchSchema(many=True))
    def get(self):
        return BranchModel.query.all()

    @blp.arguments(BranchSchema)
    @blp.response(201,BranchSchema)
    def post(self,branch_data):
        branch=BranchModel(**branch_data)
        try:
            branch.save()
            return branch
        except:
            return abort(500,mesage="Couldn't save branch")



@blp.route('/branch/<string:branch_code>')
class BranchbyId(MethodView):

    @blp.response(200,BranchSchema)
    def get(self,branch_code):
        return BranchModel.find_by_id(branch_code)



