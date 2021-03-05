import flask
from flask import request, jsonify, session, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3 as sql
import urllib.request
import jwt
import datetime
import json
import socket

TOKEN = "11457afdfe3ca5de6a418cccad5f373d"

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'JlRlR3GRUl'
app.config["DEBUG"] = True

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped


class BadRequest(Exception):
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload

@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    if request_data['username'] and request_data['password'] == 'password':
        session['logged_in'] = True
        token = jwt.encode({
            'user' : request_data['username'],
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=1200)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403)

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message

    return jsonify(payload), 400

@app.route('/', methods=['GET'])
def home():
    return "<h1>Geolocation data storing application</p>"

@app.route('/add_info', methods=['POST'])
@check_for_token
def add_info():
    data = request.get_json()
    ip = get_ip_from_request_content(data)

    geo_info = get_geolocation_info(ip)
    insert_gelocation_info(geo_info)

    return jsonify({'message' : f"Geolocation data added for ip address: {ip}"})

@app.route('/delete_info', methods=['POST'])
def delete_info():
    data = request.get_json()
    print(data)
    ip = get_ip_from_request_content(data)

    delete_geolocation_info(ip)

    return jsonify({'message' : f"Geolocation data removed for ip address: {ip}"})

@app.route('/get_info', methods=['GET'])
def get_info():
    if 'ip' in request.args:
        ip = request.args['ip']
    else:
        raise BadRequest('Ip was not provided, please specify ip', 40000, { 'ext': 1 })
    
    result = fetch_info_from_database(ip)
    return(result)

def get_ip_from_request_content(data):
    if "type" not in data or "address" not in data:
        raise BadRequest('Request content has to include type and address keys', 40001, { 'ext': 1 })

    if data["type"] == "ip":
        ip = data["address"]
    elif data["type"] == "url":
        ip = socket.gethostbyname(data["address"])
        
    else:
        raise BadRequest('Type value has to be equal to ip or url', 40002, { 'ext': 1 })
    
    return ip

def get_geolocation_info(ip):
    api = 'http://api.ipstack.com/' + ip + '?access_key=' + TOKEN + '&format=1'
    result = urllib.request.urlopen(api).read()
    result = result.decode()
    result = json.loads(result)

    return(result)

def insert_gelocation_info(info):    
    try:
        print(type(info))
        ip = info['ip'],
        continent_name = info['continent_name']
        country_name = info['country_name']
        latitude = info['latitude']
        longitude = info['longitude']
        zip_code = info['zip']

        with sql.connect("geolocation_info.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO GeolocationInfo (ip, continent_name, country_name, latitude, longitude, zip) VALUES (?,?,?,?,?,?)",
                        (ip[0], continent_name, country_name, str(latitude), str(longitude), zip_code))

            con.commit()

    except sql.Error as er:
        msg = 'SQLite error: %s' % (' '.join(er.args))
        raise BadRequest(msg, 40003, { 'ext': 1 })

    finally:
        con.close()

def delete_geolocation_info(ip):
    try:
        with sql.connect("geolocation_info.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM GeolocationInfo WHERE ip = ?", (ip,))

            con.commit()

    except sql.Error as er:
        msg = 'SQLite error: %s' % (' '.join(er.args))
        raise BadRequest(msg, 40004, { 'ext': 1 })

    finally:
        con.close()

def fetch_info_from_database(ip):
    try:
        with sql.connect("geolocation_info.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM GeolocationInfo WHERE ip = ?", (ip,))

            data = cur.fetchall()[0]
            names = list(map(lambda x: x[0], cur.description))
            result = dictionary = dict(zip(names, data))

            return result

    except sql.Error as er:
        msg = 'SQLite error: %s' % (' '.join(er.args))
        raise BadRequest(msg, 40005, { 'ext': 1 })

    finally:
        con.close()