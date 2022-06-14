from models.query import Query
from werkzeug import security
from pymongo import MongoClient
from pymongo.errors import ExecutionTimeout, ServerSelectionTimeoutError
from flask import abort, jsonify, render_template
from utility import create_df, process_data, filter_device_names
from flask_login import login_user
from models.user import User
from threading import Timer
from flask_mail import Mail, Message
from flask_recaptcha import ReCaptcha
from random import randint
from flask import Flask, render_template

app = Flask(__name__)
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

# Recaptcha Verification

recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY="6LeKOaMZAAAAAI7L6TVsZa9A2t6-9LDVYSVqX9ZP",
    RECAPTCHA_SECRET_KEY="6LeKOaMZAAAAAKw9nhAjnpzrzrC3R0YYRf-kKDH1",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)



class Database:

    def __init__(self, uri: str):
        try:
            self.__client = MongoClient(uri)
        except ServerSelectionTimeoutError:
            pass
        self.pre_fetched_data = []
        self.__get_stats()

    def __check_connection(self):
        try:
            if self.__client.server_info()['ok'] != 1:
                abort(500)
        except ServerSelectionTimeoutError:
            abort(500)

    def verify_user(self, email: str, password: str):
        self.__check_connection()
        res = {}
        query = Query(key='email', value=email).get()
        db = self.__client['admin']['usercreds']
        try:
            res = db.find_one(query)
        except ExecutionTimeout:
            abort(500)
        if res is not None:
            user = User(res=res)
            # password = security.check_password_hash(user.password, password)
            if password:
                user.id = email
                login_user(user)
                msg = Message(subject='otp', sender='sagartiwari.bmp@gmail.com', recipients=[email])
                msg.body = str(otp)
                mail.send(msg)
                return render_template('verify.html')
            else:
                abort(401, 'wrong password')
        else:
            abort(401, 'user does not exist')

    def __get_stats(self):
        try:
            db = self.__client['admin']
            stat = filter_device_names(db.list_collection_names())
            for device in stat:
                device['doc_count'] = db[device['col_name']].count_documents(filter={})
                device['data_size'] = list(db[device['col_name']].aggregate([
                    {
                        '$group': {
                            '_id': None,
                            'rootSize': {'$sum': {'$bsonSize': '$$ROOT'}}
                        }
                    }
                ]))[0]['rootSize'] // 1000000
                device['data_size'] = f"{device['data_size']} MB"
            self.pre_fetched_data = stat
        except ServerSelectionTimeoutError:
            pass
        Timer(interval=60*30, function=self.__get_stats).start()

    def get_data(self, col: list, query: Query, save_as_one: bool = True):
        self.__check_connection()
        df_list = []
        res = []
        for device in col:
            print(f'[+] collecting data from {device.strip()} collection')
            db = self.__client['admin'][device.strip()]
            try:
                res = list(db.find(query.get(), {'_id': 0}).max_time_ms(max_time_ms=10000))
                print(f'[+] collecting data from {device.strip()} collection completed')
            except ExecutionTimeout:
                abort(500)
            if len(res) != 0:
                print(f'[+] converting that into a DataFrame')
                df_list.append(create_df(res))
        return process_data(df_list, col, save_as_one)
