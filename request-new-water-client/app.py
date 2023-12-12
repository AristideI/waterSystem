from datetime import date, datetime
import functools
import json
import os
from flask import Flask,redirect,jsonify,render_template,flash,request,url_for,session,send_from_directory,make_response
import requests
from num2words import num2words
import time
import pyotp


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



    @app.route('/customerLogin',methods=['GET', 'POST'])
    def customerLogin():

        if request.method == 'POST':
            email=request.form.get('email')
            password=request.form.get('password')

            r= requests.get(f'http://127.0.0.1:5000/customer/{email}/login',json={"password": password})
            if r.ok and json.loads(r.text):
                session['user']=json.loads(r.text)
                fn=session['user']['firstname']
                ln=session['user']['lastname']
                key='wasac'
                totp=pyotp.TOTP(key)
                session['randomNumber']=totp.now()
                randomNumber=session['randomNumber']
                print(f'the ramdon mnudjh ===>>  {randomNumber}')
                requests.post('http://127.0.0.1:5000/email',json={"username": f"{fn} {ln}","verification_code": randomNumber,"sendto": email,"title": "Verification Code"})
                return redirect(url_for('login2fa'))

            flash('Incorrect email or password')

        return render_template('customer-login.html')



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
            key='wasac'
            totp=pyotp.TOTP(key)
            session['randomNumber']=totp.now()
            randomNumber=session['randomNumber']
            
            requests.post('http://127.0.0.1:5000/email',json={"username": f"{fn} {ln}","verification_code": randomNumber,"sendto": email,"title": "Verification Code"})
            return redirect(url_for('register2fa'))
           

        return render_template('customer-register.html')



    @app.route('/customerDashboard', methods=['POST','GET'])
    @login_required
    def customerDashboard():

        if request.method == 'POST':
            fn=request.form.get('fn')
            ln=request.form.get('ln')
            email=request.form.get('email')
            phone=request.form.get('phone')
            nid=request.form.get('nid')
            plotn=request.form.get('plotn')
            wu=request.form.get('wu')
            prov=request.form.get('prov')
            distr=request.form.get('distr')
            sect=request.form.get('sect')
            cell=request.form.get('cell')
            vill=request.form.get('vill')
            bra=request.form.get('bra')
            niddoc=request.files.get('niddoc')
            upidoc=request.files.get('upidoc')

            r1=requests.get(f'http://127.0.0.1:5000/branch/{bra}').text
            r1=json.loads(r1)
            
            sect=int(sect)
            r3=requests.get(f'http://127.0.0.1:5000/sector/{sect}').text
            r3=json.loads(r3)

            docinfo={"province": prov,"village": vill,"water_usage": wu,"branch_code": bra,"sector": r3['name'],"plotn": plotn,"customer_email": email,"district": distr,"cell": cell,"nid": nid,"phone": phone,"cco_email": r1['ccos'][0]['email']}
            
            r2=requests.post('http://127.0.0.1:5000/clientRequest',json=docinfo)
            if r2.ok:
                docval=json.loads(r2.text)
                docid=docval['_id']
                os.mkdir(os.path.join(f'../newWaterFile/{docid}'))
                nidname=f'{fn}-{ln}-nid-{docid}.pdf'
                upiname=f'{fn}-{ln}-upi-{docid}.pdf'
                niddoc.save(os.path.join(f'../newWaterFile/{docid}',nidname))
                upidoc.save(os.path.join(f'../newWaterFile/{docid}',upiname))
                requests.put(f'http://127.0.0.1:5000/clientRequest/{docid}',json={"upi_doc": upiname,"nid_doc": nidname})
                flash('The requested is successfully saved')
            else:
                flash('The requested is not saved')

        r=requests.get('http://127.0.0.1:5000/province').text

        return render_template('customer-dashboard.html',user=session.get('user'),provinces=json.loads(r))



    @app.route('/provinceName')
    def provinceName():
        province=request.args.get('province')
        r=requests.get(f'http://127.0.0.1:5000/province/{province}').text
        return json.loads(r)



    @app.route('/districtName')
    def districtName():
        district=request.args.get('district')
        r=requests.get(f'http://127.0.0.1:5000/district/{district}').text
        return json.loads(r)



    @app.route('/sectorName')
    def sectorName():
        sector=int(request.args.get('sector'))
        r=requests.get(f'http://127.0.0.1:5000/sector/{sector}').text
        return json.loads(r)



    @app.route('/customerTrackRequest')
    def customerTrackRequest():

        customer=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/customer/{customer}').text
        r=json.loads(r)

        return render_template('customer-track-request.html',user=session.get('user'),cust_reqs=r,stdconv=stringtodateconv)



    @app.route('/ccoLogin',methods=['GET', 'POST'])
    def cccoLogin():

        if request.method == 'POST':
            email=request.form.get('email')
            password=request.form.get('password')

            r= requests.get(f'http://127.0.0.1:5000/cco/{email}/login',json={"password": password})
            print(r.content)
            if r.ok and json.loads(r.text):
                session['user']=json.loads(r.text)
                session['userStatus']='cco'
                return redirect(url_for('ccoDashboard'))

            flash('Incorrect email or password')

        return render_template('cco-login.html')



    @app.route('/wdoLogin',methods=['GET', 'POST'])
    def wdoLogin():

        if request.method == 'POST':
            email=request.form.get('email')
            password=request.form.get('password')

            r= requests.get(f'http://127.0.0.1:5000/wdo/{email}/login',json={"password": password})
            print(r.content)
            if r.ok and json.loads(r.text):
                session['user']=json.loads(r.text)
                session['userStatus']='wdo'
                return redirect(url_for('wdoDashboard'))

            flash('Incorrect email or password')

        return render_template('wdo-login.html')



    @app.route('/hobLogin',methods=['GET', 'POST'])
    def hobLogin():

        if request.method == 'POST':
            email=request.form.get('email')
            password=request.form.get('password')

            r= requests.get(f'http://127.0.0.1:5000/hob/{email}/login',json={"password": password})
            print(r.content)
            if r.ok and json.loads(r.text):
                session['user']=json.loads(r.text)
                session['userStatus']='hob'
                return redirect(url_for('hobDashboard'))

            flash('Incorrect email or password')

        return render_template('hob-login.html')


    
    @app.route('/ccoDashboard',methods=['GET', 'POST'])
    @login_required
    def ccoDashboard():

        cco=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/cco/{cco}').text
        r=json.loads(r)

        return render_template('cco-dashboard.html',user=session.get('user'),cco_reqs=r)



    @app.route('/filedownload')
    @login_required
    def file_download():

        dwld=request.args.get('dwld')
        folder=dwld[-5]
        return send_from_directory(f'../newWaterFile/{folder}',f'{dwld}',as_attachment=True,download_name=f'{dwld}')



    @app.route('/updateToWdo')
    @login_required
    def update_to_wdo():
        data=request.args.get('data')
        requests.put(f'http://127.0.0.1:5000/clientRequest/status/{data}',json={"status": 'wdo pending'})
        return redirect(url_for('ccoDashboard'))



    @app.route('/wdoDashboard',methods=['GET', 'POST'])
    @login_required
    def wdoDashboard():

        wdo=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/wdo/{wdo}').text
        r=json.loads(r)

        return render_template('wdo-dashboard.html',user=session.get('user'),cco_reqs=r)



    @app.route('/billingOfQuality')
    @login_required
    def billingOfQuality():
        data=request.args.get('data')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/{data}').text
        r=json.loads(r)
        bra=r['branch_code']
        r1=requests.get(f'http://127.0.0.1:5000/branch/{bra}').text
        r1=json.loads(r1)
        return render_template('wdo-billing-of-quality.html',user=session.get('user'),areq=r,stdconv=stringtodateconv,nowtime=date.today(),hob=r1)



    @app.route('/wordsToNumbers')
    def wordsToNumbers():
        thenumber= request.args.get('word')
        return num2words(thenumber)



    @app.route('/saveBOQ',methods=['POST','GET'])
    @login_required
    def saveBOQ():

        if request.method == 'POST':
            _id= request.form.get('_id')
            fl=request.files.get('boq')
            boqname=f'boq-{_id}.pdf'
            fl.save(os.path.join(f'../newWaterFile/{_id}',boqname))
            requests.put(f'http://127.0.0.1:5000/clientRequest/boq/{_id}',json={"boq_doc": boqname})
            requests.put(f'http://127.0.0.1:5000/clientRequest/status/{_id}',json={"status": 'hob pending'})
            flash('file is successfully uploaded')
            return render_template('wdo-save-boq.html',user=session.get('user'),_id=_id)

        _id=request.args.get('data')

        return render_template('wdo-save-boq.html',user=session.get('user'),_id=_id)



    @app.route('/wdo_reject',methods=['POST','GET'])
    @login_required
    def wdo_reject():

        if request.method == 'POST':
            _id= request.form.get('_id')
            fl=request.form.get('rsn')
            requests.put(f'http://127.0.0.1:5000/clientRequest/status/{_id}',json={"status": 'cco pending',"rej_reason":fl})
            flash('request is successfully updated')
            return render_template('wdo_reject.html',user=session.get('user'),_id=_id)

        _id=request.args.get('data')

        return render_template('wdo_reject.html',user=session.get('user'),_id=_id)


    
    @app.route('/hobDashboard',methods=['GET','POST'])
    @login_required
    def hobDashboard():

        hob=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/hob/{hob}').text
        r=json.loads(r)

        return render_template('hob-dashboard.html',user=session.get('user'),cco_reqs=r)



    @app.route('/updateToFinal')
    @login_required
    def update_to_final():
        data=request.args.get('data')
        r=requests.put(f'http://127.0.0.1:5000/clientRequest/status/{data}',json={"status": 'payment pending'})
        r=json.loads(r.text)
        fn=r['customer']['firstname']
        ln=r['customer']['lastname']
        email=r['customer']['email']
        requests.post('http://127.0.0.1:5000/email',json={"username": f"{fn} {ln}","sendto": email,"title": "Water Request Approved","_id": data})
        return redirect(url_for('hobDashboard'))

        

    @app.route('/prePaymentList', methods=['POST','GET'])
    @login_required
    def prePayment():

        cust=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/payment/{cust}').text
        r=json.loads(r)

        return render_template('customer-pre-payment.html',user=session.get('user'),cco_reqs=r)



    @app.route('/customerPayment',methods=['GET','POST'])
    @login_required
    def customerPayment():

        if request.method == 'POST':
            _id= request.form.get('_id')
            fl=request.files.get('payment')
            payname=f'payment-{_id}.pdf'
            fl.save(os.path.join(f'../newWaterFile/{_id}',payname))
            requests.put(f'http://127.0.0.1:5000/clientRequest/payUpload/{_id}',json={"payment": payname})
            requests.put(f'http://127.0.0.1:5000/clientRequest/status/{_id}',json={"status": 'water connection pending'})
            flash('file is successfully uploaded')
            return render_template('customer-payment-upload.html',user=session.get('user'),_id=_id)

        _id=request.args.get('data')

        return render_template('customer-payment-upload.html',user=session.get('user'),_id=_id)



    @app.route('/waitToConnect')
    @login_required
    def waitToConnect():

        cust=session.get('user').get('email')
        r=requests.get(f'http://127.0.0.1:5000/clientRequest/waitToConnect/{cust}').text
        r=json.loads(r)

        return render_template('wdo-water-connection.html',user=session.get('user'),cco_reqs=r)


    
    @app.route('/updateToSuccess')
    @login_required
    def update_to_success():
        data=request.args.get('data')
        requests.put(f'http://127.0.0.1:5000/clientRequest/status/{data}',json={"status": 'completed'})
        return redirect(url_for('waitToConnect'))



    @app.route('/register2fa',methods=['POST','GET'])
    def register2fa():

        if request.method == 'POST':

            thecode=request.form.get('thecode')
            if thecode == session['randomNumber']:

                r= requests.post('http://127.0.0.1:5000/customer',json=session['reg_client'])
                if r.ok:
                    flash('The user is successfully registered')
                    return redirect(url_for('customerLogin'))

                flash('sorry we were unable to register the user')
                return redirect(url_for('customerRegister'))

            flash('sorry! Incorrect code')
        

        return render_template('register2fa.html')



    @app.route('/login2fa',methods=['POST','GET'])
    def login2fa():

        if request.method == 'POST':

            thecode=request.form.get('thecode')
            if thecode == session['randomNumber']:
                session['userStatus']='customer'
                return redirect(url_for('customerDashboard'))

            flash('sorry! Incorrect code')
        

        return render_template('register2fa.html')



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