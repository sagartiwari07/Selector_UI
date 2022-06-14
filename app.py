# from crypt import methods
import json
from flask import Flask, jsonify, redirect, request, abort, send_file, render_template, session
from flask_login import LoginManager, login_required, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import Database
from models.user import User
from models.query import Query
from utility import file_exists
from dotenv import load_dotenv
import os
from flask_recaptcha import ReCaptcha
from flask_mail import Mail, Message
from random import randint
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)
app.secret_key = 'userr'
login_manager = LoginManager()
login_manager.init_app(app)

# Adding rate throttling
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute", "50 per hour"],
    storage_uri=os.getenv('LIMITER_STORAGE')
)

# initialising Database
db = Database('mongodb://mumbai11:study77%23@3.7.66.36:27017/?authMechanism=DEFAULT&authSource=admin')


# Recaptcha Verification

recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY="6LeKOaMZAAAAAI7L6TVsZa9A2t6-9LDVYSVqX9ZP",
    RECAPTCHA_SECRET_KEY="6LeKOaMZAAAAAKw9nhAjnpzrzrC3R0YYRf-kKDH1",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

# Email Verification

mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'sagartiwari.bmp@gmail.com'   
app.config['MAIL_PASSWORD'] = 'eznplbvuokcpqucw'                #App password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)


# Handling Errors
@app.errorhandler(400)
def bad_request(e):
    return jsonify(message=str(e)), 400


@app.errorhandler(401)
def unauthorized(e):
    return jsonify(message=str(e)), 401


@app.errorhandler(403)
def forbidden(e):
    return jsonify(message=str(e)), 403


@app.errorhandler(404)
def not_found(e):
    return jsonify(message=str(e)), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(message=str(e)), 405


@app.errorhandler(429)
def rate_limit(e):
    return jsonify(message=str(e)), 429


@app.errorhandler(500)
def server_error(e):
    return jsonify(message=str(e)), 500


@login_manager.unauthorized_handler
def unauthorized():
    abort(403, 'authentication required')


@login_manager.user_loader
def load_user(email):
    user = User()
    user.id = email
    return user

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/login')
def login():
    # if not current_user.is_authenticated:
        if request.args.__contains__('email') and request.args.__contains__('password'):
            email = request.args.get('email')
            password = request.args.get('password')     
            # (email, password)=db.verify_user(email, password)
            return db.verify_user(email, password)   
        else:
            abort(400)
    # else:
    #     return abort(400, 'already logged in')

@app.route('/validate',methods=['POST'])
@login_required
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp) or recaptcha.verify():
        return render_template('/dashboard.html')
    return render_template('error.html')     

@app.route('/device_details')
@login_required
def device_details():
    if len(db.pre_fetched_data) == 0:
        abort(500)
    else:
        return jsonify(message='ok', data=db.pre_fetched_data)


@app.route('/data', methods=['POST'])
@login_required
def data():
    post_data = json.loads(request.data.decode('UTF-8'))
    if post_data.__contains__('query') and post_data.__contains__('devices') and \
            post_data.__contains__('save_as_one'):
        devices = post_data.get('devices')
        query = Query(query_list=post_data.get('query'))
        return jsonify(message='ok', data=db.get_data(col=devices, query=query, save_as_one=post_data.get('save_as_one')))
    else:
        abort(400)


@app.route('/download/<path>')
@login_required
def download(path):
    if path is not None:
        if file_exists(path):
            return send_file(f'./files/{path}.zip', download_name='data.zip', as_attachment=True)
        else:
            abort(404, 'requested file not found')
    else:
        abort(400, 'invalid path')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='ok')


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=False)
