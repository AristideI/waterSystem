from flask.views import MethodView
from flask_smorest import abort,Blueprint
from schema import PlainSendMailSchema, PLainSendMailResponseSchema
import jinja2
from dotenv import load_dotenv
load_dotenv()
import requests
import os



blp=Blueprint('sendmail',__name__,description='operation on email')

@blp.route('/email')
class SendMail(MethodView):

    @blp.arguments(PlainSendMailSchema)
    @blp.response(200,PLainSendMailResponseSchema)
    def post(self,mail_data):
        send_simple_message(**mail_data)
        pass



template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)


def send_simple_message(sendto='',verification_code='',username='',_id='',title=''):
    return requests.post(
        f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
        auth=("api", f"{os.getenv('MAILGUN_API_KEY')}"),
        data={"from": f"wasac <mailgun@{os.getenv('MAILGUN_DOMAIN')}>",
            "to": [sendto],
            "subject": "WASAC",
            "text": "WASAC",
            "html":render_template("email.html",username=username,verification_code=verification_code,_id=_id,title=title)
            })