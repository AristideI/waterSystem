from datetime import date, datetime
import functools
import json
import os
from flask import Flask,redirect,jsonify,render_template,flash,request,url_for,session,send_from_directory,make_response
import requests



def create_app():

    app=Flask(__name__)

    app.secret_key='oBQ4GBTlzpSwE2OCGzRCGcXVANO9bsYZL_Cf3CSEXPs'

    def login_required(route):
        @functools. wraps(route)
        def route_wrapper(*args, **kwargs):
            if not session.get('user'):
                return redirect(url_for("home"))
            return route(*args, **kwargs)
        return route_wrapper


    def stringtodateconv(dtstr):
        return datetime.strptime(dtstr[:10],'%Y-%m-%d')



    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('index.html')


######################
    @app.route('/customerLogin',methods=['GET', 'POST'])
    def customerLogin():

        if request.method == 'POST':
            email=request.form.get('email')
            password=request.form.get('password')

            r= requests.get(f'http://127.0.0.1:5000/customer/{email}/login',json={"password": password})
            if r.ok and json.loads(r.text):
                session['user']=json.loads(r.text)
                session['userStatus']='customer'
                return redirect(url_for('customerDashboard'))

            flash('Incorrect email or password')

        return render_template('customer-login.html')


##################
    @app.route('/customerRegister',methods=['GET', 'POST'])
    def customerRegister():

        if request.method == 'POST':
            fn=request.form.get('fn')
            ln=request.form.get('ln')
            email=request.form.get('email')
            password=request.form.get('password')
            passw_conf=request.form.get('passw_conf')
            phone=request.form.get('phone')

            if requests.get(f'http://127.0.0.1:5000/customer/{email}').ok:
                flash('The user already exists')
                return render_template('customer-register.html')
            if password != passw_conf:
                flash('You typed unmatching password')
                return render_template('customer-register.html')

            session['reg_client']={"lastname": ln,"password": password,"firstname": fn,"phone": phone,"email": email}
            r= requests.post('http://127.0.0.1:5000/customer',json=session['reg_client'])
            if r.ok:
                flash('The user is successfully registered')
                return redirect(url_for('customerLogin'))
           

        return render_template('customer-register.html')


##################
    @app.route('/customerDashboard', methods=['POST','GET'])
    @login_required
    def customerDashboard():

        cust=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/customer/{cust}').text
        r=json.loads(r)

        return render_template('customer-track-request.html',user=session.get('user'),cust_reqs=r.get('pocs'))



#############
    @app.route('/cfoLogin',methods=['GET', 'POST'])
    def wdoLogin():

        if request.method == 'POST':
            email=request.form.get('email')
            password=request.form.get('password')

            r= requests.get(f'http://127.0.0.1:5000/cfo/{email}/login',json={"password": password})
            print(r.content)
            if r.ok and json.loads(r.text):
                session['user']=json.loads(r.text)
                session['userStatus']='wdo'
                return redirect(url_for('wdoDashboard'))

            flash('Incorrect email or password')

        return render_template('wdo-login.html')



################
    @app.route('/filedownload')
    @login_required
    def file_download():

        data=request.args.get('data')
        data=eval(data)
        dwld=data['doc']
        folder=data['_id']
        return send_from_directory(f'../disconnectFile/{folder}',f'{dwld}',as_attachment=True,download_name=f'{dwld}')



#################
    @app.route('/cfoDashboard',methods=['GET', 'POST'])
    @login_required
    def wdoDashboard():

        wdo=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/poc').text
        r=json.loads(r)

        return render_template('wdo-dashboard.html',user=session.get('user'),cco_reqs=r)



###############
    @app.route('/pocStatus',methods=['POST','GET'])
    @login_required
    def saveBOQ():

        data=request.args.get('data')
        data=eval(data)
        data_code=data['code']
        requests.put(f'http://127.0.0.1:5000/poc/{data_code}',json={'status':data['status']})
        return redirect(url_for('wdoDashboard'))



###################
    @app.route('/customerPayment',methods=['GET','POST'])
    @login_required
    def customerPayment():

        if request.method == 'POST':
            _id= request.form.get('_id')
            fl=request.files.get('payment')
            payname=f'payment-{_id}.pdf'
            r=requests.post(f'http://127.0.0.1:5000/disconnectPay',json={"doc_name": payname,"poc_code": _id})
            r=json.loads(r.text)
            fldr=r.get('_id')
            os.mkdir(os.path.join(f'../disconnectFile/{fldr}'))
            fl.save(os.path.join(f'../disconnectFile/{fldr}',payname))
            flash('file is successfully uploaded')
            return render_template('customer-payment-upload.html',user=session.get('user'),_id=_id)

        _id=request.args.get('data')

        return render_template('customer-payment-upload.html',user=session.get('user'),_id=_id)


###############
    @app.route('/paidClient')
    @login_required
    def waitToConnect():

        r=requests.get(f'http://127.0.0.1:5000/disconnectPay').text
        r=json.loads(r)

        return render_template('wdo-water-connection.html',user=session.get('user'),cco_reqs=r,stdconv=stringtodateconv)



    @app.route('/manifest.json')
    def manifest():
        return send_from_directory('static', 'manifest.json')



    @app.route('/sw.js')
    def service_worker():
        response = make_response(send_from_directory('static', 'sw.js'))
        response.headers['Cache-Control'] = 'no-cache'
        return response


    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.errorhandler(404)
    def pageNoFound(error):
        return render_template('errors-404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors-403.html'), 403

    @app.errorhandler(500)
    def internalServerError(error):
        return render_template('errors-500.html'), 500

    @app.errorhandler(503)
    def serviceUnavailable(error):
        return render_template('errors-503.html'), 503
    
    return app